#!/usr/local/bin/python3 

import wpilib
from robotpy_ext.control.button_debouncer import ButtonDebouncer
from components import drive, intake
from automations import shootBall
from automations import portcullis
from robotpy_ext.common_drivers import navx

from networktables.networktable import NetworkTable

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
        
        ##NavX##
        self.navx = navx.AHRS.create_spi()
        self.analog = wpilib.AnalogInput(navx.getNavxAnalogInChannel(0))
        
        ##SMART DASHBOARD##
        self.sd = NetworkTable.getTable('SmartDashboard')
                
        ##Intake Mechanism
        self.leftBall = wpilib.Talon(9)
        
        self.intake = intake.Arm(wpilib.CANTalon(25),wpilib.CANTalon(30), self.leftBall, 1)
        
        ##ROBOT DRIVE##
        self.drive = drive.Drive(self.robot_drive, self.navx)
        
        
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
        self.logger.info("Operator Control")
        
        reverseButton = ButtonDebouncer(self.joystick1, 1)
        
        shoot = ButtonDebouncer(self.joystick2, 1)
        raiseButton = ButtonDebouncer(self.joystick2, 3)
        lowerButton = ButtonDebouncer(self.joystick2, 2)
        portcullis = ButtonDebouncer(self.joystick2, 10)
    
        shooting = False
        raise_portcullis = False
        
        
        while self.isOperatorControl() and self.isEnabled():
            
                
            self.drive.move(self.joystick1.getY(), self.joystick2.getX())
            
            if reverseButton.get():
                self.drive.switch_direction()
                
            if self.joystick2.getRawButton(5):
                self.intake.intake()
                shooting = False
                raise_portcullis = False
            elif self.joystick2.getRawButton(4):
                self.intake.outtake()
                shooting = False
                raise_portcullis = False
                
            if raiseButton.get():
                self.intake.raise_arm()
                shooting = False
                raise_portcullis = False
            elif lowerButton.get():
                self.intake.lower_arm()
                shooting = False
                raise_portcullis = False
                
            if self.joystick1.getRawButton(3):                
                self.intake.set_manual(-1)
                shooting = False
                raise_portcullis = False
            if self.joystick1.getRawButton(2):
                self.intake.set_manual(1)
                shooting = False
                raise_portcullis = False
            
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
            self.updateSmartDashboard()
            wpilib.Timer.delay(0.005)
    
    
    def update(self):
        for component in self.components.values():
            component.doit()
    
    def updateSmartDashboard(self):
        self.sd.putBoolean('NavX | SupportsDisplacement', self.navx._isDisplacementSupported())
        self.sd.putBoolean('NavX | IsCalibrating', self.navx.isCalibrating())
        self.sd.putBoolean('NavX | IsConnected', self.navx.isConnected())
        self.sd.putNumber('NavX | Angle', self.navx.getAngle())
        self.sd.putNumber('NavX | Pitch', self.navx.getPitch())
        self.sd.putNumber('NavX | Yaw', self.navx.getYaw())
        self.sd.putNumber('NavX | Roll', self.navx.getRoll())
        self.sd.putNumber('NavX | Analog', self.analog.getVoltage())        
            
if __name__ == '__main__':
    wpilib.run(MyRobot)
