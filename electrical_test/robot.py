#! /usr/bin/env python3
import wpilib
import enum

from networktables import NetworkTable

class Swerve(enum.IntEnum):
    DRIVE = 0
    ROTATE = 1
    
class MyRobot(wpilib.SampleRobot):
    
    def robotInit(self):
        self.sd = NetworkTable.getTable('SmartDashboard')
        
    
        self.timercounter = 0

        # #INITIALIZE JOYSTICKS##
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)
        
        
        
        # #INITIALIZE MOTORS##
        self.lf_wheel = (wpilib.Victor(0), wpilib.CANTalon(5))
        self.lr_wheel = (wpilib.Victor(1), wpilib.CANTalon(10))
        self.rf_wheel = (wpilib.Victor(2), wpilib.CANTalon(15))
        self.rr_wheel = (wpilib.Victor(3), wpilib.CANTalon(20))
        
        self.lf_wheel[Swerve.ROTATE].changeControlMode(wpilib.CANTalon.ControlMode.Position)
        self.lr_wheel[Swerve.ROTATE].changeControlMode(wpilib.CANTalon.ControlMode.Position)
        self.rf_wheel[Swerve.ROTATE].changeControlMode(wpilib.CANTalon.ControlMode.Position)
        self.rr_wheel[Swerve.ROTATE].changeControlMode(wpilib.CANTalon.ControlMode.Position)
        # #SMART DASHBOARD
        
        # #ROBOT DRIVE##
        #self.robot_drive = wpilib.RobotDrive(self.lf_motor, self.lr_motor, self.rf_motor, self.rr_motor)
        self.robot_drive = wpilib.RobotDrive(self.lf_wheel[Swerve.DRIVE],self.lr_wheel[Swerve.DRIVE],self.rf_wheel[Swerve.DRIVE],self.rr_wheel[Swerve.DRIVE])
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kFrontLeft, True);
        self.robot_drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kRearLeft, True);
    def disabled(self):
        # self.talon.setSensorPosition(0)
        wpilib.Timer.delay(.01)
    
    def operatorControl(self):
        # self.myRobot.setSafetyEnabled(True)
        
        while self.isOperatorControl() and self.isEnabled():
            '''
            self.angle = self.joystick1.getDirectionDegrees()
            self.magnitude = self.joystick1.getMagnitude()
            self.rotation = self.joystick2.getX() #no greater than 1, no less than -1
            
            Vtx = self.magnitude*COS(RADIANS(self.angle+90)) #no greater than 1, no less than -1
            Vty = self.magnitude*SIN(RADIANS(self.angle+90)) #no greater than 1, no less than -1
            
            #Velocity in (x,y)            
            lf = (Vtx - self.rotation * 1, Vty + self.rotation * -1)
            lr = (Vtx - self.rotation * -1, Vty + self.rotation * -1)
            rf = (Vtx - self.rotation * 1, Vty + self.rotation * 1)
            rr = (Vtx - self.rotation * -1 , Vty + self.rotation * 1)
            
            #(speed, angle) in (x,y)            
            lf2 = (sqrt((lf(0)*lf(0))+(lf(1)*lf(1))), atan2(lf(0),lf(1)))
            lr2 = (sqrt((lr(0)*lr(0))+(lr(1)*lr(1))), atan2(lr(0),lr(1)))
            rf2 = (sqrt((rf(0)*rf(0))+(rf(1)*rf(1))), atan2(rf(0),rf(1)))
            rr2 = (sqrt((rr(0)*rr(0))+(rr(1)*rr(1))), atan2(rr(0),rr(1)))
            '''
            
            self.x = self.joystick1.getX()
            self.y = self.joystick1.getY()
            self.rotation = self.joystick2.getX() #no greater than 1, no less than -1

            self.robot_drive.arcadeDrive(self.x,self.y)
            
            if self.joystick1.getRawButton(1):
                self.lf_wheel[Swerve.ROTATE].set(self.lf_wheel[Swerve.ROTATE].getEncPosition() + 300)
                self.lr_wheel[Swerve.ROTATE].set(self.lf_wheel[Swerve.ROTATE].getEncPosition() + 300) 
                self.rf_wheel[Swerve.ROTATE].set(self.lf_wheel[Swerve.ROTATE].getEncPosition() + 300)
                self.rr_wheel[Swerve.ROTATE].set(self.lf_wheel[Swerve.ROTATE].getEncPosition() + 300)
            
            self.sd.putNumber("Encoder Position", self.lr_wheel[Swerve.ROTATE].getEncPosition())
            self.sd.putNumber("Encoder Position", self.rf_wheel[Swerve.ROTATE].getEncPosition())
            self.sd.putNumber("Encoder Position", self.rr_wheel[Swerve.ROTATE].getEncPosition())
            self.sd.putNumber("Encoder Position", self.lf_wheel[Swerve.ROTATE].getEncPosition())
            
            wpilib.Timer.delay(0.005)
            
if __name__ == '__main__':
    wpilib.run(MyRobot)
