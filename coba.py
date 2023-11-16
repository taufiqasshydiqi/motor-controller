from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

def run_async_server():
    nreg = 200
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [15]*nreg),
        co=ModbusSequentialDataBlock(0, [16]*nreg),
        hr=ModbusSequentialDataBlock(0, [17]*nreg),
        ir=ModbusSequentialDataBlock(0, [18,20]*nreg)
    )
    context = ModbusServerContext(slaves=store, single=True)

    identity = ModbusDeviceIdentification()
    identity.VendorName = 'bbt'
    identity.ProductCode = 'apaya'
    identity.VendorUrl = "www.bbt.com"
    identity.ProductName = "modbus server bbt"
    identity.ModelName = "modbus server"
    identity.MajorMinorRevision = "3.0.2"
    
    StartTcpServer(context=context, identity=identity, address=('127.0.0.1', 502))

if __name__ == "__main__":
    print("Modbus server started on localhost port 502")
    run_async_server()