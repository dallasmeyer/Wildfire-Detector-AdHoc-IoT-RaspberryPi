import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

ads = ADS.ADS1015(i2c) # ADC object

chan = AnalogIn(ads, ADS.P0) # pin 0 analog input channel

# chan1 = AnalogIn(ads, ADS.P1) # pin 0 analog input channel
print(chan.value, chan.voltage)
# print(chan1.value, chan1.voltage)
