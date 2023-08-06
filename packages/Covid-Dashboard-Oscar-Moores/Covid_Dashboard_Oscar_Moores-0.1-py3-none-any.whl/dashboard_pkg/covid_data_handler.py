"""The main module, handles interactions with the dashboard, processing covid data and scheduling updates"""
from flask.helpers import url_for
from flask.wrappers import Request
from werkzeug.datastructures import Range
from werkzeug.utils import redirect
from werkzeug.wrappers import request
import sched, time, logging, json
from covid_news_handling import update_news
from uk_covid19 import Cov19API
from flask import Flask, render_template, url_for, request

#Setting up scheduler
schedulerObj = sched.scheduler(time.time, time.sleep)

#Opens config file and loads into the variable config_data then closes the file
file = open("config.json")
config_data = json.load(file)
file.close()

#Setting up logging file
logging.basicConfig(filename='event_log.log', level=logging.DEBUG)

#An array for holding information about current covid updates
covid_update_dictionary = {}
#A dictionary of values for updating the dashboard
dashboard_update_dictioanry = {
    "title":config_data["template_settings"]["title"],
    "location":None,
    "updates":[],
    "hospital_cases":"Local hospital cases: None",
    "deaths_total":"Deaths in local area: None",
    "location":config_data["location_terms"]["location"],
    "local_7day_infections":None,
    "nation_location":config_data["location_terms"]["nation_location"],
    "national_7day_infections":None,
    "news_articles":[]

}





#Setting up flask
app = Flask(__name__)

#Rendering the html template provided
@app.route("/")
def render_dashboard():
    """Updates values on webpage with values from dashboard_update_dictionary"""
    logging.debug("Function render_dashboard run")
    return(render_template("covidDashboard.html",
    title = dashboard_update_dictioanry["title"],
    updates = dashboard_update_dictioanry["updates"],
    hospital_cases = dashboard_update_dictioanry["hospital_cases"],
    deaths_total = dashboard_update_dictioanry["deaths_total"],
    location = dashboard_update_dictioanry["location"],
    local_7day_infections = dashboard_update_dictioanry["local_7day_infections"],
    nation_location = dashboard_update_dictioanry["nation_location"],
    national_7day_infections = dashboard_update_dictioanry["national_7day_infections"],
    news_articles = dashboard_update_dictioanry["news_articles"],
    ))


#Will get information from the webpage whenever the submit button is pressed 
#Will then run appropriate functions, schedule_covid_updates
@app.route("/index", methods=["GET"])
def get_page_data():
    """Gets values from webpage, is run whenever a button is pressed on the webpage \n
        Initiates the scheduling of an update if appropriate values are input \n
        Also initiates cancelling of an update or removal of a news article if correct button pressed
    """
    logging.debug("Function get_page_data run")

    #Returns the time input by the user in the form hours:minutes, or nothing no value can be found
    inputTime = request.values.get("update")
    logging.debug("requested values using flask, update: %s",inputTime)
    #Finding the name of the scheduled update 
    update_name = request.values.get("two")
    logging.debug("requested values using flask, two: %s",update_name)


    #Finding if an update needs to be deleted
    update_delete = request.values.get("update_item")
    logging.debug("requested values using flask, update_item: %s",update_delete)
    #Finding if an article needs to be deleted
    article_delete = request.values.get("notif")
    logging.debug("requested values using flask, notif: %s",article_delete)
    #If article_delete has a value then delete the article

    if (update_delete != None):
        logging.info("covid update is being removed")
        delete_covid_update(update_delete)
        #If update_delete has a value then delete the update
    elif (article_delete != None):
        logging.info("news article is being removed")
        exclude_news_title(article_delete) 
        #Making sure there are values for items required for scheduling event
    elif ((update_name != None) & (inputTime != None)):
        logging.info("Values input, event is to be scheduled")
        #Finding the abs time the scheduled update should take place
        update_interval = find_next_abs_time(inputTime)
        update_repeat = request.values.get("repeat")
        update_covid_data = request.values.get("covid-data")
        update_news_data = request.values.get("news")
        update_news = request.values.get("news")
        logging.debug("requested values using flask, repeat: %s ",update_repeat)
        logging.debug("requested values using flask, covid-data: %s ",update_covid_data)
        logging.debug("requested values using flask, news: %s ",update_news)

        #Create a dictionary for individual update, scheduled reperesents if the current item has been scheduled
        #covid_update and new_update will hold the scheduler objects
        update_dictionary = {"update_name":update_name,"update_interval":update_interval,"update_repeat":update_repeat,"update_covid_data":update_covid_data,"update_news_data":update_news_data,"update_news":update_news,"scheduled":0,"covid_update":None,"news_update":None}
        #Adds covid update to a dictionary holding all data about active covid updates
        covid_update_dictionary[update_name] = update_dictionary

        #Parses the update_dictionary into update_manager
        update_manager(update_dictionary)
    
    

    

    #Checks to see if anything is scheduled, means when page refreshes at regular interval
    #will update covid and news if needed
    logging.info("scheduler being run")
    schedulerObj.run(blocking=False)
    #Redirects the user back to the covid dashboard
    return redirect(url_for("render_dashboard"))




