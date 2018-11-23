import time
import RPi.GPIO as GPIO

KEYPAD = [
    ["4", "8", "12", "16"],
    ["3", "7", "11", "15"],
    ["1", "5",  "9", "13"],
    ["2", "6", "10", "14"]
]

GRID = ["0", "0", "0", "0","0", "0", "0", "0","0", "0", "0", "0","0", "0", "0", "0"]

ROW = [7,11,13,15]

COL = [12,16,18,22]

GPIO.setmode(GPIO.BCM)

def print_grid():
    print('\033[2J')
    for i in range(4):
        print('%s%s%s%s' % (GRID[i*4], GRID[i*4+1], GRID[i*4+2], GRID[i*4+3]))

for j in range(4):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j], 1)

for i in range(4):
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

try:
    while(True):
        for j in range(4):
            GPIO.output(COL[j], 0)
            for i in range(4):
                if GPIO.input(ROW[i]) == 0:
                    key = int(KEYPAD[i][j])
                    GRID[key-1] = "."
                    print_grid()
                    time.sleep(0.5)
            GPIO.output(COL[j], 1)
except KeyboardInterrupt:
    GPIO.cleanup()
