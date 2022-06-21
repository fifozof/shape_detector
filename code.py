
# zaimportowanie potrzebnych bibliotek
import time
import board
import busio
import adafruit_lis3dh

# Hardware I2C setup. Use the CircuitPlayground built-in accelerometer if available;
# otherwise check I2C pins.
if hasattr(board, "ACCELEROMETER_SCL"):
    i2c = busio.I2C(board.ACCELEROMETER_SCL, board.ACCELEROMETER_SDA)
    lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)
else:
    i2c = board.I2C()  # uses board.SCL and board.SDA
    lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c)

# Set range of accelerometer (can be RANGE_2_G, RANGE_4_G, RANGE_8_G or RANGE_16_G).
lis3dh.range = adafruit_lis3dh.RANGE_2_G

# Loop forever printing accelerometer values
while True:
    # Read accelerometer values (in m / s ^ 2).  Returns a 3-tuple of x, y,
    # z axis values.
    x, y, z = [
        value / adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration
    ]
    print("%f %f %f" % (x, y, z))
    # Small delay to keep things responsive but give time for interrupt processing.
    time.sleep(0.01)































# dac = analogio.AnalogOut(board.A0)  # on Trinket M0 & QT Py
# adc = analogio.AnalogIn(board.A1)
# i = 1
# res2 = 32767.5
#
#
# def get_voltage(pin):
#     return (pin.value * 3.3) / 65536
#
# #position = adc.value  # ranges from 0-65535
#
# while True:
#
#     sinewave = int(res2+res2*math.sin(i*math.pi/180))
#     dac.value = sinewave
#     i = i+1
#
#     if i == 360:
#         i = 1
#
#     #print((get_voltage(adc),)) # format for Mu editor plotter
#     #print(get_voltage(adc)) # format for Arduino editor plotter
#     print(adc.value >> 6) # format for SKP ex3 10bit adc data
#     time.sleep(0.01)
