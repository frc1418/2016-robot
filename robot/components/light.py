import wpilib
class Light:
    
    flashlight = wpilib.Relay
    
    def __init__(self):
        self.on = False

    def turnOn(self):
        self.flashlight.set(wpilib.Relay.Value.kForward)
        self.on = True
        
    def turnOff(self):
        self.flashlight.set(wpilib.Relay.Value.kOff)
        self.on = False
    
    def execute(self):
        pass