"""Handles the retrival, storage and handling of covid and covid news data.

Utilizes multithreading and the sched module to handle timed updates.
Includes functions for structuring the data.
"""

import sched
import time
import threading
import uuid
import logging

from .config import config

from . import covid_data_handler
from . import covid_news_handler

class BackgroundDataUpdateHandler():
    """Manages retrival, storage and handling of covid and covid news data.

    Upon initialization a thread is created that handles background updates.
    Only one instance should be created though instances are unlikely to interact with each other.
    """
    global_data_store: dict = {
        "covid_data": {
            "local": None,
            "national": None
        },
        "news_data": None,
        "removed_news_articles": []
    }
    scheduled_events: list = []
    scheduler_instance: sched.scheduler = None
    background_thread_instance: threading.Thread = None

    def __init__(self):
        logging.info("Initializing data store")
        self.update_covid_data()
        self.update_news_data()

        self.scheduler_instance = sched.scheduler(time.time, time.sleep)

        self.background_thread_instance = threading.Thread(
            target=self.__background_thread,
            daemon=True
        )
        self.background_thread_instance.start()

        logging.info("Started background event handler")

    def update_covid_data(self):
        """Update covid data (local and national) in this instance's data store"""
        logging.info("Updating covid data")
        self.global_data_store["covid_data"] = {
            "local": covid_data_handler.covid_api_request(
                location=config["location"],
                location_type=config["location-type"]
            ),
            "national": covid_data_handler.covid_api_request(
                location=config["location-nation"],
                location_type="nation"
            )
        }
        logging.info("Updated covid data")

    def update_news_data(self):
        """Update news data in this instance's data store"""
        logging.info("Updating news data")
        self.global_data_store["news_data"] = covid_news_handler.news_api_request()
        logging.info("Updated news data")

    # I would love to use url for this but template returns title
    def remove_news_article(self, title: str):
        """Stop a news article from being displayed in the future
        It does this by adding a news article's title to the list of removed news articles
        GRIPE: I would prefer to use urls instead of titles but I'm not allowed to edit the template
        """
        self.global_data_store["removed_news_articles"].append(title)

    def __background_thread(self):
        """Runs the scheduler on a loop
        Includes a sort delay to avoid any overloading
        Meant to be/Is run in a thread"""
        while True:
            self.scheduler_instance.run()
            time.sleep(0.1)

    def dashboard_data(self) -> dict:
        """Return data formatted for the dashboard template
        This might fit better in the flask request function.
        """

        def iterate_list_of_dicts_till_key_not_none(lod, key):
            for dic in lod:
                if dic[key] is not None:
                    return dic[key]

        # Can't do this bc I need {{ value|safe }} in the template and I can't edit its
        #def make_news_headlines_links(news_article):
        #    news_article["title"] = "<a href=\"{url}\">{title}</a>".format(**news_article)
        #    return news_article

        def filter_removed_articles(news_article):
            if news_article["title"] in self.global_data_store["removed_news_articles"]:
                return False
            else:
                return True

        local_data = self.global_data_store["covid_data"]["local"]
        national_data = self.global_data_store["covid_data"]["national"]

        news_articles = list(filter(
            filter_removed_articles,
            self.global_data_store["news_data"]["articles"])
        )

        organized_data = {
            "deaths_total": "Total Deaths: {}".format( #pylint: disable=consider-using-f-string
                iterate_list_of_dicts_till_key_not_none(national_data["data"],
                "cumDeaths28DaysByDeathDate"
            )),
            "hospital_cases": "Hospital Cases: {}".format( #pylint: disable=consider-using-f-string
                iterate_list_of_dicts_till_key_not_none(national_data["data"],
                "hospitalCases"
            )),
            "local_7day_infections": iterate_list_of_dicts_till_key_not_none(
                local_data["data"],
                "newCasesByPublishDateRollingSum"
            ),
            "national_7day_infections": iterate_list_of_dicts_till_key_not_none(
                national_data["data"],
                "newCasesByPublishDateRollingSum"
            ),
            "news_articles": news_articles
        }

        return organized_data

    def schedule(self, data_update: "DataUpdate"):
        """Schedules a data update event defined in the given instance of DataUpdate
        That instance is then added to scheduled_events
        """
        logging.info("Update named %s scheduled for %i seconds in the future",
            data_update.label,
            data_update.interval
        )
        data_update.sched_event_instance = self.scheduler_instance.enter(
            delay=10,
            priority=0,
            action=self._run_data_update,
            argument=[data_update]
        )
        self.scheduled_events.append(data_update)

    def remove(self, data_update: "DataUpdate"):
        """Cancels a scheduled event"""
        self.scheduler_instance.cancel(data_update.sched_event_instance)
        self.scheduled_events = list(filter(
            lambda i: i.uuid != data_update.uuid,
            self.scheduled_events
        ))

    def _run_data_update(self, data_update: "DataUpdate"):
        logging.info("Running data update")
        if data_update.update_covid_data:
            self.update_covid_data()
        if data_update.update_news_data:
            self.update_news_data()

        if data_update.repeat:
            self.scheduler_instance.enter(
            delay=data_update.interval,
            priority=0,
            action=self._run_data_update,
            argument=[data_update]
        )
        else:
            self.scheduled_events.remove(data_update)

class DataUpdate:
    """Represents a data update.

    Is passed to an instance of BackgroundDataUpdateHandler for scheduling and cancelation
    """
    uuid: str = ""
    label: str = ""
    interval: int = 0
    repeat: bool = False
    update_covid_data: bool = False
    update_news_data: bool = False
    sched_event_instance: bool = None

    def __init__(
        self,
        interval: int=0,
        label: str="Data Update",
        repeat: bool=False,
        update_covid_data: bool=False,
        update_news_data: bool=False
    ):
        self.uuid = uuid.uuid1()
        self.label = label
        self.interval = interval
        self.repeat = repeat
        self.update_covid_data = update_covid_data
        self.update_news_data = update_news_data

    def __str__(self) -> str:
        # Disable pylint message because no it could not be an f string
        # pylint: disable-next=consider-using-f-string
        return '''Name: {name}.
        Delay {interval} minutes.
        Updating covid data: {update_covid_data}.
        Updating news data: {update_news_data}.
        {repeating}.
        '''.format(name=self.label,
            interval=round(self.interval/60),
            update_covid_data="Yes" if self.update_covid_data else "No",
            update_news_data="Yes" if self.update_news_data else "No",
            repeating="Event will repeat" if self.repeat else ""
        )
