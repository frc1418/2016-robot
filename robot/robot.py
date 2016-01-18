#!/usr/bin/env python3

import wpilib
from robotpy_ext.control.button_debouncer import ButtonDebouncer
from components import drive, intake
from automations import gateLift, shootBall

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
        
        self.lf_motor.reverseOutput(True)
        self.lr_motor.reverseOutput(True)
        self.rf_motor.reverseOutput(True)
        self.rr_motor.reverseOutput(True)
        
        self.robot_drive = wpilib.RobotDrive(self.lf_motor, self.lr_motor, self.rf_motor, self.rr_motor)
        
        
        ##Intake Mechanism
        self.leftBall = wpilib.Relay(0)
        self.rightBall = wpilib.Relay(1)
        
        self.intake = intake.Arm(wpilib.CANTalon(25), self.leftBall, self.rightBall, -1)
        
        # #SMART DASHBOARD
        
        ##ROBOT DRIVE##
        self.drive = drive.Drive(self.robot_drive)
        
        
        self.components = {
            'drive': self.drive,
            'intake': self.intake
        }
        
        ##AUTO FUNCTIONALITY##
        self.auto_gate_lift = gateLift.GateLift(self.drive, self.intake)
        self.shootBall = shootBall.shootBall(self.intake)
        
    def disabled(self):
        # self.talon.setSensorPosition(0)
        wpilib.Timer.delay(.01)
    
    def operatorControl(self):
        # self.myRobot.setSafetyEnabled(True)
        reverseButton = ButtonDebouncer(self.joystick1, 1)
        raiseButton = ButtonDebouncer(self.joystick2, 3)
        lowerButton = ButtonDebouncer(self.joystick2, 2)
        shoot = ButtonDebouncer(self.joystick1, 2)
        manualZero = ButtonDebouncer(self.joystick1,3)
        shooting = False
        
        while self.isOperatorControl() and self.isEnabled():
            if reverseButton.get():
                self.drive.switch_direction()
            
            if self.joystick2.getRawButton(4):
                self.intake.intake()
                self.shootBall.override()
            elif self.joystick2.getRawButton(5):
                self.intake.outtake()
                self.shootBall.override()
                
                
            if raiseButton.get():
                self.intake.raise_arm()
                self.shootBall.override()
            elif lowerButton.get():
                self.intake.lower_arm()
                self.shootBall.override()
                
            if self.joystick1.getRawButton(3):                
                self.intake.set_manual(-1)
                self.shootBall.override()
            if self.joystick1.getRawButton(2):
                self.intake.set_manual(1)
                self.shootBall.override()
            
            if shoot.get():
                shooting = True
            if shooting:
                self.shootBall.doit()
                shooting = self.shootBall.get_running()  
                
            if self.joystick1.getRawButton(10) and not self.auto_gate_lift.get_running():
                self.auto_gate_lift.go()
            elif not self.joystick1.getRawButton(10) and self.auto_gate_lift.get_running():
                self.auto_gate_lift.override()
            
            self.drive.move(self.joystick1.getY(), self.joystick2.getX())
            
            self.drive.move(self.joystick1.getY(), -self.joystick2.getX())
            self.update()            
            wpilib.Timer.delay(0.005)
    
    
    def update(self):
        for component in self.components.values():
            component.doit()
            
            
if __name__ == '__main__':
    wpilib.run(MyRobot)
