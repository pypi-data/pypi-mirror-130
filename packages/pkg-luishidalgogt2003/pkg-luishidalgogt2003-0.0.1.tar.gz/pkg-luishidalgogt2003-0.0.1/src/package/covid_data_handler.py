from uk_covid19 import Cov19API
import requests, json, sched, time
import logging

""" This Module handles the Covid Data in the CSV file and API and it processes both of this data into a list of dictonaries"""

s = sched.scheduler(time.time, time.sleep)
Log_format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="covid_dashboard.log", level=logging.DEBUG, format=Log_format, filemode="w")
logger = logging.getLogger()

logger.info("COVID19 DASHBOARD")
logger.info("covid_data_handling module:")

logger.debug("configuration file opens")
""" Configuration file needed for the sensitive information, such as API keys and also is needed to choose the city or nation where the
    api gets the data from and for the news articles terms."""
with open("config.json") as config_file:
    data = json.load(config_file)

def parse_csv_data(csv_filename):
    """ Opens csv file, iterates through the file and adds the content to a list"""
    logger.info("parse_csv_data:")
    logger.debug("Open The File")   
    lines = open(csv_filename, "r").readlines()
    data = []
    logger.debug("Iterate through the file and append to a list")
    for line in lines:
        data.append(line.strip())
    logger.debug("Return the list of data")
    return data


def test_parse_csv_data():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639


def process_covid_csv_data(covid_csv_data):
    """ Processes the Data from the parse_csv_data function and returns three values: current hospital cases, the last 7 days Covid cases 
    and the cumulative deaths recorded from the data in the function"""
    logger.info("process_covid_csv_data:")
    total_deaths = 0
    last7days_cases = 0
    logger.debug("calculates current hospital cases")
    current_hospital_cases = int(covid_csv_data[1].split(",")[5])
    logger.debug("calculates total deaths")
    total_deaths = int(covid_csv_data[14].split(",")[4])
    logger.debug("calculates last seven days cases")
    for i in range(3, 10):
        last7days_cases += int(covid_csv_data[i].split(",")[6])
    """ testing whether the data processed is correct"""
    logger.debug("returns the three values processed")
    return current_hospital_cases, last7days_cases, total_deaths
process_covid_csv_data(parse_csv_data("nation_2021-10-28.csv"))


def test_process_covid_csv_data():
    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data ( parse_csv_data (
            'nation_2021-10-28.csv' ) )
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544


def covid_API_request(location=data["location"], location_type=data["location_type"]):
    """ gets the Covid Data from the API and return the covid data of Exeter in a list of dictonaries
    in the structure of the variable up_to_date_data """
    logger.info("covid_API_request:({0}, {1})".format(location, location_type))
    types = ["areaType="+location_type,"areaName="+location]
    logger.debug("structure for the Covid19 API data")
    data_structure = { 
    "areaCode": "areaCode",
    "areaName": "areaName",
    "areaType": "areaType", 
    "date": "date", 
    "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate", 
    "hospitalCases": "hospitalCases", 
    "newCasesBySpecimenDate": "newCasesBySpecimenDate",
    "newCasesByPublishDate": "newCasesByPublishDate"
    }
    """ Covid19API is the API which was installed and imported in line1"""
    logger.debug("Gets all the data from the Covid19 API")
    api = Cov19API(filters=types, structure=data_structure)
    global response
    response = api.get_json()["data"]
    logger.debug("Returns the filtered Covid19 API data")
    return api.get_json()["data"]


def test_covid_API_request():
    data = covid_API_request()
    assert isinstance(data, list)


