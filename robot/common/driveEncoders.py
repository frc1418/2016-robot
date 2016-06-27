import wpilib

class DriveEncoders:
    """
        This class deals with the zeroing and reading
        from the encoders mounted on the drive motors
    """

    def __init__(self, motor, isReversed = False):
        """:type motor: wpilib.CANTalon()"""

        self.motor = motor
        if(isReversed):
            self.mod = -1
        else:
            self.mod = 1
        self.initialValue = self.mod * self.motor.getAnalogInPosition()

    def get(self):
        return (self.mod * self.motor.getAnalogInPosition()) - self.initialValue

    def zero(self):
        self.initialValue = self.mod * self.motor.getAnalogInPosition()