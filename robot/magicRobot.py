#!/usr/local/bin/python3
import magicbot
import wpilib

from robotpy_ext.control.button_debouncer import ButtonDebouncer
from components import drive, intake, winch
from automations import shootBall, portcullis
from common import driveEncoders

from robotpy_ext.common_drivers import navx
from robotpy_ext.autonomous import AutonomousModeSelector

from networktables.networktable import NetworkTable


class MyRobot(magicbot.MagicRobot):
    
    drive = drive.Drive
    intake = intake.Arm
    winch = winch.Winch
    
    def createObjects(self):
        # #INITIALIZE JOYSTICKS##
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)


        # #INITIALIZE MOTORS##
        self.lf_motor = wpilib.CANTalon(5)
        self.lr_motor = wpilib.CANTalon(10)
        self.rf_motor = wpilib.CANTalon(15)
        self.rr_motor = wpilib.CANTalon(20)        
        
        self.robot_drive = wpilib.RobotDrive(self.lf_motor, self.lr_motor, self.rf_motor, self.rr_motor)
        
        self.leftArm = wpilib.CANTalon(25)
        self.rightArm = wpilib.CANTalon(30)
        
        self.leftBall = wpilib.Talon(9)
        
        self.winchMotor = wpilib.Talon(0)
        self.kickMotor = wpilib.Talon(1)
        ##DRIVE ENCODERS##
        self.rf_encoder = driveEncoders.DriveEncoders(self.robot_drive.frontRightMotor, True)
        self.lf_encoder = driveEncoders.DriveEncoders(self.robot_drive.frontLeftMotor)
        ##NavX##
        self.navx = navx.AHRS.create_spi()

        ##SMART DASHBOARD##
        self.sd = NetworkTable.getTable('SmartDashboard')

        ##AUTO FUNCTIONALITY##
        self.auto_portcullis = portcullis.PortcullisLift(self.sd, self.drive, self.intake)
        self.shootBall = shootBall.shootBall(self.intake)
        
        self.control_loop_wait_time = 0.025
        self.automodes = AutonomousModeSelector('autonomous', self.auto_components)
    
        self.reverseButton = ButtonDebouncer(self.joystick1, 1)

        self.shoot = ButtonDebouncer(self.joystick2, 1)
        self.raiseButton = ButtonDebouncer(self.joystick2, 3)
        self.lowerButton = ButtonDebouncer(self.joystick2, 2)
        self.portcullis = ButtonDebouncer(self.joystick2, 10)
        
        self.shooting = False
        self.raise_portcullis = False
    def teleopInit(self):
        self.drive.reset_drive_encoders()

    
    def teleopPeriodic(self):
        if self.joystick1.getZ() > .75:
                self.robot_drive.tankDrive(self.joystick1, self.joystick2)
        else:
            self.drive.move(-self.joystick1.getY(), self.joystick2.getX())   
            
        if self.reverseButton.get():
            self.drive.switch_direction()
        
        ##BALL INTAKE##
        if self.joystick2.getRawButton(5):
            self.intake.outtake()
            self.shooting = False
            self.raise_portcullis = False
        elif self.joystick2.getRawButton(4):
            self.intake.intake()
            shooting = False
            self.raise_portcullis = False
        
        ##AUTO ARM##
        if self.raiseButton.get():
            self.intake.raise_arm()
            self.shooting = False
            self.raise_portcullis = False
        elif self.lowerButton.get():
            self.intake.lower_arm()
            self.shooting = False
            self.raise_portcullis = False
            
        ##MANUAL ARM##
        if self.joystick1.getRawButton(3):
            self.intake.set_manual(-1)
            self.shooting = False
            self.raise_portcullis = False
        if self.joystick1.getRawButton(2):
            self.intake.set_manual(1)
            self.shooting = False
            self.raise_portcullis = False
            
        ##AUTO SHOOT##
        if self.shoot.get():
            self.shooting = not shooting
            self.raise_portcullis = False
        if shooting:
            self.raise_portcullis = False
            self.shootBall.doit()
            self.shooting = self.shootBall.get_running()

        ##AUTO PORTCULLIS##
        if self.portcullis.get():
            self.raise_portcullis = not self.raise_portcullis
        if self.raise_portcullis:
            self.auto_portcullis.doit()
            self.raise_portcullis = self.auto_portcullis.get_running()
        else:
            self.auto_portcullis.state = 1
        
        ##WINCH##
        if self.joystick1.getRawButton(7):
            self.winch.deploy_winch()
        if self.joystick1.getRawButton(8):
            self.shooting = False
            self.raise_portcullis = False
            self.winch.winch()
               
        self.update()            
        
    def update(self):
        for component in self.components.values():
            component.exe()

if __name__ == '__main__':
    wpilib.run(MyRobot)
