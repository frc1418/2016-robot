#!/usr/bin/env python3

import wpilib
from wpilib.cantalon import CANTalon

class MyRobot(wpilib.SampleRobot):
    
    def robotInit(self):
        
        # #INITIALIZE JOYSTICKS##
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)

        
        # #INITIALIZE MOTORS##
        self.lf_motor = wpilib.Talon(0)
        self.lr_motor = wpilib.Talon(1)
        self.rf_motor = wpilib.Talon(2)
        self.rr_motor = wpilib.Talon(3)
        
        
        # #SMART DASHBOARD
        
        # #ROBOT DRIVE##
        self.robot_drive = wpilib.RobotDrive(self.lf_motor, self.lr_motor, self.rf_motor, self.rr_motor)
        #self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kFrontLeft, True)
        #self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kRearLeft, True)

    def disabled(self):
        # self.talon.setSensorPosition(0)
        wpilib.Timer.delay(.01)
    
    def operatorControl(self):
        # self.myRobot.setSafetyEnabled(True)
        
        while self.isOperatorControl() and self.isEnabled():    
            
            '''
            wpilib.SmartDashboard.putNumber('Enc', self.toteMotor.getEncPosition())
            
            if wpilib.SmartDashboard.getNumber('P') is not self.talon.getP():
                self.talon.setP(wpilib.SmartDashboard.getNumber('P'))
            
            position = (wpilib.SmartDashboard.getNumber('Dist')*1440)/5.75
            canPosition = (wpilib.SmartDashboard.getNumber('Dist')*1440)/9.625
            self.talon.set(wpilib.SmartDashboard.getNumber('Pos')*-1)
            #self.XOfRobot=self.XOfRobot+(self.accelerometer.getX()*.5*(self.timercounter**2))
            #self.YOfRobot=self.YOfRobot+(self.acwcelerometer.getY()*.5*(self.timercounter**2))
            '''
            
            
            self.robot_drive.tankDrive(self.joystick1.getY(), self.joystick2.getY())
            
            wpilib.Timer.delay(0.005)
            
if __name__ == '__main__':
    wpilib.run(MyRobot)
