# Using Adafruit Bluefruit Connect phone app to tele-operate the Picobot 
This project is similar to the [PicoBot TeleOperation using a pair of HC-05 / HC-06 BT modules](https://github.com/dblanding/Picobot_joy_HC-05) project, but uses the [Adafruit Bluefruit LE Connect](https://learn.adafruit.com/bluefruit-le-connect/ios-setup) phone app instead of a physical joystick.
* The HC-05 / HC-06 BT modules are no longer needed.
* The physical joystick is no longer needed.
* The phone itself is the joystick.
* When the phone is tipped and tilted, the app sends accelerometer data to the Picobot over BLE.
* An [Adafruit Bluefruit LE UART Friend](https://www.adafruit.com/product/2479) onboard the Picobot receives the "joystick commands".
* The joystick commands are then converted to Picobot driving commands.

