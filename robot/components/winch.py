import wpilib
from networktables.networktable import NetworkTable

class Winch:

    winchMotor = wpilib.Talon
    kickMotor = wpilib.Talon
    sd = NetworkTable
    def on_enable(self):

        self.winchValue = 0
        self.kickValue = 0
        self.isExtended = False

    def deploy_winch(self):
        self.kickValue = 1
        self.isExtended = True
        self.sd.putValue('ladderUp', True)
    def winch(self):
        if self.isExtended:
            self.winchValue = 1

    def execute(self):
        self.winchMotor.set(self.winchValue)
        self.kickMotor.set(self.kickValue)

        self.winchValue = 0
        self.kickValue = 0