#Finds the next absolute time value that will occur for this input time (hours:mins)
def find_next_abs_time(inputTime):
    """Find the next absolute time value for the parameter input time \n
        :param name: inputTime  \n
        :param type: time \n
        :return: integer 
    """
    logging.debug("Function find_next_abs_time run with parameters: %s",inputTime)
    #Finding abs time of start of day by finding abs time of current time and then abs time of current time relative to start of day
    #Finding current abs time for local time, making sure it is the time for the start of the min
    absTimeCurrent = time.mktime(time.localtime()) - int(time.strftime("%S"))
    #Finding current hour and min of day
    hour, min = map(int, time.strftime("%H %M").split())
    absTimeCurrentOffset = hour * 60 * 60 + min * 60
    #Finding abs time of start of day
    absTimeStartDay = absTimeCurrent - absTimeCurrentOffset

    #Separating time into hours and mins
    splitTime = inputTime.split(":")
    hour = int(splitTime[0])
    min = int(splitTime[1])
    #Finds the time in seconds from the start of the day of the input time
    absTimeOffset = hour * 60 * 60 + min * 60

    #If true then the next schedulled time is tomorrow
    if (absTimeOffset < absTimeCurrentOffset):
        #Returns the abs time of schedulled time tomorrow, as todays time has already passed
        return(absTimeStartDay + 24 * 60 * 60 + absTimeOffset)
    else:
        #Returns abs time of schedulled time today
        return(absTimeOffset + absTimeStartDay)









#Takes filename, opens file and returns list of strings for rows in file
def parse_csv_data(csv_filename):
    """Opens a file with the name of the parameter csv_filename and returns the contents of the file as an list \n
        :param name: csv_filename \n
        :param type: string \n
        :return: list 
    """
    logging.debug("Function parse_csv_data run with parameters: %s",csv_filename)
    file = open(csv_filename,"r")
    list = []
    #Adds every line in the file to the list
    for line in file:
        list.append(line)

    file.close()
    #Returns list containing every line in file
    return(list)




