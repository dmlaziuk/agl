#!/usr/bin/python3

import RPi.GPIO as GPIO
import os, time, signal, sys
from time import localtime, strftime, sleep
from datetime import datetime, timedelta


class LCD:
    def __init__(self, pin_rs=4, pin_e=15, pins_db=[9, 11, 7, 8]):
        self.pin_rs=pin_rs
        self.pin_e=pin_e
        self.pins_db=pins_db

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_e, GPIO.OUT)
        GPIO.setup(self.pin_rs, GPIO.OUT)
        for pin in self.pins_db:
            GPIO.setup(pin, GPIO.OUT)

        self.clear()

    def clear(self):
        self.cmd(0x33) # $33 8-bit mode
        self.cmd(0x32) # $32 8-bit mode
        self.cmd(0x28) # $28 8-bit mode
        self.cmd(0x0C) # $0C 8-bit mode
        self.cmd(0x06) # $06 8-bit mode
        self.cmd(0x01) # $01 8-bit mode

    def cmd(self, bits, char_mode=False):
        sleep(0.001)
        bits=bin(bits)[2:].zfill(8)

        GPIO.output(self.pin_rs, char_mode)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i], True)

        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4,8):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i-4], True)


        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

    def message(self, text, line):
        if line == 1:
            self.cmd(0x80)
        elif line == 2:
            self.cmd(0xC0)
        elif line == 3:
            self.cmd(0x90)
        elif line == 4:
            self.cmd(0xD0)

        for char in text:
            self.cmd(ord(char),True)


if __name__ == '__main__':

    KEYPAD = [
        ["4", "8", "12", "16"],
        ["3", "7", "11", "15"],
        ["2", "6", "10", "14"],
        ["1", "5",  "9", "13"]
    ]

    GRID = ["0", "0", "0", "0","0", "0", "0", "0","0", "0", "0", "0","0", "0", "0", "0"]

    ROW = [6,13,19,26]

    COL = [12,16,20,21]

    lcd = LCD()

    def signal_handler(signal, frame):
        GPIO.cleanup()
        sys.exit(0)

    def print_grid():
        print('\033[2J')
        for i in range(4):
            lcd.message('%s%s%s%s' % (GRID[i*4], GRID[i*4+1], GRID[i*4+2], GRID[i*4+3]), i+1)
            print('%s%s%s%s' % (GRID[i*4], GRID[i*4+1], GRID[i*4+2], GRID[i*4+3]))

    signal.signal(signal.SIGINT, signal_handler)


    for j in range(4):
        GPIO.setup(COL[j], GPIO.OUT)
        GPIO.output(COL[j], 1)

    for i in range(4):
        GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

    while True:
        for j in range(4):
            GPIO.output(COL[j], 0)
            for i in range(4):
                if GPIO.input(ROW[i]) == 0:
                    key = int(KEYPAD[i][j])
                    GRID[key-1] = "."
                    print_grid()
                    time.sleep(0.3)
            GPIO.output(COL[j], 1)