# bluetooth_uart
Create a bluetooth uart and send results to the minor uart on the Raspberry Pi Zero W 

main.py is code run on the Mac to look for the device called raspberrypi. Once it connect
via bluetooth it will start to send test strings

The directory Pi contains the code to run on the raspberry pi zero, to create the UART
service. uart-server.py sends what text string it gets to the minor port ( the UART port using
GPIO 14(tx) and GPIO15(rx))