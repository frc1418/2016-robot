#!/usr/bin/env python3

import wpilib
from wpilib.cantalon import CANTalon
import robotpy_ext
from robotpy_ext.control.button_debouncer import ButtonDebouncer

class MyRobot(wpilib.SampleRobot):
    
    def robotInit(self):
        
        # #INITIALIZE JOYSTICKS##
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)

        
        # #INITIALIZE MOTORS##
        self.lf_motor = wpilib.CANTalon(5)
        self.lr_motor = wpilib.CANTalon(10)
        self.rf_motor = wpilib.CANTalon(15)
        self.rr_motor = wpilib.CANTalon(20)
        
        
        # #SMART DASHBOARD
        
        # #ROBOT DRIVE##
        self.robot_drive = wpilib.RobotDrive(self.lf_motor, self.lr_motor, self.rf_motor, self.rr_motor)

    def disabled(self):
        # self.talon.setSensorPosition(0)
        wpilib.Timer.delay(.01)
    
    def operatorControl(self):
        # self.myRobot.setSafetyEnabled(True)
        reverse = False
        while self.isOperatorControl() and self.isEnabled():
            
            
            reverseButton = ButtonDebouncer(self.joystick1, 1, period=.6)
            if reverseButton.get():
                reverse = not reverse
            if not reverse:    
                self.robot_drive.arcadeDrive(self.joystick1.getY(), self.joystick2.getX())
            else:
                self.robot_drive.arcadeDrive(self.joystick1.getY()*-1, self.joystick2.getX())
            wpilib.Timer.delay(0.005)
            
if __name__ == '__main__':
    wpilib.run(MyRobot)
