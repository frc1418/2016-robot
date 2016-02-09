import wpilib

class Winch:
    
    winchMotor = wpilib.Talon
    kickMotor = wpilib.Talon
    def on_enable(self):
        
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
        self.kickValue = 0