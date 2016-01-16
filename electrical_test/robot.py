#! /usr/bin/env python3
import wpilib
import enum

from networktables import NetworkTable
from wpilib import cantalon

class Swerve(enum.IntEnum):
    DRIVE = 0
    ROTATE = 1
    
class MyRobot(wpilib.SampleRobot):
    
    def robotInit(self):
        self.sd = NetworkTable.getTable('SmartDashboard')
        

        # #INITIALIZE JOYSTICKS##
        self.joystick1 = wpilib.Joystick(0)
        
        
        
        # #INITIALIZE MOTORS##
        self.lf_wheel = wpilib.CANTalon(5)
        self.lr_wheel = wpilib.CANTalon(10)
        self.rf_wheel = wpilib.CANTalon(15)
        self.rr_wheel = wpilib.CANTalon(20)
        
        
    def disabled(self):
        # self.talon.setSensorPosition(0)
        wpilib.Timer.delay(.01)
    
    def operatorControl(self):
        # self.myRobot.setSafetyEnabled(True)
        
        while self.isOperatorControl() and self.isEnabled():
        
            self.lf_wheel.set(self.joystick1.getRawButton(1))
            
            #Make this wheel 5. So record the wheel this turns and which CANTalon is hooked up to this wheel. Swap
            self.lr_wheel.set(self.joystick1.getRawButton(2))
            self.rf_wheel.set(self.joystick1.getRawButton(3))
            self.rr_wheel.set(self.joystick1.getRawButton(4))
        
            
            wpilib.Timer.delay(0.005)
if __name__ == '__main__':
    wpilib.run(MyRobot)