#Takes data from csv file and returns num of cases in last week, 
#current hospital cases and cumulative deaths
def process_covid_csv_data(covid_csv_data):
    """Takes data from csv file and returns num of cases in last week, current hospital cases and cumulative deaths \n
        :param name: covid_csv_data \n
        :param type: list \n
        :return: int - the covid cases in the last week, int - the current covid cases, int - total deaths due to covid"""
    logging.debug("process_covid_csv_data run with covid csv data as parameters")
    #Getting date to use when finding relevent csv information

    cum_deaths = 0

    covid_cases_week = 0

    #Finding 7 day cases
    for i in range(3,10):

        data = covid_csv_data[i].split(",")[6].split("\n")[0]
        if (data != ""):
            covid_cases_week += int(data)

    #Finding current covid cases
    covid_current_cases = covid_csv_data[1].split(",")[5]
    if (covid_current_cases != ""):
        covid_current_cases = int(covid_current_cases)
    else:
        covid_current_cases = 0

    #Finding cumulative deaths
    for i in range(1,len(covid_csv_data)-1):
        if (covid_csv_data[i].split(",")[4] != ""):
            cum_deaths = int(covid_csv_data[i].split(",")[4])
            break
    

    return(covid_cases_week,covid_current_cases,cum_deaths)

#Takes the covid data dictionary and returns the required covid data
def process_covid_dict_data(covid_dict_data):
    """Takes data from an list of dictionaries and returns num of cases in last week, current hospital cases and cumulative deaths \n
        :param name: covid_dict_data - an list of covid data \n
        :param type: list \n
        :return: int - the covid cases in the last week, int - the current covid cases, int - total deaths due to covid"""
    logging.debug("Function process_covid_dict_data run with covid data dictionary as parameter")

    #Finding 7 day cases, the dictionary starts with an index of 1  
    covid_cases_week = 0
    for i in range(1,8):
        data = covid_dict_data[i]["newCasesBySpecimenDate"]
        covid_cases_week += data

    #Finding current covid cases
    covid_current_cases = covid_dict_data[i]["hospitalCases"]
    covid_current_cases = int(covid_current_cases)

    #Finding cumulative deaths
    cum_deaths = int(covid_dict_data[i]["cumDailyNsoDeathsByDeathDate"])
      
    return(covid_cases_week,covid_current_cases,cum_deaths)

#Makes a request with the covid API, default values Exeter and ltla gotten from config file
def covid_API_request(location = config_data["location_terms"]["location"],location_type = config_data["location_terms"]["location_type"]):
    """Queries the covid API and returns an list of dictionaries containing covid data
        :param name: location - the location data is to be requested for, location_type - the type of location the api is to be queried for \n
        :param type: string, string \n
        :return: list"""
    logging.debug("Function covid_API_request run with location parameter: %s",location)
    logging.debug("Function covid_API_request run with location_type parameter: %s",location_type)

    #Creates a filter, what location you are looking for data for
    filter = ["areaName="+location,"areaType="+location_type]
    #Defines the structure the data will be returned in
    dataStructure = {
        "areaCode":"areaCode",
        "areaName":"areaName",
        "areaType":"areaType","date":"date",
        "cumDailyNsoDeathsByDeathDate":"cumDailyNsoDeathsByDeathDate",
        "hospitalCases":"hospitalCases",
        "newCasesBySpecimenDate":"newCasesBySpecimenDate"
    }

    #Creates an Cov19API object
    api = Cov19API(filters=filter, structure=dataStructure)
    #Extracts data in csv format
    data = api.get_csv()

    #Splits data by line
    splitData = data.split("\n")

    #Creating the dictionary that will be returned containing covid data
    covid_dict_current = {}
    
    #Making an array of dictionaries, with each index being its own dictionary
    for i in range(1,len(splitData)-1):

        #Splits into each individual item
        individualItems = splitData[i].split(",")
        #Makes sure all items that are numbers and not null are numbers

        if (individualItems[4]):
            individualItems[4] = int(individualItems[4])
        else:
            individualItems[4] = 0
        if (individualItems[5]):
            individualItems[5] = int(individualItems[5])
        else:
            individualItems[5] = 0
        if (individualItems[6]):
            individualItems[6] = int(individualItems[6])
        else:
            individualItems[6] = 0
        
        #Makes a dictionary for current line
        tempDict = {"date":individualItems[3],"cumDailyNsoDeathsByDeathDate":individualItems[4],"hospitalCases":individualItems[5],"newCasesBySpecimenDate":individualItems[6]}
        
        #Adding index as key for dictionary returning covid data, beacause we have to return the data as a dictionary, not an array
        #which would be way easier for finding the covid data for the last week but hey why not
        covid_dict_current[i] = tempDict

    #Returns dictionary
    return(covid_dict_current)
    
