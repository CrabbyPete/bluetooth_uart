# bluetooth_uart
Create a bluetooth uart and send results to the minor uart on the Raspberry Pi Zero W 
The primary UART on the Pi is the bluetooth adapter, the minor port is the USB or GPIO 14(tx)
and GPIO 15(rx). blu_uart.py is the server code that acts as a proxy sending everything it gets 
ts from the bluetooth uart to /dev/ttyS0 which is the UART defined by the pins, or the USB

console.py is code run on the Mac. It will prompt for
any input from the terminal and send it to the server. It will also return character by character
anything coming from the uart on the Pi

The blu_uart.py is the server code runs on the raspberry pi zero, to create the UART
service. blu_uart.py sends what text string it gets to the minor port and returns any characters it gets back to console.py running on the mac

Install instructions for the Raspberry Pi using Raspbian

1. sudo apt install git
2. sudo apt install python3-pip
3. sudo raspi-config
   1. select interface options
   2. Would you like a login shell to be accessible over serial? No
   3. Would you like the serial port hardware to be enabled? Yes
   4. You should see.
        The serial login shell is disabled                       
        The serial interface is enabled
   5. When you exit it will ask to reboot. Yes
4. After the Pi reboots login again and return to the pi directory
5. python3 -m venv bluetooth_uart
6. cd bluetooth_uart
7. . bin/activate
8. git clone https://github.com/CrabbyPete/bluetooth_uart.git
9. pip install -r requirements.txt
10. python3 blu_uart.py
11. Enter text on the console 

You can use an app such as BT Scanner or BT Inspector and the Pi will show up as the
same name as the WiFi network or 'rpi-gatt-uart'

If the app allows it you can connect, and send text the device
You can also connect an FTDI (https://microcontrollerslab.com/ftdi-usb-to-serial-converter-cable-use-linux-windows/)
and connect to pin 14(tx) and pin 15(rx) and view the text being sent, using minicom or screen on
the Mac console

On a Mac, you can test as follows
1. create a python venv using python3 -m venv bluetooth_uart
2. cd bluetooth_uart
3. git clone https://github.com/CrabbyPete/bluetooth_uart.git
4. pip install bleak
5. pip install bless
6. cd bluetooth_uart
7. python3 console.py






   
   