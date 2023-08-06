#! /usr/bin/env python
# -*- coding: utf-8 -*-



# from AiDragonfly import constantModule
# from AiDragonfly import motorModule
# from AiDragonfly import sensorModule
# from AiDragonfly import musicModule
# import asyncio
# from functools import partial
# import platform
# from AiDragonfly.bleak import discover
# from AiDragonfly.bleak import BleakClient
# import time
# import sys

from . import constantModule
from . import motorModule
from . import sensorModule
from . import musicModule
from .bleak import discover
from .bleak import BleakClient
import asyncio
import time
import sys

# import constantModule
# import motorModule
# import sensorModule
# import musicModule
# import asyncio
# import time
# import sys
# from bleak import discover
# from bleak import BleakClient


# The global variable
_volume = 0
_engine = 0
_voltage = 0
_regeditNum = 0
_regedit = [[0 for i in range(50)] for j in range(30)]


def _data_xor_check(data):
    value = 0x00
    for i in data:
        value = value ^ i
    return value

def _int2hex(data,bitnum):
    if data < 0:
        if bitnum == 8:
            bdata = bin(data & 0xff)
            cdata = bdata[2:10]
        elif bitnum == 16:
            bdata = bin(data & 0xFFFF)
            cdata = bdata[2:18]
        ldata = []
        for i in cdata:
            ldata.append(i)
        sdata = ''
        for i in ldata:
            sdata = sdata + str(i)
        fdata = int(sdata, 2)
        return fdata
    else:
        fdata = data
        return fdata


def _hex2int(hexnum,bitnum):
    if (bitnum == 8)and(0xFF>=hexnum>=0x80):
        return ~(0xFF ^ hexnum)
    elif (bitnum == 16)and(0xFFFF>=hexnum>=0x8000):
        return ~(0xFFFF ^ hexnum)
    elif (bitnum == 32)and(0xFFFFFFFF>=hexnum>=0x80000000):
        return ~(0xFFFFFFFF ^ hexnum)
    else:
        return hexnum


