import os
from twilio.rest import Client
import requests

account_sid = os.environ["ACf7bc3bab7a448622a43454fae58289f2"]
auth_token = os.environ["be5b242fbeef94750a9c397f5e3533cd"]
API_KEY = "f8c0e7fb43c0faba75a78f68dbd98d05"
LATITUDE = 23.7957
LONGITUDE = 86.4304
endpoint = "https://api.openweathermap.org/data/2.5/forecast"
weather_params = {
    "lat":LATITUDE,
    "lon":LONGITUDE,
    "appid":API_KEY,
    "cnt":4,
}
#recpvery_code = J2KNTHDFSBQCHBY3LUAY9MG4
response = requests.get(url=endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()

will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if condition_code < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_="whatsapp:+14155238886",
        body="It's going to rain today. Remember to bring an umbrella",
        to="whatsapp:+917004972945"
    )
print(message.status)



# while list < 4:
#     weather_id = weather_data["list"][list]["weather"][0]["id"]
#     list+=1
#     weather_id_list.append(weather_id)
#     if weather_id < 700:
#         print("Bring umbrella")