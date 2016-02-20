import wpilib

class Light():
    def __init__(self, Light):
        self.light = Light
        self.on = False

    def turnOn(self):
        self.light.set(wpilib.Relay.Value.kForward)
        self.on = True
        
    def turnOff(self):
        self.light.set(wpilib.Relay.Value.kOff)
        self.on = False