#! /usr/bin/env python3

import RPi.GPIO as GPIO
import serial
import time


ENABLE_PIN  = 18              # The BCM pin number corresponding to GPIO1
SERIAL_PORT = '/dev/ttyAMA0'  # The location of our serial port.  This may
                              # vary depending on OS version.


def validate_rfid(code):
    # A valid code will be 12 characters long with the first char being
    # a line feed and the last char being a carriage return.
    s = code.decode("ascii")

    if (len(s) == 12) and (s[0] == "\n") and (s[11] == "\r"):
        # We matched a valid code.  Strip off the "\n" and "\r" and just
        # return the RFID code.
        return s[1:-1]
    else:
        # We didn't match a valid code, so return False.
        return False

    
def main():
    # Initialize the Raspberry Pi by quashing any warnings and telling it
    # we're going to use the BCM pin numbering scheme.
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # This pin corresponds to GPIO1, which we'll use to turn the RFID
    # reader on and off with.
    GPIO.setup(ENABLE_PIN, GPIO.OUT)

    # Setting the pin to LOW will turn the reader on.  You should notice
    # the green LED light on the reader turn red if successfully enabled.

    print("Enabling RFID reader...\n")
    GPIO.output(ENABLE_PIN, GPIO.LOW)

    # Set up the serial port as per the Parallax reader's datasheet.
    ser = serial.Serial(baudrate = 2400,
                        bytesize = serial.EIGHTBITS,
                        parity   = serial.PARITY_NONE,
                        port     = SERIAL_PORT,
                        stopbits = serial.STOPBITS_ONE,
                        timeout  = 1)

    # Wrap everything in a try block to catch any exceptions.
    try:
        # Loop forever, or until CTRL-C is pressed.
        while 1:
            # Read in 12 bytes from the serial port.
            data = ser.read(12)

            # Attempt to validate the data we just read.
            code = validate_rfid(data)

            # If validate_rfid() returned a code, display it.
            if code:
                print("Read RFID code: " + code);
                time.sleep(1)
    except:
        # If we caught an exception, then disable the reader by setting
        # the pin to HIGH, then exit.
        print("Disabling RFID reader...")
        GPIO.output(ENABLE_PIN, GPIO.HIGH)

        
if __name__ == "__main__":
    main()

