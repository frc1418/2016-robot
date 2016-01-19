#!/usr/local/bin/python3 

import wpilib
from robotpy_ext.control.button_debouncer import ButtonDebouncer
from components import drive, intake
from automations import shootBall
from automations import portcullis

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
        
        self.intake = intake.Arm(wpilib.CANTalon(25),wpilib.CANTalon(30), self.leftBall, self.rightBall, -1)
        
        # #SMART DASHBOARD
        
        ##ROBOT DRIVE##
        self.drive = drive.Drive(self.robot_drive)
        
        
        self.components = {
            'drive': self.drive,
            'intake': self.intake
        }
        
        ##AUTO FUNCTIONALITY##
        self.auto_portcullis = portcullis.PortcullisLift(self.drive, self.intake)
        self.shootBall = shootBall.shootBall(self.intake)
        
    def disabled(self):
        # self.talon.setSensorPosition(0)
        wpilib.Timer.delay(.01)
    
    def operatorControl(self):
        # self.myRobot.setSafetyEnabled(True)
        reverseButton = ButtonDebouncer(self.joystick1, 1)
        
        shoot = ButtonDebouncer(self.joystick2, 1)
        raiseButton = ButtonDebouncer(self.joystick2, 3)
        lowerButton = ButtonDebouncer(self.joystick2, 2)
        portcullis = ButtonDebouncer(self.joystick2, 10)
    
        shooting = False
        raise_portcullis = False
        
        self.intake._calibrate()
        
        while self.isOperatorControl() and self.isEnabled():
            
                
            self.drive.move(self.joystick1.getY(), -self.joystick2.getX())
            
            if reverseButton.get():
                self.drive.switch_direction()
                
            if self.joystick2.getRawButton(4):
                self.intake.intake()
                shooting = False
            elif self.joystick2.getRawButton(5):
                self.intake.outtake()
                shooting = False
                
                
            if raiseButton.get():
                self.intake.raise_arm()
                shooting = False
            elif lowerButton.get():
                self.intake.lower_arm()
                shooting = False
                raise_portcullis = False
                
            if self.joystick1.getRawButton(3):                
                self.intake.set_manual(-1)
                shooting = False
            if self.joystick1.getRawButton(2):
                self.intake.set_manual(1)
                shooting = False
            
            if shoot.get():
                shooting = not shooting
                raise_portcullis = False
            if shooting:
                raise_portcullis = False
                self.shootBall.doit()
                shooting = self.shootBall.get_running()  
                
            
            if portcullis.get():
                raise_portcullis = not raise_portcullis
            if raise_portcullis:
                self.auto_portcullis.doit()
                raise_portcullis = self.auto_portcullis.get_running()  
                
            self.update()            
            wpilib.Timer.delay(0.005)
    
    
    def update(self):
        for component in self.components.values():
            component.doit()
            
            
if __name__ == '__main__':
    wpilib.run(MyRobot)
