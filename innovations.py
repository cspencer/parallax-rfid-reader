#! /usr/bin/env python3

# import RPi.GPIO as GPIO
from functools import reduce
import serial

SERIAL_PORT = '/dev/cu.usbserial-A90808OA'
                              
def validate_rfid(code):
    data = bytes(code)

    # Validate that we have a start transmission byte at byte 1.
    if data[0] != 0x02:
        return False

    # Validate that we have a CRLF at bytes 14 and 15.
    if data[13] != 13 and data[14] != 10:
        return False

    # Validate that we have an end transmission byte at byte 16.
    if data[15] != 0x03:
        return False

    # Extract the RFID string and the checksum.
    check = int(data[11:13], 16)
    rfid  = data[1:11]

    # Compute the checksum on the RFID code.
    valid = reduce(lambda x, y: x ^ y,
                   [ int(rfid[(x * 2):(x * 2) + 2], 16) for x in range(0,5) ])

    # Check the computed checksum against the one read from the string and
    # ensure that they match.
    if valid != check:
        return False

    return rfid.decode("ascii")
    
def main():
    print("Enabling RFID reader...")

    # Set up the serial port as per the Parallax reader's datasheet.
    ser = serial.Serial(baudrate = 9600,
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
            data = ser.read(16)

            # Attempt to validate the data we just read.
            if (len(data) == 16):
                code = validate_rfid(data)

                # If validate_rfid() returned a code, display it.
                if code:
                    print("Read RFID code: " + str(code));
    except Exception as e:
        # If we caught an exception, then disable the reader by setting
        # the pin to HIGH, then exit.
        print("Disabling RFID reader...: ")
        print(e)
        #        GPIO.output(ENABLE_PIN, GPIO.HIGH)

        
if __name__ == "__main__":
    main()

