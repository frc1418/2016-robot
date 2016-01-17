#!/usr/bin/env python3

import wpilib
from robotpy_ext.control.button_debouncer import ButtonDebouncer
from components import drive, intake, button

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
        
        self.robot_drive = wpilib.RobotDrive(self.lf_motor, self.lr_motor, self.rf_motor, self.rr_motor)
        
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kFrontLeft, True)
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kFrontRight, True)
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kRearLeft, True)
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kRearRight, True)
        
        ##Intake Mechanism
        self.leftBall = wpilib.Relay(0)
        self.rightBall = wpilib.Relay(1)
        
        self.arm = wpilib.CANTalon(25)
        self.arm.setF
        
        # #SMART DASHBOARD
        
        # #ROBOT DRIVE##
        
        self.drive = drive.Drive(self.robot_drive)
        
        self.intake = intake.Intake(self.leftBall, self.rightBall, self.arm)
        
        self.components = {
            'drive': self.drive,
            'intake': self.intake
        }
        
        
    def disabled(self):
        # self.talon.setSensorPosition(0)
        wpilib.Timer.delay(.01)
    
    
    def operatorControl(self):
        # self.myRobot.setSafetyEnabled(True)
        while self.isOperatorControl() and self.isEnabled():
            
            
            reverseButton = button.Button(self.joystick1, 1)
            raiseButton = button.Button(self.joystick2, 3)
            lowerButton = button.Button(self.joystick2, 2)
            
            if reverseButton.get():
                self.drive.switch_direction()
            
            if self.joystick2.getRawButton(4):
                self.intake.intake()
            elif self.joystick2.getRawButton(5):
                self.intake.outtake()
                
                
            if raiseButton.get():
                print("Hello")
                self.intake.raise_arm()
            elif lowerButton.get():
                print("Goodbye")
                self.intake.lower_arm()
                
            self.drive.move(self.joystick1.getY(), self.joystick2.getX())
            
            self.update()            
            wpilib.Timer.delay(0.005)
    
    
    def update(self):
        for component in self.components.values():
            component.doit()
            
            
if __name__ == '__main__':
    wpilib.run(MyRobot)
