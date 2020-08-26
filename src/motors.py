import ev3dev.ev3 as ev3
import time
import math

from odometry import Odometry #new

class Motors:
    def __init__(self):
        self.rm = ev3.LargeMotor("outB")
        self.lm = ev3.LargeMotor("outC")
        #self.robot = robot

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
    def follow_line(self, duration, myColorSensor, myOdometry, ticks_previous_l, ticks_previous_r): #myOdometry new
        r, g, b = myColorSensor.get_colors()
        previous_brightness = math.sqrt(r**2 + g**2 + b**2) # for D-Controller
        #previous_error_d = 0
        right_speed = 0
        left_speed = 0




        for i in range(0, int(duration*10)):
            #Odometry: coordinates(ticks) to default 0
            #myOdometry.reset_position()

            r, g, b = myColorSensor.get_colors()
            brightness = math.sqrt(r**2 + g**2 + b**2)



            multiplicator_p = 0.4#??? 0.57   0.4
            multiplicator_d = 0.2#??? 0.8 0.1
            #multiplicator_d = 0.1

            error_p = brightness - 350
            error_d = brightness - previous_brightness#error - previous_error_p
            #error_d = error_d-previous_error_d
            turn = multiplicator_p*error_p + multiplicator_d*error_d#(change y)/(change x)*error


            #maybe I-Controller instead

            if 150 < brightness <= 450:
                offset = 200
            else:
                offset = 150

            #offset = 200

            right_speed = offset + turn
            left_speed = offset - turn
            self.rm.speed_sp = right_speed
            self.lm.speed_sp = left_speed
            self.rm.command = "run-forever"
            self.lm.command = "run-forever"

            time.sleep(duration/10)

            previous_brightness = brightness
            #previous_error_d = error_d

            ticks_l, ticks_r = myOdometry.get_position()
            myOdometry.add_point(((ticks_l-ticks_previous_l),(ticks_r-ticks_previous_r)))
            ticks_previous_l = ticks_l
            ticks_previous_r = ticks_r

        return ticks_previous_l, ticks_previous_r

    #done
    def stop(self):
        self.rm.reset()
        self.lm.reset()
        self.rm.stop()
        self.lm.stop()


    def turn_angle(self, speed, angle):

        self.rm.position_sp = -angle * 2 #2 for speed = 100 (2.2 calculated and tested?)
        self.lm.position_sp = angle * 2 #for one rotation -> wheels 2.2 rotations
        self.rm.speed_sp = speed
        self.lm.speed_sp = speed
        self.rm.command = "run-to-rel-pos"
        self.lm.command = "run-to-rel-pos"
        #time.sleep(duration)#wait.until?
        self.rm.wait_until_not_moving()

    def detect_nodes(self, speed, cs):#new (25.08)
        nodes = []
        odometry = Odometry(self.lm, self.rm)
        odometry.reset_position()
        self.rm.position_sp = 360*2
        self.lm.position_sp = -360*2
        self.rm.speed_sp = speed
        self.lm.speed_sp = speed
        self.rm.command = "run-to-rel-pos"
        self.lm.command = "run-to-rel-pos"
        while self.rm.is_running:
            if cs.get_brightness() < 200:
                #odometry.add_point(odometry.get_position())
                #_, _, gamma, _ = odometry.calculate_values()
                #nodes.append(gamma)
                nodes.append(self.rm.position/2)
        return nodes

    def turn_until_path_found(self, speed, cs):
        odometry = Odometry(self.lm, self.rm)
        odometry.reset_position()
        self.rm.position_sp = 360 * 2
        self.lm.position_sp = -360 * 2
        self.rm.speed_sp = speed
        self.lm.speed_sp = speed
        self.rm.command = "run-to-rel-pos"
        self.lm.command = "run-to-rel-pos"
        while self.rm.is_running:
            if cs.get_brightness() < 200:
                self.stop()



    #done
    def drive_in_center_of_node(self, speed, duration, odometry):
        self.stop()
        previous_ticks_l, previous_ticks_r = odometry.get_position()
        self.drive_forward(speed, duration)
        ticks_l, ticks_r = odometry.get_position()
        odometry.add_point((ticks_l-previous_ticks_l, ticks_r-previous_ticks_r))
        self.stop()

    #done
    def get_motors(self):
        return self.lm, self.rm


