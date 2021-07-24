# What is this

serialkey is a simple python3 program that allows typing on a virtual ASCII keyboard and having the appropriate key down/key up events sent over serial.  It was designed for entering keystrokes on Apple II computers so currently its features are geared toward that retro platform.

Currently it is designed to work with the Hagstrom Electronics [https://www.hagstromelectronics.com](https://www.hagstromelectronics.com/index.php) USB-ASC232 and USBtoUSB in "keynumber mode", but support of the Raspberry Pi W/4B in USB gadget mode (as a keyboard) is planned.





## How to install

Clone the repository.  
Edit *serialkey_config.py* for the serial port designation for your USB-ASC232 or USBtoUSB device, and baud rate that you have configured your device for (see the manual for the device). 

Requirements: pyserial

Possibly requires installing [unicurses](https://github.com/unicurses/unicurses.git).

## How to use

* Launch serialkey : *python3 serialkey.py*
* Typed keys should flash on the keyboard and the keycodes sent through serial --> to USB --> the remote computer.  
* Capture of modifier keys is not currently supported so there are latched keys to workaround:
	* ^A - Enables/Disables Apple
	* ^B - Enables/Disables Solid Apple/Option
	* ^C - Kills the program, don't type this unless you want to
	* ^D - Enables/Disables Control
* ^] Key brings up an options menu of special functions
* Mousekeys mode (forward Del key) enables mousekeys in GS/OS gui apps and causes numbers to send number pad keycodes instead

## Should I use?!
This is alpha software code, and not and example of how *to* code.  What do *you* think? :)  Of course there isn't much trouble you can get into sending bytes through a USB to serial device, unless you type something that your Apple ][ on the other end isn't happy to hear...  

This was intended as a quick way to send keys to an Apple ][ (with appropriate hardware to receive USB keystrokes), and its nature allows other apps on a modern computer to simply redirect text to the window running serialkey, or allow copy and paste of text directly into the window.  It also allows for mostly complete control of the Apple II's keyboard directly from a remote location, as long as you can ssh/desktop share/etc into the modern computer hosting serialkey.  But it's not particularly convenient for replacing a real USB keyboard for every day use.

The next planned feature is customization for controlling the USB sync controller devices - some may have different hotkeys than mine.  Also, finishing support for the Raspberry Pi's gadget mode is high priority as they are probably easier to obtain and have more function for the money.  And they may have greater compatibility with USB host devices on the other end.