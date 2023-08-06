"""
Load and process covid data
"""

from typing import List, Tuple
from uk_covid19 import Cov19API

def parse_csv_data(csv_filename: str) -> List[str]:
    """Returns a list of strings of the lines in the given csv file"""
    with open(csv_filename, 'r', encoding='utf-8') as csv_file:
        data = [line.strip() for line in csv_file]

    return data

def process_covid_csv_data(row_list: List[str]) -> Tuple[int, int, int]:
    """Returns covid data based on a list of strings representing rows from a csv file"""
    # Split each row in the list into a list of the values that were comma separated
    data = list(map(lambda row: row.split(","), row_list))

    # The first row contains the headers. The second row is empty and the third has incomplete data
    data_from_last_7_days = data[3:10]
    data_from_last_7_days = list(map(lambda column: column[6], data_from_last_7_days))
    data_from_last_7_days = list(map(int, data_from_last_7_days))
    cases_in_last_7_days = sum(data_from_last_7_days)

    current_hospital_cases = int(data[1][5])

    for row in data[1:]:
        if row[4] != "":
            total_deaths = int(row[4])
            break

    return (cases_in_last_7_days, current_hospital_cases, total_deaths)

def covid_api_request(location: str="Exeter", location_type: str="ltla") -> dict:
    """Proforms a covid api request.
    Uses the given location parameters and returns the resulting data structure.
    """
    api = Cov19API(
        filters=[
            "areaType=" + location_type,
            "areaName=" + location
        ],
        structure={
            "date": "date",
            "newCasesByPublishDate": "newCasesByPublishDate",
            "cumCasesByPublishDate": "cumCasesByPublishDate",
            "hospitalCases": "hospitalCases",
            "newCasesBySpecimenDate": "newCasesBySpecimenDate",
            "cumDeaths28DaysByDeathDate": "cumDeaths28DaysByDeathDate",
            "newCasesByPublishDateRollingSum": "newCasesByPublishDateRollingSum"
        }

    )

    # For some reason this returns a dict NOT json
    data = api.get_json()

    return data
