'''
Main Robot Code 2019-02-23


'''

import RPi.GPIO as GPIO
import sys

from time       import sleep
from bluedot    import BlueDot
from signal     import pause

global OUTPUT, INPUT, PUP, PDWN, BTdeviceName, BTdeviceMAC
OUTPUT = GPIO.OUT
INPUT = GPIO.IN
PUP = RPIO.PUD_UP
PDWN = RPIO.PUD_DOWN

BTdeviceName = 'OnePlus 6'
BTdeviceMAC =  '64:A2:F9:2F:6A:9B' #'1C:AF:05:22:FE:43'


class DriveController():
    __instance = None

    @staticmethod
    def getInstance():
        if DriveController.__instance is None:
            DriveController()
        return DriveController.__instance

    def __init__(self):
        if DriveController.__instance is not None:
            raise Exception('InstanceError!')
        else:
            DriveController.__instance = self

        self._command = None
        self.running = False
        self.throttleL = 0
        self.throttleR = 0

        self.forward = None
        self.backwards = None




    def getCommand(self, cObj):
        self._command = cObj

    def handleCommand(self):
        
        if (self._command is not None):
            self.running = True

            distance = self._command.distance

            if (self._command.x < 0): # left turn
                self.throttleL = (distance - abs(self._command.x))*100
                self.throttleR = distance*100
            elif (self._command.x > 0): # right turn
                self.throttleL = distance*100
                self.throttleR = (distance - abs(self._command.x))*100

            if (self._command.y < 0): # backwards
                self.forward = False
                self.backwards = True
            elif (self._command.y > 0): # forward
                self.forward = True
                self.backwards = False

            if (self.throttleL > 100):
                self.throttleL = 100

            if (self.throttleR > 100):
                self.throttleR = 100

            if (self.throttleL < 0):
                self.throttleL = 0

            if (self.throttleR < 0):
                self.throttleR = 0


        elif (self._command is None):
            self.throttleL = 0
            self.throttleR = 0
            self.forward = None
            self.backwards = None

        self.running = False



    def setThrottle(self, MotorObjL, MotorObjR):
        MotorObjL.throttle = self.throttleL
        MotorObjR.throttle = self.throttleR

        # print('Throttle Left:', MotorObjL.throttle, 'Throttle Right', MotorObjR.throttle )



    def getSensorData(self):
        pass




class DCMotor:
    """docstring for DCMotor"""

    def __init__(self, pinList):
        self._pins      = {     'en'    : pinList[0],
                                'in1'   : pinList[1],
                                'in2'   : pinList[2],
                            }

        self.throttle   = 0     # %
        self._freq      = 200   # Hz 

        GPIO.setup(pinList, OUTPUT)
        self._p = GPIO.PWM(self._pins['en'], self._freq)
        print('initialized ->', self._pins)



    def drive_cw(self):
        self._p.start(self.throttle)
        # GPIO.PWM(self._pins['en'], self.throttle)
        GPIO.output(self._pins['in1'], True)
        GPIO.output(self._pins['in2'], False)


    def drive_ccw(self):
        self._p.start(self.throttle)
        # GPIO.PWM(self._pins['en'], self.throttle)
        GPIO.output(self._pins['in1'], False)
        GPIO.output(self._pins['in2'], True)

    #### TO BE TESTED
    # PWM or digitial?
    def idle(self):
        GPIO.output(self._pins['en'], False)


    def stop(self):
        self._p.stop()
        GPIO.output(self._pins['in1'], False)
        GPIO.output(self._pins['in2'], False)


class BTControllerEvent:

    def movedDot(position):
        if (not DriveController.getInstance().running):
            DriveController.getInstance().getCommand(position)
        print('moved')

    def releasedDot(position):
        if (not DriveController.getInstance().running):
            DriveController.getInstance().getCommand(None)
        print('released')

    def pressedDot(position):
        if (not DriveController.getInstance().running):
            DriveController.getInstance().getCommand(position)
        print('pressed')


def reset_pin(pins):
    print('\nreset pins')
    for number in pins:
        GPIO.output(number, False)


''' 
MAIN PROGRAM 



'''

pBT_status = 14

if __name__ == '__main__':
    try:
        print('\n#####################')
        print('setting up hardware..')
        GPIO.setmode(GPIO.BCM)

        # init bluetooth LED
        GPIO.setup(pBT_status, OUTPUT, pull_up_down=PDWN)

        # init DC motors
        motorL = DCMotor(   pinList = [
                                    12,     # enA
                                    20,     # in1
                                    16,     # in2
                                    ])
        motorR = DCMotor(   pinList = [
                                    13,     # enB
                                    26,     # in3
                                    19,     # in4
                                    ])

        reset_pin([
            12, 20, 16,     # left motor
            13, 26, 19,     # right motor
            pBT_status,     # BT status LED
            ])


        print('\n###############')
        print('establish connection with controller..')
        bd = BlueDot()

        print('connect one of the following devices: \n', bd.paired_devices)

        if (bd.wait_for_connection()):
            print('connection succeeded!')

        bd.when_released = BTControllerEvent.releasedDot
        bd.when_pressed = BTControllerEvent.pressedDot
        bd.when_moved = BTControllerEvent.movedDot

        controller = DriveController()
        print('\n###############')
        print('robot setup done!')


        while bd.wait_for_connection():

            GPIO.output(pBT_status, bd.is_connected)

            controller.handleCommand()
            controller.setThrottle(motorL, motorR)

            if controller.forward:
                motorL.drive_ccw()
                motorR.drive_cw()
            elif controller.backwards:
                motorL.drive_cw()
                motorR.drive_ccw()
            elif (controller.forward is None) and (controller.backwards is None):
                motorL.stop()
                motorR.stop()

        print('programm ended!')


    except KeyboardInterrupt:
        reset_pin([
            12, 20, 16,     # left motor
            13, 26, 19      # right motor
            pBT_status,     # BT status LED
            ])

    finally:
        GPIO.cleanup()



