# robot.py

"""
MicroPython code for Pico car project
* Raspberry Pi Pico mounted on differential drive car
* 56:1 gear motors with encoders
"""

import encoder_rp2 as encoder
import gc
import math
from machine import I2C, Pin, PWM, UART
from time import sleep
import motors
from odometer import Odometer
from parameters import TICKS_PER_METER, TARGET_TICK_RATE, TURN_SPD, ANGLE_TOL, SPD_GAIN
import struct
from bno08x_rvc import BNO08x_RVC
# import VL53L0X

# setup encoders
enc_b = encoder.Encoder(0, Pin(14))
enc_a = encoder.Encoder(1, Pin(12))

# setup onboard LED
led = machine.Pin("LED", machine.Pin.OUT)

# set up uart0 for communication with BLE UART friend
uart0 = UART(0, 9600)
uart0.init(bits=8, parity=None, stop=1, timeout=10)

'''
# set up left & right VCSEL TOF distance sensors
def setup_tof_sensor(bus_id, sda_pin, scl_pin):
    """Setup a Vcsel sensor on an I2C bus.
    There are two available busses: 0 & 1.
    Return VL53L0X object."""
    sda = Pin(sda_pin)
    scl = Pin(scl_pin)

    print("setting up i2c%s" % bus_id)
    i2c = I2C(id=bus_id, sda=sda, scl=scl)
    print("Set up device %s on i2c%s" % (i2c.scan(), bus_id))

    return VL53L0X.VL53L0X(i2c)


tof0 = setup_tof_sensor(0, 8, 9)  # Left
tof0.start()
tof1 = setup_tof_sensor(1, 10, 11)  # Right
tof1.start()
'''

# set up uart1 for IMU communication
uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5))
uart1.init(rxbuf=2048)
print(uart1)
rvc = BNO08x_RVC(uart1)
sleep(2) # wait for IMU to settle


yaw_prev = 0
N = 10  # number of 'fast' loop cycles per 'slow' loop
count = N
odom = Odometer()
while True:

    # get IMU data every time through loop
    try:
        yaw_degrees, *rest = rvc.heading
        # convert from degrees to radians
        yaw = -yaw_degrees * math.pi / 180 
        if yaw != yaw_prev:
            yaw_prev = yaw
    except Exception as e:
        print(e)
        yaw = yaw_prev

    # slow loop
    if count == 0:
        count = N

        '''
        # read distances from sensors
        dist0 = tof0.read()
        dist1 = tof1.read()
        # print("left, right = ", dist0, dist1)
        '''

        if uart0.any() > 0:
            try:
                # get Bluetooth command
                bytestring = uart0.readline()
                substring = bytestring[2:14]
                x, y, z = struct.unpack('3f', substring)
                print(x, y, z)
                lin_spd = y * SPD_GAIN
                ang_spd = -x * SPD_GAIN
            except Exception as e:
                lin_spd, ang_spd = 0, 0
                print(e)

            # get latest encoder values
            enc_a_val = enc_a.value()
            enc_b_val = enc_b.value()

            # send commands to motors
            motors.drive_motors(lin_spd, ang_spd)

        led.toggle()

    count -= 1
    sleep(0.01)  # time delay for 'fast' loop (the IMU likes this speed)