#Takes a dictionary of information about an update and schedules covid updates based on its content
def update_manager(update_dictionary):
    """Takes the parameter update_dictionary as a parameter and based on its content runs a function to schedule a covid and or news update \n
        :param name: update_dictionary  \n
        :param type: dictionary
        """
    logging.debug("Function update_manager run with parameters: %s",update_dictionary)

    content = "Update scheuled for " + time.strftime("%H:%M",time.localtime(update_dictionary["update_interval"]))
    #Finding what content will be displayed
    if (update_dictionary["update_repeat"] == "repeat"):
        content = content + " every day. " 
    if (update_dictionary["update_covid_data"] == "covid-data"):
        content = content + "Updating covid data. "
    if (update_dictionary["update_news_data"] == "news"):
        content = content + "Updating news articles. "
    #Updates the dashboard update dictionary which will then update the scheduled updates section of the dashboard
    dashboard_update_dictioanry["updates"].append({
        "title":("Update name: "+str(update_dictionary["update_name"])),
        "content":(content)
    }) 



    #Checks to see what the updates are for, covid data or news
    if (update_dictionary["update_covid_data"] == "covid-data"):
        #Schedules a covid update
        schedule_covid_updates(update_dictionary["update_interval"],update_dictionary["update_name"])
    if (update_dictionary["update_news_data"] == "news"):
        #Schedules a news update
        schedule_news_updates(update_dictionary["update_interval"],update_dictionary["update_name"])

#Takes update name and time then schedules update 
def schedule_covid_updates(update_interval,update_name):
    """Takes the parameters update_interval and update_name and uses these to schedule a covid update \n
        :param name: update_interval - the absolute time an update is scheduled for, update_name - the name given to an update to be scheduled \n
        :param type: int, str
        """
    logging.debug("Function schedule_covid_updates run with update_interval parameter: %s",update_interval)
    logging.debug("Function schedule_covid_updates run with update_name parameter: %s",update_name)

    #Makes an object in the covid_update_dictionary the scheduled update to allow for easy cancellation
    covid_update_dictionary[update_name]["covid_update"] = schedulerObj.enterabs(update_interval,0,update_covid_data,argument=(update_name,))

    
#Takes update name and time then schedules update 
def schedule_news_updates(update_interval,update_name):
    """Takes the parameters update_interval and update_name and uses these to schedule a news update \n
        :param name: update_interval - the absolute time a covid update is scheduled for, update_name - the name given to an update to be scheduled \n
        :param type: int, str"""
    logging.debug("Function schedule_news_updates run with update_interval parameter: %s",update_interval)
    logging.debug("Function schedule_news_updates run with update_name parameter: %s",update_name)

    #Makes an object in the covid_update_dictionary the scheduled update to allow for easy cancellation
    covid_update_dictionary[update_name]["news_update"] = schedulerObj.enterabs(update_interval,0,add_to_news_datastructure)


    
