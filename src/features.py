from ev3dev.ev3 import *
from time import sleep
import ev3dev.fonts as fonts


def run_display():
    lcd = Screen()
    lcd.clear()

    lcd.draw.rectangle((45, 70, 55, 90), fill='black')
    lcd.draw.rectangle((55, 40, 65, 50), fill='black')
    lcd.draw.rectangle((55, 60, 65, 110), fill='black')
    lcd.draw.rectangle((65, 50, 75, 70), fill='black')
    lcd.draw.rectangle((65, 80, 115, 100), fill='black')
    lcd.draw.rectangle((65, 110, 85, 120), fill='black')
    lcd.draw.rectangle((75, 60, 105, 80), fill='black')
    lcd.draw.rectangle((95, 110, 115, 120), fill='black')
    lcd.draw.rectangle((105, 50, 115, 70), fill='black')
    lcd.draw.rectangle((115, 40, 125, 50), fill='black')
    lcd.draw.rectangle((115, 40, 125, 50), fill='black')
    lcd.draw.rectangle((115, 60, 125, 110), fill='black')
    lcd.draw.rectangle((125, 70, 135, 90), fill='black')

    lcd.draw.text((20, 5), 'ROBOLAB 2020', font=fonts.ImageFont.truetype("/home/robot/src/assets/Roboto-Regular.ttf", 20))

    while True:
        lcd.draw.rectangle((35, 80, 45, 110), fill='white')
        lcd.draw.rectangle((135, 80, 145, 110), fill='white')

        lcd.draw.rectangle((35, 50, 45, 80), fill='black')
        lcd.draw.rectangle((135, 50, 145, 80), fill='black')

        lcd.update()
        sleep(1)

        lcd.draw.rectangle((35, 50, 45, 80), fill='white')
        lcd.draw.rectangle((135, 50, 145, 80), fill='white')

        lcd.draw.rectangle((35, 80, 45, 110), fill='black')
        lcd.draw.rectangle((135, 80, 145, 110), fill='black')

        lcd.update()
        sleep(1)
