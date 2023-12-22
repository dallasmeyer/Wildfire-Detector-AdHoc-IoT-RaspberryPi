# Serially polls all sensors every 5 seconds
# Logs their measurements into a file named polling-log.txt
import time
from datetime import datetime

import board
import busio

# init sht30
import adafruit_sht31d
i2c = busio.I2C(board.SCL, board.SDA)
sht30_sensor = adafruit_sht31d.SHT31D(i2c)

# init moisture
from adafruit_seesaw.seesaw import Seesaw
i2c_bus = board.I2C()  # uses board.SCL and board.SDA
ss = Seesaw(i2c_bus, addr=0x36)

# init anemometer
# Voltage [0.4v,2.0v] max 32.4m/s wind speed
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1015(i2c) # ADC object


with open("polling-log.txt", "w") as file:
    while(True):
        file.write("Dallas Meyer\n")
        # time
        now = datetime.now() # https://www.programiz.com/python-programming/datetime/current-datetime
        t = now.strftime("%H:%M:%S")
        date = now.strftime("%m-%d-%Y")
        file.write(date + " " + t + "\n")
        
        file.write('Temperature: {0:.3f}°C\n'.format(sht30_sensor.temperature))
        file.write('Humidity: {0:.3f}%\n'.format(sht30_sensor.relative_humidity))
        file.write('Soil Moisture: {0:.3f}\n'.format(ss.moisture_read()))
        file.write('Soil Temperature: {0:.3f}°C\n'.format(ss.get_temp()))
        
        chan = AnalogIn(ads, ADS.P0) # pin 0 analog input channel
        file.write('Wind speed: {0:.3f}m/s\n\n'.format((chan.voltage - 0.4)*32.4/2))
        print("wrote to file")
        time.sleep(5)


