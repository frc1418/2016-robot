#! /usr/bin/env python3
import wpilib
from robotpy_ext.control import xbox_controller
import magicbot

class MyRobot(magicbot.MagicRobot):
    
    def createObjects(self):
        
       self.driveStick = xbox_controller.XboxController(0)
       
       if MyRobot.isSimulation():
           self.lf_motor = wpilib.Jaguar(1)
           self.lr_motor = wpilib.Jaguar(2)
           self.rf_motor = wpilib.Jaguar(3)
           self.rr_motor = wpilib.Jaguar(4)
       self.drive = wpilib.RobotDrive(self.lf_motor, self.lr_motor, self.rf_motor, self.rr_motor)
        
    def disabledPeriodic(self):
        wpilib.Timer.delay(.01)
    
    def teleopInit(self):
        pass
    
    def teleopPeriodic(self):
        
        self.drive.tankDrive(self.driveStick.getLeftY(), self.driveStick.getRightY(), False)
if __name__ == '__main__':
    wpilib.run(MyRobot)
