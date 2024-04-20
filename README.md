# bluetooth_uart
Create a bluetooth uart and send results to the minor uart on the Raspberry Pi Zero W 

main.py is code run on the Mac to look for the device called raspberrypi. Once it connect
via bluetooth it will start to send test strings

The directory Pi contains the code to run on the raspberry pi zero, to create the UART
service. uart-server.py sends what text string it gets to the minor port ( the UART port using
GPIO 14(tx) and GPIO15(rx))

Install instructions for the Raspberry Pi using Raspbian(Bullseye)

1. sudo apt install git
2. git clone https://github.com/CrabbyPete/bluetooth_uart.git
3. cd bluetooth_uart/pi
4. sudo apt install python3-pip
5. sudo apt install python3-dbus
6. sudo raspi-config
   1. select interface options
   2. Would you like a login shell to be accessible over serial? No
   3. Would you like the serial port hardware to be enabled? Yes
   4. You should see.
        The serial login shell is disabled                       
        The serial interface is enabled
   5. When you exit it will ask to reboot. Yes
7. After the Pi reboots login again and return to the pi directory
8. python3 uart-server.py
   The code should display
   Skip adapter: /org/bluez
   GATT application registered
   GetAll
   returning props
   Advertisement registered


You can use an app such as BT Scanner or BT Inspector and the Pi will show up as the
same name as the WiFi network or 'rpi-gatt-server'

If the app allows it you can connect, and send text the device
You can also connect an FTDI (https://microcontrollerslab.com/ftdi-usb-to-serial-converter-cable-use-linux-windows/)
and connect to pin 14(tx) and pin 15(rx) and view the text being sent.

On a Mac, you can test as follows
1. create a python venv using python3 -m venv bluetooth_uart
2. cd bluetooth_uart
3. git clone https://github.com/CrabbyPete/bluetooth_uart.git
4. pip3 install bleak
5. cd bluetooth_uart
6. python3 main.py

if the code exits and does not dispay your device, check line 35
and make sure you device is here
    if d.name in ('raspberry','rpi-gatt-server'):
change 'raspberry' to what your network shows as



   
   