def _protocol_analysis(num,data):
    global _receive_message
    global _regeditNum, _regedit, _volume, _engine, _voltage
    global i

    length = num
    _receive_message = data

    if length > 4:
        if _receive_message[0] == 0x55:
            buf = _receive_message
            if buf[0] == 0x55 and buf[-1] == 0xAA:
                if buf[1] == 0x01 and buf[2] == 0x04 and buf[3] == 0x01 and buf[4] == 0x00:
                    _volume = buf[5]
                    _engine = buf[6]
                elif buf[1] == 0x02 and buf[2] == 0x06 and buf[3] == 0x00 and buf[4] == 0xC8:
                    volume = buf[8] * 256 + buf[9]
                    # print('Synchronous voltage')
                    pass
                elif buf[1] == 0x01 and buf[2] == 0x02 and buf[3] == 0x00 and buf[4] == 0x00:
                    # print('The heartbeat packets')
                    pass
                elif buf[1] == 0x01 and buf[2] == 0x03 and buf[3] == 0x00 and buf[4] == 0x01:
                    # print('The registry starts uploading')
                    pass
                elif buf[1] == 0x01 and buf[2] == 0x03 and buf[3] == 0x01 and buf[4] == 0x01:
                    # print('Registry upload complete')
                    pass

                elif buf[1] == 0x01 and buf[2] == 0x06 and buf[3] == 0x00:
                    musicModule._version = (buf[4] << 24) + (buf[5] << 16) + (buf[6] << 8) + buf[7]

                elif buf[1] == 0x05 and buf[2] == 0x00 and buf[3] == 0x00:
                    if _regeditNum == 0:
                        _regedit[_regeditNum][0:20] = buf[0:20]
                        _regeditNum = _regeditNum + 1
                    else:
                        while True:
                            for i in list(range(_regeditNum)):
                                if _regedit[i][5:11] == buf[5:11]:
                                    break
                                else:
                                    i = i + 1
                            if i == _regeditNum:
                                _regedit[_regeditNum][0:20] = buf[0:20]
                                _regeditNum = _regeditNum + 1
                                break
                            else:
                                break

                elif buf[1] == 0x02 and buf[2] == 0x02 and buf[3] == 0x05:
                    motorModule.motor._rotation_completed_flag = 1
                    motorModule.motor._rotation_completed_port = buf[4]
                elif buf[1] == 0x02 and buf[2] == 0x06 and buf[3] == 0x00 and buf[4] == 0x0B:
                    if buf[11] == 4 or buf[11] == 5 or buf[11] == 6 or buf[11] == 7:
                        motorModule.motor._port_speed = buf[5]*256 + buf[6]
                    elif buf[11] == 0 or buf[11] == 1 or buf[11] == 2 or buf[11] == 3:
                        motorModule.motor._port_angle = buf[5]*256 + buf[6]

                elif buf[1] == 0x02 and buf[2] == 0x06 and buf[3] == 0x00:
                    if buf[10] == 0x00:
                        if buf[4] == sensorModule._sensor.regedit_num:
                            for i in list(range(_regeditNum)):
                                if sensorModule._sensor.regedit_num == _regedit[i][4]:
                                    if _regedit[i][5] == constantModule.SENSOR_DIGITAL_SERVO:
                                        if buf[11] == constantModule.DIGITALSERVO_GETANGLE:
                                            motorModule.digitalServo._angle = buf[5]*256 + buf[6]

                                    elif _regedit[i][5] == constantModule.SENSOR_OPTICAL:
                                        if buf[11] == constantModule.OPTICAL_COLOR:
                                            sensorModule.sensor_optical._color = buf[6]
                                        elif buf[11] == constantModule.OPTICAL_GRAY_SCALE:
                                            sensorModule.sensor_optical._grayScale = buf[6]
                                        elif buf[11] == constantModule.OPTICAL_RGB:
                                            sensorModule.sensor_optical._R = buf[5]
                                            sensorModule.sensor_optical._G = buf[6]
                                            sensorModule.sensor_optical._B = buf[7]
                                        elif buf[11] == constantModule.OPTICAL_AMBIENT_LIGHT_INTENSITY:
                                            sensorModule.sensor_optical._ambientLightIntensity = buf[5] * 256 + buf[6]
                                        elif buf[11] == constantModule.OPTICAL_KEY_STATUS:
                                            sensorModule.sensor_optical._keyStatus = buf[6]
                                        # elif buf[11] == constantModule.OPTICAL_SIGNAL_STRENGTH:
                                        #     sensorModule.sensor_optical._signalStrength = buf[6]

                                    elif _regedit[i][5] == constantModule.SENSOR_PHOTOSENSITIVE:
                                        if buf[11] == constantModule.PHOTOSENSITIVE_AMBIENT_LIGHT_INTENSITY:
                                            sensorModule.sensor_photosensitive._ambientLightIntensity = buf[5] * 256 + buf[6]

                                    elif _regedit[i][5] == constantModule.SENSOR_LASER:
                                        if buf[11] == constantModule.LASER_DISTANCE_MM:
                                            sensorModule.sensor_laser._distance_mm = buf[5]*256 + buf[6]
                                        elif buf[11] == constantModule.LASER_DISTANCE_CM:
                                            sensorModule.sensor_laser._distance_cm = buf[6]
                                        elif buf[11] == constantModule.LASER_KEY_STATUS:
                                            sensorModule.sensor_laser._keyStatus = buf[6]
                                        # elif buf[11] == constantModule.LASER_SIGNAL_STRENGTH:
                                        #     sensorModule.sensor_laser._signal_strength = buf[6]

                                    # elif _regedit[i][5] == constantModule.SENSOR_FLAME:
                                    #     if buf[11] == constantModule.FLAME_DIRECTION:
                                    #         sensorModule.sensor_infraredRadar._flameDirection = buf[6]
                                    #     elif buf[11] == constantModule.FLAME_INTENSITY:
                                    #         sensorModule.sensor_infraredRadar._flameIntensity = buf[6]
                                    #     elif buf[11] == constantModule.FLAME_KEY_STATUS:
                                    #         sensorModule.sensor_infraredRadar._keyStatus = buf[6]
                                    #     elif buf[11] == constantModule.FLAME_FOOTBALL_DIRECTION:
                                    #         sensorModule.sensor_infraredRadar._footballDirection = buf[6]

                                    elif _regedit[i][5] == constantModule.SENSOR_GEOMAGNETIC:
                                        if buf[11] == constantModule.GEOMAGNETIC_FIELD_ANGLE:
                                            sensorModule.sensor_geomagnetic._magneticFieldAngle = buf[5]*256 + buf[6]
                                        elif buf[11] == constantModule.GEOMAGNETIC_KEY_STATUS:
                                            sensorModule.sensor_geomagnetic._keyStatus = buf[6]

                                    elif _regedit[i][5] == constantModule.SENSOR_ATTITUDE:
                                        if buf[11] == constantModule.ATTITUDE_DICE:
                                            sensorModule.sensor_attitude._dice = buf[6]
                                        # elif buf[11] == constantModule.ATTITUDE_STEPS:
                                        #     sensorModule.sensor_attitude._steps = buf[5]*256 + buf[6]
                                        # elif buf[11] == constantModule.ATTITUDE_SIGNAL_STRENGTH:
                                        #     sensorModule.sensor_attitude._signalStrength = buf[6]
                                        elif buf[11] == constantModule.ATTITUDE_KEY_STATUS:
                                            sensorModule.sensor_attitude._keyStatus = buf[6]
                                        elif buf[11] == constantModule.ATTITUDE_ACCELERATION_X:
                                            sensorModule.sensor_attitude._acceleration_X = buf[5]*256 + buf[6]
                                        elif buf[11] == constantModule.ATTITUDE_ACCELERATION_Y:
                                            sensorModule.sensor_attitude._acceleration_Y = buf[5]*256 + buf[6]
                                        elif buf[11] == constantModule.ATTITUDE_ACCELERATION_Z:
                                            sensorModule.sensor_attitude._acceleration_Z = buf[5]*256 + buf[6]
                                        elif buf[11] == constantModule.ATTITUDE_ANGULAR_VELOCITY_X:
                                            sensorModule.sensor_attitude._angularVelocity_X = buf[5]*256 + buf[6]
                                        elif buf[11] == constantModule.ATTITUDE_ANGULAR_VELOCITY_Y:
                                            sensorModule.sensor_attitude._angularVelocity_Y = buf[5]*256 + buf[6]
                                        elif buf[11] == constantModule.ATTITUDE_ANGULAR_VELOCITY_Z:
                                            sensorModule.sensor_attitude._angularVelocity_Z = buf[5]*256 + buf[6]
                                        # elif buf[11] == constantModule.ATTITUDE_INCLINATION_ANGLE_X:
                                        #     sensorModule.sensor_attitude._inclinationAngle_X = buf[6]
                                        # elif buf[11] == constantModule.ATTITUDE_INCLINATION_ANGLE_Y:
                                        #     sensorModule.sensor_attitude._inclinationAngle_Y = buf[6]
                                        # elif buf[11] == constantModule.ATTITUDE_INCLINATION_ANGLE_Z:
                                        #     sensorModule.sensor_attitude._inclinationAngle_Z = buf[6]

                                    else:
                                        print('Sensor not found')
                    else:
                        print('sensor offline')


