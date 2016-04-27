#!/usr/bin/env python3

import magicbot
import wpilib

from robotpy_ext.control.button_debouncer import ButtonDebouncer
from components import drive, intake, winch, light
from automations import shootBall, portcullis, lightOff, targetGoal
from common import driveEncoders
from networktables.util import ntproperty


from robotpy_ext.common_drivers import navx, distance_sensors

from networktables.networktable import NetworkTable


class MyRobot(magicbot.MagicRobot):
    
    targetGoal = targetGoal.TargetGoal
    shootBall = shootBall.ShootBall
    winch = winch.Winch
    light = light.Light
    lightSwitch = lightOff.LightSwitch
    intake = intake.Arm
    drive = drive.Drive
    #auto_portcullis = portcullis.PortcullisLift
    
    enable_camera_logging = ntproperty('/camera/logging_enabled', True)
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
        
        self.flashlight = wpilib.Relay(0)
        self.lightTimer = wpilib.Timer()
        self.turningOffState = 0
        self.lastState = False
        
                
        ##DRIVE ENCODERS##
        self.rf_encoder = driveEncoders.DriveEncoders(self.robot_drive.frontRightMotor, True)
        self.lf_encoder = driveEncoders.DriveEncoders(self.robot_drive.frontLeftMotor)
        
        ##DISTANCE SENSORS##
        self.back_sensor = distance_sensors.SharpIRGP2Y0A41SK0F(0)
        self.ultrasonic = wpilib.AnalogInput(1)
        
        ##NavX##
        self.navX = navx.AHRS.create_spi()

        ##SMART DASHBOARD##
        self.sd = NetworkTable.getTable('SmartDashboard')
        
        self.control_loop_wait_time = 0.025
        self.reverseButton = ButtonDebouncer(self.joystick1, 1)

        self.shoot = ButtonDebouncer(self.joystick2, 1)
        self.raiseButton = ButtonDebouncer(self.joystick2, 3)
        self.lowerButton = ButtonDebouncer(self.joystick2, 2)
        self.portcullis = ButtonDebouncer(self.joystick2, 10)
        self.lightButton = ButtonDebouncer(self.joystick1, 6)
        
        self.shooting = False
        self.raise_portcullis = False
    
    def autonomous(self):
        self.drive.reset_gyro_angle()
        magicbot.MagicRobot.autonomous(self)
    
    def disabledPeriodic(self):
        pass
    
    def disabledInit(self):
        self.enable_camera_logging = True
        self.drive.disable_camera_tracking()
    
    def teleopInit(self):
        self.drive.reset_drive_encoders()
        self.sd.putValue('startTheTimer', True)
        self.intake.target_position = None
        self.intake.target_index = None
        
        self.drive.disable_camera_tracking()
        self.enable_camera_logging = False

    def teleopPeriodic(self):
        self.drive.move(-self.joystick1.getY(), self.joystick2.getX())   
            
        if self.reverseButton.get():
            self.drive.switch_direction()
        
        ##BALL INTAKE##
        if self.joystick2.getRawButton(5):
            self.intake.outtake()
        elif self.joystick2.getRawButton(4):
            self.intake.intake()
        
        ##AUTO ARM##
        if self.raiseButton.get():
            self.intake.raise_arm()
        elif self.lowerButton.get():
            self.intake.lower_arm()
            
        ##MANUAL ARM##
        if self.joystick1.getRawButton(3):
            self.intake.set_manual(-1)
        if self.joystick1.getRawButton(2):
            self.intake.set_manual(1)
            
        ##AUTO SHOOT##
        if self.shoot.get():
            self.shootBall.shoot()
        
        ##LIGHTBULB##
        lightButton = False
        guiButton = self.sd.getValue("LightBulb", False)
        if guiButton != self.lastState:
            self.lastState = guiButton
            lightButton = True
        
        self.lastState = guiButton

        if (self.lightButton.get() or lightButton) and self.turningOffState == 0:
            self.lightSwitch.switch()
            
        if self.sd.getValue('Drive/autoAim', False):
            self.targetGoal.target()    
        
        
        ##WINCH##
        if self.joystick1.getRawButton(7): #or self.sd.getValue('ladderButtonPressed'):
            self.winch.deploy_winch()
        if self.joystick1.getRawButton(8):
            self.killAutoActions()
            self.winch.winch()
        
        if self.joystick1.getRawButton(9):
            if self.drive.isTheRobotBackwards:
                self.drive.move(.5, 0)
        
        # Debug stuff
        if not self.ds.isFMSAttached():
            if self.joystick1.getRawButton(10):
                self.drive.angle_rotation(35)
            elif self.joystick1.getRawButton(9): #this could prove problematic if the robot is backwards
                self.drive.angle_rotation(0)
            elif self.joystick2.getRawButton(10):
                self.drive.enable_camera_tracking()
                self.drive.align_to_tower()
            
                

if __name__ == '__main__':
    wpilib.run(MyRobot)
