import ev3dev.ev3 as ev3
import time
import math

class Motors:
    def __init__(self):
        """
        Initializes odometry module
        """

        # YOUR CODE FOLLOWS (remove pass, please!)
    def drive_forward(self, speed, duration):
        rm = ev3.LargeMotor("outB")
        lm = ev3.LargeMotor("outC")
        rm.reset()
        lm.reset()
        rm.stop_action = "brake"
        lm.stop_action = "brake"
        rm.speed_sp = speed
        lm.speed_sp = speed
        rm.command = "run-forever"
        lm.command = "run-forever"
        time.sleep(duration)
        rm.stop()
        lm.stop()

    def drive_backward(self, speed, duration):

        rm = ev3.LargeMotor("outB")
        lm = ev3.LargeMotor("outC")
        rm.reset()
        lm.reset()
        rm.stop_action = "brake"
        lm.stop_action = "brake"
        rm.speed_sp = (-1)*speed
        lm.speed_sp = (-1)*speed
        rm.command = "run-forever"
        lm.command = "run-forever"
        time.sleep(duration)
        rm.stop()
        lm.stop()

    def turn_left(self, cycle, duration):

        rm = ev3.LargeMotor("outB")
        lm = ev3.LargeMotor("outC")
        rm.reset()
        lm.reset()
        rm.stop_action = "brake"
        lm.stop_action = "brake"
        rm.duty_cycle_sp = cycle
        lm.duty_cycle_sp = (-1) * cycle
        rm.command = "run-direct"
        lm.command = "run-direct"
        time.sleep(duration)
        rm.stop()
        lm.stop()

    def turn_right(self, speed, duration):
        rm = ev3.LargeMotor("outB")
        lm = ev3.LargeMotor("outC")
        rm.reset()
        lm.reset()
        rm.stop_action = "brake"
        lm.stop_action = "brake"
        rm.duty_cycle_sp = (-1)*cycle
        lm.duty_cycle_sp = cycle
        rm.command = "run-direct"
        lm.command = "run-direct"
        time.sleep(duration)
        rm.stop()
        lm.stop()

    def follow_line(self, speed, duration):
        cs = ev3.ColorSensor()#exchange with method
        cs.mode = 'RGB-RAW'
        rm = ev3.LargeMotor("outB")
        lm = ev3.LargeMotor("outC")

        for i in range(0, duration*5):
            right_speed = 0
            left_speed = 0
            r, g, b = cs.bin_data("hhh")
            brightness = math.sqrt(r**2 + g**2 + b**2)
            print("Brightness: " + str(brightness))

            right_speed = 50 + 50*brightness/250
            left_speed = 50 + 50*250/brightness #break condition (for low brightness value too high

            rm.speed_sp = right_speed
            lm.speed_sp = left_speed
            rm.command = "run-forever"
            lm.command = "run-forever"
            time.sleep(0.2)
            i += 1
    def stop(self):
        rm = ev3.LargeMotor("outB")
        lm = ev3.LargeMotor("outC")
        rm.reset()
        lm.reset()
        rm.stop()
        lm.stop()
