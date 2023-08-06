from covid_data_handler import *
from covid_news_handling import *
from flask import Flask, request, render_template, redirect

""" This module imports everything from covid_data_handler and covid_news_handling modules and imports Flask so a webpage is created with the
data from both of the modules and outputes an interactive covid dashboard"""

logger.info("covid_user_interface module:")

app = Flask(__name__)
app.debug=True

news_data = news_API_request()
closed_articles = []
news_covid_error = [{
            "title": "No Updates Selected  ",
            "content": "If you want to schedule an update select the time and what you want to update and press submit"
            }]

def news_removal():
    """ if the user removes a news articles it compares both the list and removes it from news api list"""  
    logger.info("news_removal:")
    logger.debug("Gets user request")
    news_articles = request.args.get("notif")
    closed_articles.append(news_articles)
    for article in news_data:
        if article["title"] in closed_articles:
            logger.debug("Article selected is removed")
            news_data.remove(article)
    logger.debug("returns data updated")
    return news_data


def calculate_time(update_time):
    """ calculates the time selected by the user and convertes it in seconds so that the data can be updated
    with the schedulers """
    logger.info("calculate_time:")
    time_update_hours = int(update_time.split(":")[0])
    time_update_minutes = int(update_time.split(":")[1])
    logger.debug("Gets time of the update in seconds")
    time_update = (time_update_hours*3600) + (time_update_minutes*60)
    logger.debug("Gets datetime")
    time_now = time.strftime("%H:%M:%S").split(":")
    time_now_hours = int(time_now[0])
    time_now_minutes = int(time_now[1])
    time_now_seconds = int(time_now[2])
    logger.debug("Gets datetime in seconds")
    time_int_seconds = (time_now_hours*3600) + (time_now_minutes*60) + (time_now_seconds)
    logger.debug("calculates time until update")
    time_before_update = time_update - time_int_seconds
    if time_update == time_int_seconds:
        news_covid_error.append({ 
            "title": "Data Update Succesful! " ,
            "content": ""
            })
    if time_before_update <= 0:
        time_before_update += 86400
    logger.debug("returns time until update")
    return time_before_update


def schedule_event():
    """ Gets every interaction from the user and it outputs some string and updates either covid data api or the news articles api
    or both depending on the user input. """
    logger.info("schedule_event:")
    s.run(blocking=False)
    logger.debug("Gets Update Time from user")
    #news_covid_error = []
    alarm = request.args.get("update")
    logger.debug("Gets input from the text field")
    text_field = request.args.get("two")
    logger.debug("Gets repeat update request from user")
    repeat = request.args.get("repeat")
    logger.debug("Gets covid data update request from user")
    covid_data_update = request.args.get("covid_data")
    logger.debug("Gets news data update request from user")   
    news_update = request.args.get("news")
    if alarm:
        logger.debug("update time is calculated")
        alarm_seconds = calculate_time(alarm)
    if covid_data_update:
        logger.debug("covid data request")
        schedule_covid_updates(covid_API_request, alarm_seconds, (data["location"], data["location_type"]))
        national_schedule_covid_updates(covid_API_request, alarm_seconds, (data["nation"], data["nation_type"]))
        news_covid_error.append({
            "title": "Covid Data will be Updated at:  " + alarm,
            "content": ""
            })
    if news_update:
        logger.debug("news articles request")
        update_news(news_API_request, alarm_seconds)
        news_covid_error.append({
                "title": "News Data will be Updated at:  " + alarm,
                "content": ""
                })
    if repeat and not news_update and not covid_data_update:
        logger.debug("only repeat update request ")            
        news_covid_error.append({
            "title": "Sorry, you have to select what you want to update",
            "content": ""
            })
    elif alarm and not repeat and not news_update and not covid_data_update:
        logger.debug("only update time request ")
        news_covid_error.append({
            "title": "Sorry, you have to select what you want to update",
            "content": ""
            })
    elif repeat and news_update and not covid_data_update:
        logger.debug(" repeat and news article update request")  
        update_news(news_API_request, alarm_seconds)  
        news_covid_error.append({
            "title": "The Update will be Repeated at :  " + alarm,
            "content": ""
            })     
    elif repeat and covid_data_update and not news_update:
        logger.debug("repeat and covid data update request ") 
        schedule_covid_updates(covid_API_request, alarm_seconds, ("Exeter", "ltla"))
        national_schedule_covid_updates(covid_API_request, alarm_seconds, (data["nation"], data["nation_type"]))
        news_covid_error.append({
            "title": "The Update will be updated at:  " + alarm,
            "content": ""
            })
    elif repeat and covid_data_update and news_update:
        logger.debug(" repeat and both covid data and news articles update request ")
        schedule_covid_updates(covid_API_request, alarm_seconds, ("Exeter", "ltla"))
        national_schedule_covid_updates(covid_API_request, alarm_seconds, (data["nation"], data["nation_type"]))
        update_news(news_API_request, alarm_seconds)
        news_covid_error.append({
            "title": "The Update will be  Repeated at:  " + alarm,
            "content": ""
            })
    logger.debug("return the four request")
    return alarm, text_field, covid_data_update, news_update


def update_removal():
    """ if the user removes the update message popping up it compares both the list and removes it from an update list"""  
    logger.info("update_removal:")
    closed_updates = []
    logger.debug("Gets user request")
    update_removal = request.args.get("update_item")
    closed_updates.append(update_removal)
    for update in news_covid_error:
        if update["title"] in closed_updates:
            logger.debug("update popping selected is removed")
            news_covid_error.remove(update)
    logger.debug("returns list updated")
    return news_covid_error


@app.route('/')
def home():
    """ home page """
    logger.info("home:")
    logger.debug("redirects to '/index page' ")
    return redirect("/index")


@app.route("/index")
def dashboard_index():
    logger.info("dashboard_index:")
    """ index page where the templates is uploaded and where all the covid data and news articles are outputed"""
    logger.debug("retuns the covid dashboard with all the requests")
    #print(s.queue)  
    events = schedule_event()
    return render_template("index.html", notif = news_removal(), title = "Covid19 Data Dashbord", news_articles = news_removal()[0:6], image = "masks.png", location = "Exeter", local_7day_infections = process_API_data(covid_API_request())[2],
    nation_location = "England", national_7day_infections = national_process_API_data(national_covid_API_request())[2],
    hospital_cases = national_process_API_data(national_covid_API_request())[1], deaths_total = national_process_API_data(national_covid_API_request())[0], 
    update = events[0], two = events[1], covid_data = events[2], news = events[3], updates = update_removal(), update_item = update_removal())

if __name__ == '__main__':
    app.run()
                      
