"""Main dashboard app file.
Defines the flask app object
"""

import logging

from flask import Flask, render_template, request, url_for, send_file

from .data_handler import DataUpdate, BackgroundDataUpdateHandler

from .config import config

logging.basicConfig(
    filename=config["logging"]["file"],
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s %(message)s'
)

app = Flask(__name__)

data_handler = BackgroundDataUpdateHandler()

@app.route("/healthcheck")
def healthcheck():
    """Returns "OK" if the app is running"""
    return "OK"

@app.route('/favicon.ico')
def favicon():
    """Returns the file /static/favicon.ico"""
    return send_file("static/favicon.ico")

@app.route("/")
@app.route("/index")
def dashboard():
    """Main dashboard view.
    Renders the template and handles requests
    """
    data = data_handler.dashboard_data()

    if "two" in request.args:
        if ":" in request.args["update"]:
            [hours, minutes] = list(map(int, request.args["update"].split(":")))
        else:
            hours = 0
            minutes = 5
        update_delay = minutes*60 + hours*60*60
        update_label = request.args["two"]
        update_repeat = "repeat" in request.args
        update_covid_data = "covid-data" in request.args

        update = DataUpdate(interval=update_delay,
            label=update_label,
            repeat=update_repeat,
            update_covid_data=update_covid_data
        )
        data_handler.schedule(update)

    if "update_item" in request.args:
        event_to_remove = filter(
            lambda i: i.label == request.args["update_item"],
            data_handler.scheduled_events
        )
        for event in event_to_remove:
            data_handler.remove(event)

    if "notif" in request.args:
        data_handler.remove_news_article(request.args["notif"])

    # Update data
    updates = []
    for event in data_handler.scheduled_events:
        updates.append({
            "title": event.label,
            "content": str(event)
        })


    return render_template("index.html",
        **data,
        location=config["location"],
        nation_location=config["location-nation"],
        updates=updates
    )

def run_app():
    """Run the app.
    Used by setup.py as the command line entrypoint.
    Same as main.py
    """
    app.run(
        debug=config["flask_debug"],
        host=config["host"],
        port=config["port"]
    )
