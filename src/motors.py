import ev3dev.ev3 as ev3
import time
import math
from sensors import ColorSensor
from odometry import Odometry
from robot import Robot

class Motors:
    def __init__(self, robot: Robot):
        self.rm = ev3.LargeMotor("outB")
        self.lm = ev3.LargeMotor("outC")
        self.robot = robot

    #in progress (all commands necessary? better command than "run-forever"?)
    def drive_forward(self, speed, duration):
        self.rm.reset()
        self.lm.reset()
        self.rm.stop_action = "brake"
        self.lm.stop_action = "brake"
        self.rm.speed_sp = speed
        self.lm.speed_sp = speed
        self.rm.command = "run-forever"
        self.lm.command = "run-forever"
        time.sleep(duration)
        self.rm.stop()
        self.lm.stop()

    #done
    def drive_backward(self, speed, duration):
        self.drive_forward(-speed, duration)

    ''''#in progress
    def turn_left(self, cycle, duration):
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
    #in progress
    def turn_right(self, speed):
        rm = ev3.LargeMotor("outB")
        lm = ev3.LargeMotor("outC")
        rm.reset()
        lm.reset()
        rm.stop_action = "brake"
        lm.stop_action = "brake"
        rm.position_sp = 360
        lm.position_sp = -360
        rm.speed_sp = speed
        lm.speed_sp = speed
        rm.command = "run-to-rel-pos"
        lm.command = "run-to-rel-pos"

        print("Drehung 1 r: " + rm.state.__repr__())
        print("Drehung 1 l: " + lm.state.__repr__())
        time.sleep(10)
        print("Drehung 2: r" + rm.state.__repr__())
        print("Drehung 2: l" + lm.state.__repr__())
        #rm = ev3.LargeMotor("outB")
        #lm = ev3.LargeMotor("outC")
        #rm.reset()
        #lm.reset()
        #rm.stop_action = "brake"
        #lm.stop_action = "brake"
        #rm.duty_cycle_sp = (-1)*cycle
        #lm.duty_cycle_sp = cycle
        #rm.command = "run-direct"
        #lm.command = "run-direct"
        #time.sleep(duration)
        #rm.stop()
        #lm.stop()
        '''

    #in progress (PID-Controller)
    def follow_line(self, duration, myColorSensor, myOdometry): #myOdometry new
        r, g, b = myColorSensor.get_colors()
        previous_brightness = math.sqrt(r**2 + g**2 + b**2) # for D-Controller
        right_speed = 0
        left_speed = 0
        multiplier = 1 # for D-Controller

        for i in range(0, int(duration*10)):
            #Odometry: coordinates(ticks) to default 0
            myOdometry.reset_position()

            r, g, b = myColorSensor.get_colors()
            brightness = math.sqrt(r**2 + g**2 + b**2)

            #original speed
            #right_speed = multiplier*(50 + 50*brightness/250)
            #left_speed = multiplier*(50 + 50*250/brightness) #break condition (for low brightness value too high

            #linear speed
            #right_speed = 150 - 100 * (1 - (brightness / 350))
            #left_speed = 150 + 100 * (1 - (brightness / 350)) 75/dif

            #another linear speed with multiplier
            #right_speed = multiplier * (150 - 100 * (1 - (brightness / 350)))
            #left_speed = multiplier * (150 + 100 * (1 - (brightness / 350)))

            #print("right speed: " + str(right_speed))
            #print("left speed: " + str(left_speed))

            #PD-Line-Follower (newest try)
            error = brightness - 350
            turn = 30/70*error#(change y)/(change x)*error

            correction = 0.7
            #multiplier = (brightness - previous_brightness)*correction #negative if darker
            multiplier = 0 #just for test
            #print("Multiplier: " + str(multiplier))

            right_speed = 200 + turn - multiplier
            left_speed = 200 - turn + multiplier

            self.rm.speed_sp = right_speed
            self.lm.speed_sp = left_speed
            self.rm.command = "run-forever" #other mode?
            self.lm.command = "run-forever"

            time.sleep(duration/10)

            previous_brightness = brightness

            #ticks_l, tick_r = myOdometry.get_position()
            myOdometry.add_point(myOdometry.get_position())

    #done
    def stop(self):
        self.rm.reset()
        self.lm.reset()
        self.rm.stop()
        self.lm.stop()

    #not a good solution
    #not used
    #just for test
    def turn_left_wheel_revolutions(self, speed, revolutions, duration):

        self.rm.reset()
        self.lm.reset()
        self.rm.stop_action = "brake"
        self.lm.stop_action = "brake"

        self.rm.position_sp = 360 * revolutions
        self.lm.position_sp = -360 * revolutions
        self.rm.speed_sp = speed
        self.lm.speed_sp = speed
        self.rm.command = "run-to-rel-pos"
        self.lm.command = "run-to-rel-pos"
        time.sleep(duration)
        self.rm.stop()
        self.lm.stop()

    def turn_angle(self, speed, angle, duration):

        self.rm.position_sp = angle * 2 #2 for speed = 100 (2.2 calculated and tested?)
        self.lm.position_sp = (-1) * angle * 2 #for one rotation -> wheels 2.2 rotations
        self.rm.speed_sp = speed
        self.lm.speed_sp = speed
        self.rm.command = "run-to-rel-pos"
        self.lm.command = "run-to-rel-pos"
        time.sleep(duration)#wait.until?

    #done
    def drive_in_center_of_node(self, speed, duration):
        self.stop()
        self.drive_forward(speed, duration)
        self.stop()

    #done
    def get_motors(self):
        return self.lm, self.rm


