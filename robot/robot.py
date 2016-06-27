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

    enable_camera_logging = ntproperty('/camera/logging_enabled', True)
    auto_aim_button = ntproperty('/SmartDashboard/Drive/autoAim', False, writeDefault = False)

    '''Create basic components (motor controllers, joysticks, etc.)'''
    def createObjects(self):
        # Joysticks
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)

        # Motors (l/r = left/right, f/r = front/rear)
        self.lf_motor = wpilib.CANTalon(5)
        self.lr_motor = wpilib.CANTalon(10)
        self.rf_motor = wpilib.CANTalon(15)
        self.rr_motor = wpilib.CANTalon(20)

        # Drivetrain object
        self.robot_drive = wpilib.RobotDrive(self.lf_motor, self.lr_motor, self.rf_motor, self.rr_motor)

        # Left and right arm motors (there's two, which both control the raising and lowering the arm)
        self.leftArm = wpilib.CANTalon(25)
        self.rightArm = wpilib.CANTalon(30)

        # Motor that spins the bar at the end of the arm.
        # There was originally going to be one on the right, but we decided against that in the end.
        # In retrospect, that was probably a mistake.
        self.leftBall = wpilib.Talon(9)

        # Motor that reels in the winch to lift the robot.
        self.winchMotor = wpilib.Talon(0)
        # Motor that opens the winch.
        self.kickMotor = wpilib.Talon(1)

        # Aiming flashlight
        self.flashlight = wpilib.Relay(0)
        # Timer to keep light from staying on for too long
        self.lightTimer = wpilib.Timer()
        # Flashlight has three intensities. So, when it's turning off, it has to go off on, off on, off.
        # self.turningOffState keeps track of which on/off it's on.
        self.turningOffState = 0
        # Is currently on or off? Used to detect if UI button is pressed.
        self.lastState = False

        # Drive encoders; measure how much the motor has spun
        self.rf_encoder = driveEncoders.DriveEncoders(self.robot_drive.frontRightMotor, True)
        self.lf_encoder = driveEncoders.DriveEncoders(self.robot_drive.frontLeftMotor)

        # Distance sensors
        self.back_sensor = distance_sensors.SharpIRGP2Y0A41SK0F(0)
        self.ultrasonic = wpilib.AnalogInput(1)

        # NavX (purple board on top of the RoboRIO)
        self.navX = navx.AHRS.create_spi()

        # Initialize SmartDashboard, the table of robot values
        self.sd = NetworkTable.getTable('SmartDashboard')

        # How much will the control loop pause in between (0.025s = 25ms)
        self.control_loop_wait_time = 0.025
        # Button to reverse controls
        self.reverseButton = ButtonDebouncer(self.joystick1, 1)

        # Initiate functional buttons on joysticks
        self.shoot = ButtonDebouncer(self.joystick2, 1)
        self.raiseButton = ButtonDebouncer(self.joystick2, 3)
        self.lowerButton = ButtonDebouncer(self.joystick2, 2)
        self.lightButton = ButtonDebouncer(self.joystick1, 6)

    def autonomous(self):
        '''Prepare for autonomous mode'''

        # Reset Gyro to 0
        self.drive.reset_gyro_angle()
        # Call autonomous
        magicbot.MagicRobot.autonomous(self)

    def disabledPeriodic(self):
        '''Repeat periodically while robot is disabled. Usually emptied. Sometimes used to easily test sensors and other things.'''
        pass

    def disabledInit(self):
        '''Do once right away when robot is disabled.'''
        self.enable_camera_logging = True
        self.drive.disable_camera_tracking()

    def teleopInit(self):
        '''Do when teleoperated mode is started.'''
        self.drive.reset_drive_encoders()
        self.sd.putValue('startTheTimer', True)
        self.intake.target_position = None
        self.intake.target_index = None

        self.drive.disable_camera_tracking()
        self.enable_camera_logging = False

    def teleopPeriodic(self):
        '''Do periodically while robot is in teleoperated mode.'''

        # Get the joystick values and move as much as they say.
        self.drive.move(-self.joystick1.getY(), self.joystick2.getX())

        # If reverse control button is pressed,
        if self.reverseButton.get():
            # Reverse the drivetrain direction
            self.drive.switch_direction()

        # If outtake button is pressed,
        if self.joystick2.getRawButton(5):
            # Then spit ball out.
            self.intake.outtake()
        # Or, if intake button is pressed,
        elif self.joystick2.getRawButton(4):
            # Then suck button in.
            self.intake.intake()

        # If shoot button pressed
        if self.shoot.get():
            # Automatically shoot ball
            self.shootBall.shoot()

        '''There's two sets of arm buttons. The first automatically raises and lowers the arm the proper amount, whereas the second will let you manually raise and lower it more precise amounts.'''
        # If automatic arm raise button is pressed,
        if self.raiseButton.get():
            # Raise arm
            self.intake.raise_arm()
        # Or, if automatic arm lower button is pressed, (won't do both at once)
        elif self.lowerButton.get():
            # Lower arm
            self.intake.lower_arm()

        # If manual arm raise button is pressed,
        if self.joystick1.getRawButton(3):
            # Raise arm
            self.intake.set_manual(-1)
        # If manual arm lower button is pressed, (this one can be activated both at one time)
        if self.joystick1.getRawButton(2):
            # Lower arm
            self.intake.set_manual(1)


        # Flashlight management
        # Automatically turn flashlight off at the starting. It will only be made true if NT value is true.
        lightButton = False

        guiButton = self.sd.getValue('LightBulb', False)
        if guiButton != self.lastState:
            self.lastState = guiButton
            lightButton = True

        self.lastState = guiButton

        if (self.lightButton.get() or lightButton) and self.turningOffState == 0:
            self.lightSwitch.switch()

        if self.joystick1.getRawButton(5) or self.auto_aim_button:
            self.targetGoal.target()


        ##WINCH##
        if self.joystick1.getRawButton(7): #or self.sd.getValue('ladderButtonPressed'):
            self.winch.deploy_winch()
        if self.joystick1.getRawButton(8):
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