def process_API_data(API_data):
   """ Processes the data returned from covid_API_request and returns three values: the cumulative total deaths in Exeter,
    the current hospital casess in Exeter and the last 7 days cases in Exeter"""
   logger.info("process_API_data:")
   total_deaths = 0
   last7days_cases = 0
   logger.debug("Calculates the current hospital cases in covid_API_request")
   current_hospital_cases = API_data[1]["hospitalCases"]
   logger.debug("Calculates the total deaths in covid_API_request")
   total_deaths = API_data[1]["cumDailyNsoDeathsByDeathDate"]
   logger.debug("Calculates the last 7 days cases in covid_API_request")
   for i in range(0, 7):
        last7days_cases += API_data[i]["newCasesByPublishDate"]
   logger.debug("returns the three values calculated")
   return total_deaths, current_hospital_cases, last7days_cases


def national_covid_API_request(location=data["nation"], location_type=data["nation_type"]):
    """ gets the Covid Data from the API and return the covid data of England in a list of dictonaries
    in the structure of the variable up_to_date_data"""
    logger.info("national_covid_API_request:({0}, {1})".format(location, location_type))
    types = ["areaType="+location_type,"areaName="+location]
    logger.debug("structure for the Covid19 API data")
    up_to_date_data = { 
    "areaCode": "areaCode",
    "areaName": "areaName",
    "areaType": "areaType", 
    "date": "date", 
    "cumDailyNsoDeathsByDeathDate": "cumDailyNsoDeathsByDeathDate", 
    "hospitalCases": "hospitalCases", 
    "newCasesBySpecimenDate": "newCasesBySpecimenDate",
    "newCasesByPublishDate": "newCasesByPublishDate"
    }
    """ Covid19API is the API which was installed and imported in line1"""
    api = Cov19API(filters=types, structure=up_to_date_data)
    logger.debug("Gets all the data from the Covid19 API")
    global national_data
    national_data = api.get_json()["data"]
    logger.debug("Returns the filtered Covid19 API data")
    assert isinstance(response, list)
    return api.get_json()["data"] 


def test_national_covid_API_request():
    data = national_covid_API_request()
    assert isinstance(data, list)


def national_process_API_data(API_data):
    """ Processes the data returned from national_process_API_data and returns three values: the cumulative total deaths in England,
    the current hospital casess in England and the last 7 days cases in England"""
    logger.info("national_process_API_data:")
    total_deaths = 0
    last7days_cases = 0
    logger.debug("Calculates the current hospital cases in national_covid_API_request")
    for i in range(0, len(API_data)):
        if API_data[i]["hospitalCases"] != None:
            current_hospital_cases = API_data[2]["hospitalCases"]
            break
    logger.debug("Calculates the total deaths in  national_covid_API_request")
    for i in range(0, len(API_data)):
        if API_data[i]["cumDailyNsoDeathsByDeathDate"] != None:
            total_deaths = API_data[i]["cumDailyNsoDeathsByDeathDate"]
            break
    logger.debug("Calculates the last 7 days cases in national_covid_API_request")
    for i in range(0, 7):
        last7days_cases += API_data[i]["newCasesByPublishDate"]
    logger.debug("returns the three values calculated")
    return total_deaths, current_hospital_cases, last7days_cases


def schedule_covid_updates(update_name, update_interval, update_arguments):
    """ schedules covid data updates for both of the APIs and is called in another module """
    logger.info("schedule_covid_updates:({0}, {1}, {2})".format(update_name, update_interval, update_arguments))
    logger.debug("updating Covid19 data")
    s.enter(update_interval, 1, update_name, update_arguments)
    print("updating covid data...")


def test_schedule_covid_updates():
    schedule_covid_updates(update_interval=10, update_name='update test')


def national_schedule_covid_updates(update_name, update_interval, update_arguments):
    """ schedules national covid data updates for both of the APIs and is called in another module """
    logger.info("national_schedule_covid_updates:({0}, {1}, {2})".format(update_name, update_interval, update_arguments))
    logger.debug("updating  National Covid19 data")
    s.enter(update_interval, 1, update_name, update_arguments)
    print("updating national covid data...")


def test_national_schedule_covid_updates():
    national_schedule_covid_updates(update_interval=10, update_name='update test')