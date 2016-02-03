import wpilib

from robotpy_ext.common_drivers import navx
from networktables import NetworkTable

class Winch:
    
    def __init__(self, winchMotor, kickMotor):
        """
        :type winchMotor: wpilib.Talon()
        :type  kickMotor: wpilib.Talon() 
        :type navx: navx.AHRS.create_spi()
        """
        
        
        self.winchMotor = winchMotor
        
        self.kickMotor = kickMotor
        
        self.winchValue = 0
        self.kickValue = 0
        self.isExtended = False
        
    def deploy_winch(self):
        self.kickValue = 1
        self.isExtended = True
    def winch(self):
        if self.isExtended:
            self.winchValue = 1
        
        
    def doit(self):
        self.winchMotor.set(self.winchValue)
        self.kickMotor.set(self.kickValue)
        
        self.winchValue = 0
        self.kickValue = -.05