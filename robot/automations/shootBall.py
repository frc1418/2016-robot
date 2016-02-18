import wpilib
import components.intake as Intake

ARM_UP = 0
SPIN_WHEEL = 1
ARM_DOWN = 2    

class shootBall():
    intake = Intake.Arm
    def on_enable(self):
        self.is_running = False
        self.state = ARM_UP
        self.timer = wpilib.Timer()
        self.timer.start()
        
    def get_running(self):
        return self.is_running
        
        
    def doit(self):
        self.is_running = True
        
        if self.state == ARM_UP:
            self.timer.reset()
            self.intake.set_arm_middle()
            if self.intake.on_target():
                self.state = SPIN_WHEEL
        if self.state == SPIN_WHEEL:
            self.intake.outtake()
            if self.timer.hasPeriodPassed(1):
                self.is_running = False
                self.state = ARM_UP
        #    self.state = ARM_DOWN
        #if self.state == ARM_DOWN:
        #    self.intake.outtake()
        #    self.intake.set_arm_bottom()
        #    if self.intake.on_target():
        #        self.state = ARM_UP
        #        self.is_running = False
    def execute(self):
        pass