#Updates the dashboard_update_dictionary with data from the covid API
def update_covid_data(update_name):
    """Takes the parameter update_news and updates the dashboard_update_dictionary with values from from the function covid_API_request so the dashboard displays relevent information when refreshed \n 
        Also schedules another update if the update with the name update_name is set to repeat \n
        :param name: update_name - the name given to an update to be scheduled \n
        :param type: str"""
    logging.debug("Function update_covid_data run with parameters: %s",update_name)

    #Calling covid_API_request to get up to date covid info for local area and processing 
    #it so dashboard can be updated
    covid_dict = covid_API_request()
    covid_cases_week,covid_current_cases,cum_deaths = process_covid_dict_data(covid_dict)
    #Updates the covid update dictionary with the data for a covid update with local area info
    dashboard_update_dictioanry["local_7day_infections"] = covid_cases_week
    dashboard_update_dictioanry["hospital_cases"] = ("Local hospital cases: "+str(covid_current_cases))
    dashboard_update_dictioanry["deaths_total"] = ("Deaths in local area: "+str(cum_deaths))
    #Calling covid_API_request to get up to date covid info for england and 
    #processing it so dashboard can be updated with national 7 day infection rate
    covid_dict = covid_API_request("England","nation")
    covid_cases_week,covid_current_cases,cum_deaths = process_covid_dict_data(covid_dict)
    #Updates the covid update dictionary with the data for a covid update with national 7 day infection rate
    dashboard_update_dictioanry["national_7day_infections"] = covid_cases_week

    #Finds if the update needs to be repeated
    logging.debug("Update repeat: %s",covid_update_dictionary[update_name]["update_repeat"])
    try:
        if (covid_update_dictionary[update_name]["update_repeat"] == "repeat"):
            logging.info("Update being repeated")
            #If the update needs to be repeated changes the updated interval for same time tomorrow
            covid_update_dictionary[update_name]["update_interval"] += 60*60*24
            #Schedules a covid update for 24 hours time
            schedule_covid_updates(covid_update_dictionary[update_name]["update_interval"],update_name) 
        else:
            logging.info("Update entries being deleted")
            #Deletes covid update and associated 
            delete_covid_update(update_name)
    except KeyError:
        logging.error("KeyError in update_covid_data")
    

    return redirect(url_for("render_dashboard"))


#Deletes covid updates from covid_update_dictionary and its update widget
def delete_covid_update(update_name):
    """Takes the parameter update_name and deletes any updates with that name \n
        :param name: update_name \n
        :param type: string"""
    logging.debug("Function delete_covid_update run with parameters: %s",update_name)
        
    try:
        #Deletes old update entry in update dictionary
        del covid_update_dictionary[update_name]
    except KeyError:
        logging.warning("KeyError in delete_covid_data when deleteing covid_update_dictionary entry")

    #Creates a temporary array
    temp_array = []
    #Looks for every widget not being deleted
    for index in range(0,len(dashboard_update_dictioanry["updates"])):
        if (dashboard_update_dictioanry["updates"][index]["title"] != update_name):
            #Adds widgets not being deleted to temp array
            temp_array.append(dashboard_update_dictioanry["updates"][index])

    #Replaces the old array with the new temp array
    dashboard_update_dictioanry["updates"] = temp_array
        
#Adds news article title to config file so they are excluded from being displayed in the future
def exclude_news_title(title):
    """Takes the parameter title and adds it to the file excluded.json, which means the news article will no longer be shown when the news section is updated \n
    :param name: title \n
    :param type: string"""
    logging.debug("Function exclude_news_title run with parameters: %s",title)

    #Adds excluded title to json then replaces file with updated config file
    file = open("excluded.json")
    excluded_json = json.load(file)
    file.close()
    file = open("excluded.json","w")
    excluded_json["excluded_article_titles"].append(title)
    json.dump(excluded_json,file)
    file.close()

    #Updates news articles with new articles
    add_to_news_datastructure()

    


#Adds news articles to the news data structure
def add_to_news_datastructure():
    """Updates the dashboard_update_dictionary with the function update_news, which returns the news articles so when the dashboard is updated the appear"""
    logging.debug("Function_add_to_news_datastructure run")
    #Updates the news dictionary with the data for a news update
    dashboard_update_dictioanry["news_articles"] = update_news()
    



#if running the script with python directly is true, but not if imports this module
if __name__ == "__main__":
    #Makes flask use debug mode so can update code and it appears on page
    app.run(debug=True)


    

