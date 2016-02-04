import wpilib

class DriveEncoders:
    '''
        This class deals with the zeroing and reading
        from the encoders mounted on the drive motors
    '''

    def __init__(self, motor, isReversed = False):
        self.motor = motor
        self.motor.reverseSensor(isReversed)
        self.initialValue = self.motor.getAnalogInPosition()
        
    def get(self):
        return self.motor.getAnalogInPosition() - self.initialValue
    
    def zero(self):
        self.initialValue = self.motor.getAnalogInPosition()