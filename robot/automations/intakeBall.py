import wpilib

START_SPIN = 0
ARM_DOWN = 1    
ARM_UP = 2


class intakeBall():
    def __init__(self, intake):
        self.intake = intake
        self.is_running = False
        self.state = START_SPIN
        self.timer = wpilib.Timer()
        self.timer.start()
        
    def get_running(self):
        return self.is_running
        
    def doit(self):
        self.is_running = True
        
        if self.state == START_SPIN:
            self.timer.reset()
            self.intake.intake()
            if self.timer.hasPeriodPassed(1):
                self.state = ARM_DOWN
        if self.state == ARM_DOWN:
            self.intake.set_arm_middle()
            self.intake.intake()
            if self.timer.hasPeriodPassed(2):
                self.state = ARM_UP
        if self.state == ARM_UP:
            self.intake.set_arm_top()
            if self.intake.on_target():
                self.is_running = False
                self.state = START_SPIN