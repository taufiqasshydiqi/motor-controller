from pymodbus.server import StartAsyncTcpServer
from pymodbus.server import StartAsyncSerialServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import asyncio

class CallbackDataBlock(ModbusSequentialDataBlock):
    """A datablock that stores the new value in memory,.

    and passes the operation to a message queue for further processing.
    """

    def __init__(self, queue, addr, values):
        """Initialize."""
        self.queue = queue
        super().__init__(addr, values)

    def setValues(self, address, value):
        """Set the requested values of the datastore."""
        super().setValues(address, value)
        txt = f"Callback from setValues with address {address}, value {value}"
        print(txt)

    def getValues(self, address, count=1):
        """Return the requested values from the datastore."""
        result = super().getValues(address, count=count)
        txt = f"Callback from getValues with address {address}, count {count}, data {result}"
        # print(txt)
        return result

    def validate(self, address, count=1):
        """Check to see if the request is in range."""
        result = super().validate(address, count=count)
        txt = f"Callback from validate with address {address}, count {count}, data {result}"
        # print(txt)
        return result

async def run_async_server():
    queue = asyncio.Queue()
    block = CallbackDataBlock(queue, 0x00, [17] * 100)
    block.setValues(1, 15)
    store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
    context = ModbusServerContext(slaves=store, single=True)
    # nreg = 200
    # store = ModbusSlaveContext(
    #     di=ModbusSequentialDataBlock(0, [15]*nreg),
    #     co=ModbusSequentialDataBlock(0, [16]*nreg),
    #     hr=ModbusSequentialDataBlock(0, [17]*nreg),
    #     ir=ModbusSequentialDataBlock(0, [18,20]*nreg)
    # )
    context = ModbusServerContext(slaves=store, single=True)

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'bbt'
    identity.ProductCode = 'apaya'
    identity.VendorUrl = "www.bbt.com"
    identity.ProductName = "modbus server bbt"
    identity.ModelName = "modbus server"
    identity.MajorMinorRevision = "3.0.2"
    
    server = await StartAsyncSerialServer(
            context=context,  # Data storage
            identity=identity,  # server identify
            # timeout=1,  # waiting time for request to complete
            port='COM1',  # serial port
            # custom_functions=[],  # allow custom handling
            # framer=args.framer,  # The framer strategy to use
            stopbits=1,  # The number of stop bits to use
            bytesize=8,  # The bytesize of the serial messages
            parity="N",  # Which kind of parity to use
            baudrate=9600,  # The baud rate to use for the serial device
            # handle_local_echo=False,  # Handle local echo of the USB-to-RS485 adaptor
            # ignore_missing_slaves=True,  # ignore request to a missing slave
            # broadcast_enable=False,  # treat slave_id 0 as broadcast address,
            # strict=True,  # use strict timing, t1.5 for Modbus RTU
        )

    return server


if __name__ == "__main__":
    print("Modbus server started on localhost port 502")
    asyncio.run(run_async_server())