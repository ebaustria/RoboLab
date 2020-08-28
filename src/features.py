import ev3dev.fonts as fonts

from ev3dev.ev3 import *
from time import sleep
from threading import Thread


def start_features(robot):
    Thread(target=run_display, args=(robot,)).start()
    Thread(target=run_wings, args=(robot,)).start()


def run_display(robot):
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

    while robot.running:
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


def run_wings(robot):
    motor = MediumMotor("outA")

    running = False
    motor.stop_action = "brake"
    motor.command = "run-forever"
    motor.speed_sp = 200

    #while robot.running:
    #    sleep(2)
     #   pass
    """if not running and robot.counter == 0:
        motor.stop_action = "brake"
        motor.command = "run-forever"
        motor.speed_sp = 50
        running = True
    elif running and robot.counter != 0:
        motor.stop()
        running = False"""
    #motor.stop()
