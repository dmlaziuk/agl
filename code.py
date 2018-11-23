import RPi.GPIO as GPIO

KEYPAD = [
    ["4", "8", "12", "16"],
    ["3", "7", "11", "15"],
    ["1", "5",  "9", "13"],
    ["2", "6", "10", "14"]
]




ROW = [7,11,13,15]

COL = [12,16,18,22]

GPIO.setmode(GPIO.BCM)

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
                    print(KEYPAD[i][j])
            GPIO.output(COL[j], 1)
except KeyboardInterrupt:
    GPIO.cleanup()
