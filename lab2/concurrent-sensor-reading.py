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

# SHT30 sensor

async def sht30_function(sht30_sensor, interval=5):
    while True:
        temp = sht30_sensor.temperature
        hum = sht30_sensor.relative_humidity
        logger_1.info(f"Current time: {datetime.datetime.now().strftime('%H:%M:%S.%f')}")
        logger_1.info('Temperature: {0:.3f}°C'.format(temp))
        logger_1.info('Humidity: {0:.3f}%\n'.format(hum))
        await asyncio.sleep(interval)

# soil sensor

async def soil_function(ss, interval=6):
    while True:
        moisture = ss.get_temp()
        temp = ss.moisture_read()
        logger_2.info(f"Current time: {datetime.datetime.now().strftime('%H:%M:%S.%f')}")
        logger_2.info('Soil Moisture: {0:.3f}'.format(moisture))
        logger_2.info('Soil Temperature: {0:.3f}°C\n'.format(temp))
        await asyncio.sleep(interval)

# wind sensor
async def wind_function(ads, AnalogIn, ADS, interval=3):
    while True:
        chan = AnalogIn(ads, ADS.P0) # pin 0 analog input channel
        value = chan.value
        voltage = chan.voltage
        logger_3.info(f"Current time: {datetime.datetime.now().strftime('%H:%M:%S.%f')}")
        logger_3.info('Value = {0}, Voltage = {1}'.format(value, voltage))
        logger_3.info('Wind speed: {0:.3f}m/s\n'.format((chan.voltage - 0.4)*32.4/2))
        await asyncio.sleep(interval)


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
        sht30_function(sht30_sensor),
        soil_function(ss),
        wind_function(ads,AnalogIn, ADS)
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
