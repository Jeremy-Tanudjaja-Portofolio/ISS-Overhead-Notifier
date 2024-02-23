import time

import requests
import  datetime as dt
import smtplib

# Latitude first, then longitude
my_location = (-6.917464, 107.619125 )

def call_sunrise_hour():
    """ This Function will call when will sunrise comes in [hour]"""
    global my_location
    date = dt.datetime.now().date().strftime("%Y-%m-%d")

    # Latitude first, then longitude
    parameters = {"lat":my_location[0],
                  "lng":my_location[1],
                  "date":date,
                  "formatted": 0}

    URL_API = "https://api.sunrise-sunset.org/json"
    data = requests.get(url = URL_API, params=parameters)
    if data.status_code != 200:
        data.raise_for_status()

    # Return JSON Strings
    data_result = data.json()["results"]
    data_sunrise = data_result["sunrise"]
    data_sunset = data_result["sunset"]
    sunrise_hour = int(data_sunrise.split("T")[1].split(":")[0])
    sunset_hour =  int(data_sunset.split("T")[1].split(":")[0])
    return sunrise_hour, sunset_hour

def call_iss_location():
    """This Function will make an API call to get the coordinates of the ISS"""
    URL_API = "http://api.open-notify.org/iss-now.json"
    data = requests.get(url=URL_API)
    data_latitude = float(data.json()["iss_position"]["latitude"])
    data_longitude = float(data.json()["iss_position"]["longitude"])
    return data_latitude, data_longitude

def is_ISS_overhead():
    time_now = int(dt.datetime.now().hour)
    sun_time = call_sunrise_hour()
    location = call_iss_location()

    if time_now >= sun_time[1] or time_now <= sun_time[0]:
            if (my_location[0]+5 >= location[0] >= my_location[0]-5) and (my_location[1]+5 >= location[1] >= my_location[1]-5):
                # The ISS is Overhead
                send_email()
            else:
                print("The ISS is not Overhead")
    else:
        print("The ISS is not Overhead")


def send_email():
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user="sender@gmail.com", password="password")
        connection.sendmail(to_addrs="user@gmail.com",
                            from_addr="sender@gmail.com",
                            msg="Subject:ISS Location\n\nThe ISS is Overhead")


while True:
    is_ISS_overhead()
    time.sleep(3600)

