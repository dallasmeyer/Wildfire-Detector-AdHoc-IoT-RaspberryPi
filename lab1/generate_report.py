# Generates a report for the weather
import time
import requests
from datetime import datetime

time.sleep(20)
url = "https://api.open-meteo.com/v1/forecast?latitude=37&longitude=-122.06&daily=temperature_2m_max&timezone=America%2FLos_Angeles"

x = requests.get(url)

name = "Dallas Meyer\n"

now = datetime.now() # https://www.programiz.com/python-programming/datetime/current-datetime
time = now.strftime("%I:%M %p\n")
date = now.strftime("%m-%d-%Y\n\n")


payload = str(x.content)[2:-2]
with open("report.txt", "w") as file:
    file.write(name)
    file.write(time)
    file.write(date)
    file.write(payload)
