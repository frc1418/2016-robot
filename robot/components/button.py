import wpilib

class Button:
    '''Useful utility class for debouncing buttons'''
    
    def __init__(self,joystick,buttonnum):
        self.joystick=joystick
        self.buttonnum=buttonnum
        self.latest = 0
        self.timer = wpilib.Timer()
        
    def get(self):
        '''Returns the value of the button. If the button is held down, then
        True will only be returned once every 600ms'''
        
        now = self.timer.getMsClock()
        if(self.joystick.getRawButton(self.buttonnum)):
            if (now-self.latest) > 600: 
                self.latest = now
                return True
        return False
