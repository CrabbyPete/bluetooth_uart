import sys
import asyncio

from typing    import Iterator
from itertools import count, takewhile

from bleak     import BleakScanner, BleakClient, BleakGATTCharacteristic

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

# TIP: you can get this function and more from the ``more-itertools`` package.
def sliced(data: bytes, n: int) -> Iterator[bytes]:
    """
    Slices *data* into chunks of size *n*. The last slice may be smaller than
    *n*.
    """
    return takewhile(len, (data[i : i + n] for i in count(0, n)))


async def main():


    def handle_disconnect(_: BleakClient):
        print("Device was disconnected, goodbye.")
        # cancelling all tasks effectively ends the program
        for task in asyncio.all_tasks():
            task.cancel()

    def handle_rx(_: BleakGATTCharacteristic, data: bytearray):
        print("received:", data)

    devices = await BleakScanner.discover(timeout=30.0)
    for d in devices:
        if d.name == 'raspberrypi':
            async with BleakClient(d.address, timeout=30.0) as client:
                await client.start_notify(UART_TX_CHAR_UUID, handle_rx)
                print("Connected, start typing and press ENTER...")

                nus = client.services.get_service(UART_SERVICE_UUID)
                rx_char = nus.get_characteristic(UART_RX_CHAR_UUID)

                while True:
                    data = "This is a test of bluetooth\r\n"

                    # Writing without response requires that the data can fit in a
                    # single BLE packet. We can use the max_write_without_response_size
                    # property to split the data into chunks that will fit.
                    await client.write_gatt_char(rx_char, data.encode(), response=True)

                    print("sent:", data)
        else:
            print(d)


asyncio.run(main())