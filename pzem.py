import minimalmodbus
import time

BAUDRATE = 9600
BYTESIZES = 8
STOPBITS = 1
TIMEOUT = 0.5
PARITY = minimalmodbus.serial.PARITY_NONE
MODE = minimalmodbus.MODE_RTU
SLAVEID = 1

device = minimalmodbus.Instrument('COM5', 0x02)
device.serial.baudrate = BAUDRATE
device.serial.bytesize = BYTESIZES
device.serial.parity = PARITY
device.serial.stopbits = STOPBITS
device.serial.timeout = 0.5
device.mode = MODE
device.clear_buffers_before_each_transaction = True

while True:
    data = device.read_registers(0x00,3,4)
    print(data)
    time.sleep(2)