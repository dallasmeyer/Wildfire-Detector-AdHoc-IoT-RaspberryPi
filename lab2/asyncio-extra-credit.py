# Script  with three separate concurrent functions
# each function reads from a sensor and logs it current value
# wind sensor every 3s
# temp and humidity every 5s
# soil moisture every 6s

import asyncio
import datetime
import logging

# Blinka libraries

import time

import board
import busio

# Setting up our default logging format.
logging.basicConfig(format='[%(asctime)s] (%(name)s) %(levelname)s: %(message)s',)

# Set up loggers for each of our concurrent functions.
logger_1 = logging.getLogger('func1')
logger_2 = logging.getLogger('func2')
logger_3 = logging.getLogger('func3')

# Set the logging level for each of our concurrent functions to INFO.
logger_1.setLevel(logging.INFO)
logger_2.setLevel(logging.INFO)
logger_3.setLevel(logging.INFO)

# We will set up a common file handler for all of our loggers, and set it to INFO.
file_handler = logging.FileHandler('example.log')
file_handler.setLevel(logging.INFO)
# Add the file handler to each of our loggers.
logger_1.addHandler(file_handler)
logger_2.addHandler(file_handler)
logger_3.addHandler(file_handler)

# creating register of values array
# acts as a global variable
registers = [False, False, False]

# SHT30 sensor

async def sht30_function(sht30_sensor, sensor_num):
    while True:
        while registers[sensor_num] == False: # coroutine will loop without action
            await asyncio.sleep(0.01) # prevents the loop from using resources
        temp = sht30_sensor.temperature
        hum = sht30_sensor.relative_humidity
        logger_1.info(f"Current time: {datetime.datetime.now().strftime('%H:%M:%S.%f')}")
        logger_1.info('Temperature: {0:.3f}°C'.format(temp))
        logger_1.info('Humidity: {0:.3f}%\n'.format(hum))

        #set the flag to false
        registers[sensor_num] = False

# soil sensor

async def soil_function(ss, sensor_num):
    while True:
        while registers[sensor_num] == False: # coroutine will loop without action
            await asyncio.sleep(0.01) # prevents the loop from using resources
        moisture = ss.get_temp()
        temp = ss.moisture_read()
        logger_2.info(f"Current time: {datetime.datetime.now().strftime('%H:%M:%S.%f')}")
        logger_2.info('Soil Moisture: {0:.3f}'.format(moisture))
        logger_2.info('Soil Temperature: {0:.3f}°C\n'.format(temp))
        
        #set the flag to false
        registers[sensor_num] = False

# wind sensor
async def wind_function(ads, AnalogIn, ADS, sensor_num):
    while True:
        while registers[sensor_num] == False: # coroutine will loop without action
            await asyncio.sleep(0.01) # prevents the loop from using resources
        chan = AnalogIn(ads, ADS.P0) # pin 0 analog input channel
        value = chan.value
        voltage = chan.voltage
        logger_3.info(f"Current time: {datetime.datetime.now().strftime('%H:%M:%S.%f')}")
        logger_3.info('Value = {0}, Voltage = {1}'.format(value, voltage))
        logger_3.info('Wind speed: {0:.3f}m/s\n'.format((chan.voltage - 0.4)*32.4/2))
        
        #set the flag to false
        registers[sensor_num] = False

# Timer, which periodically sets flag to run all sensors.
async def timer(interval):
    while True:
        await asyncio.sleep(interval)
        # sets register global variable values to true.
        registers[0] = True
        registers[1] = True
        registers[2] = True

async def main():
    """
    The main coroutine, just awaits our concurrent functions.
    """

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

    await asyncio.gather(
        timer(3),
        sht30_function(sht30_sensor, 0),
        soil_function(ss, 1),
        wind_function(ads,AnalogIn, ADS, 2)
    )


if __name__ == "__main__":
    # We will use a try/except block to catch the KeyboardInterrupt.
    try:
        """
        Once we have defined our main coroutine, we will run it using asyncio.run().
        """
        asyncio.run(main())
    except KeyboardInterrupt:
        """
        If the user presses Ctrl+C, we will gracefully exit the program.
        """
        print("Exiting program...")
        exit(0)