UART_SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
UART_RX_CHAR_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
UART_TX_CHAR_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

dev_match_ok = False


client = ''
async def con():
    dev_name = 'Onebot'
    dev_mac_addr = ''
    dev_con = bytearray([0x57, 0x01, 0x02, 0xAA])
    global dev_match_ok,client
    devices = await discover()
    for dev in devices:
        for i in range(0, 5):
            sys.stdout.write("=")
            sys.stdout.flush()
            time.sleep(0.1)
        devstr = str(dev)
        if devstr.find(dev_name) != -1:
            dev_match_ok = True
            dev_mac_addr = devstr[0:17]
            sys.stdout.write("=")
            sys.stdout.flush()
            time.sleep(0.1)
            break
    if dev_match_ok == True:
        async with BleakClient(dev_mac_addr) as client:
            for i in range(28, 31):
                if i != 30:
                    sys.stdout.write("=")
                else:
                    sys.stdout.write("= " + "100%/100%" + "\n")
                sys.stdout.flush()
                time.sleep(0.1)
            await client.write_gatt_char(UART_RX_CHAR_UUID, dev_con)
            await client.start_notify(UART_TX_CHAR_UUID, _protocol_analysis)
            await asyncio.sleep(2)
            await client.stop_notify(UART_TX_CHAR_UUID)
    else:
        print("\n" + '\033[1;31m Please Turn on the master power switch or Please insert the Bluetooth adapter \033[0m')
    return client


async def sendDate(data,client):
    databytes = bytearray(data)
    await client.write_gatt_char(UART_RX_CHAR_UUID,databytes)


async def receiveData(client):
    await client.start_notify(UART_TX_CHAR_UUID, _protocol_analysis)
    await asyncio.sleep(0.7)
    await client.stop_notify(UART_TX_CHAR_UUID)


ONEBOT = ''
dev = [0x57, 0x01, 0x02, 0xAA]
def start():
    global ONEBOT
    loop = asyncio.get_event_loop()
    ONEBOT = loop.run_until_complete(con())


if __name__ == '__main__':
    start()
    time.sleep(1)
    musicModule.sound(constantModule.SOUND_GENERAL_DOORBELL)
    time.sleep(2)



