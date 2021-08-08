import requests
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("api_key")
account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
parameters = {"lat": os.getenv("lat"),
              "lon": os.getenv("lon"),
              "exclude": "current,minutely,daily",

              "appid": api_key}

response = requests.get(url="https://api.openweathermap.org/data/2.5/onecall", params=parameters)
response.raise_for_status()
data = response.json()
data_hour = data["hourly"]
will_rain = False
for _ in range(11):
    hour = data_hour[_]
    weather_id = hour["weather"][0]["id"]
    if weather_id < 600:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body="It's going to rain today. Bring an Umbrella",
        from_= os.getenv("trellonum"),
        to=os.getenv("yournum")
    )
    print(message.status)