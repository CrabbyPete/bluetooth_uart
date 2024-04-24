import serial
import logging
import asyncio
import threading

from typing import Any, Dict, Union

from bless import ( BlessServer,
                    BlessGATTCharacteristic,
                    GATTCharacteristicProperties,
                    GATTAttributePermissions )

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(name=__name__)


trigger = asyncio.Event()

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

uart = serial.Serial("/dev/ttyS0", baudrate=9600)


def read_request(characteristic: BlessGATTCharacteristic, **kwargs) -> bytearray:
    logger.debug(f"Reading {characteristic.value}")
    return characteristic.value


def write_request(characteristic: BlessGATTCharacteristic, value: Any, **kwargs):
    characteristic.value = value
    logger.debug(f"Char value set to {characteristic.value}")
    uart.write(value)

async def run(loop):
    def read_uart(server):
        while True:
            char = uart.read(1)
            server.get_characteristic(UART_TX_CHAR_UUID).value = char
            server.update_value(UART_SERVICE_UUID, UART_TX_CHAR_UUID )

    trigger.clear()

    # Instantiate the server
    gatt: Dict = {
        UART_SERVICE_UUID: {
            UART_RX_CHAR_UUID: {
                "Properties": (
                        GATTCharacteristicProperties.write
                        | GATTCharacteristicProperties.indicate
                ),
                "Permissions": (GATTAttributePermissions.writeable),
                "Value": None,
            },
            UART_TX_CHAR_UUID: {
                "Properties": (
                        GATTCharacteristicProperties.read
                        | GATTCharacteristicProperties.indicate
                ),
                "Permissions": (GATTAttributePermissions.readable),
                "Value": None,
            }
        }}
    server = BlessServer(name="rpi-gatt-uart", loop=loop)
    server.read_request_func = read_request
    server.write_request_func = write_request

    await server.add_gatt(gatt)
    await server.start()

    thread = threading.Thread(target=read_uart, args=(server,))
    thread.start()

    logger.debug("Advertising")
    await trigger.wait()

    await asyncio.sleep(2)
    await server.stop()


loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))