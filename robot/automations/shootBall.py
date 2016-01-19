ARM_UP = 0
SPIN_WHEEL = 1
ARM_DOWN = 2    

class shootBall():
    def __init__(self, intake):
        self.intake = intake
        self.is_running = False
        self.state = ARM_UP
        
    def get_running(self):
        return self.is_running
                    
    def override(self):
        self.intake.set_manual(0)
        self.is_running=False
        
    def doit(self):
        self.is_running = True
        
        if self.state == ARM_UP:
            self.intake.set_arm_middle()
            if self.intake.on_target():
                self.state = SPIN_WHEEL
        if self.state == SPIN_WHEEL:
            self.intake.outtake()
            self.state = ARM_DOWN
        if self.state == ARM_DOWN:
            self.intake.outtake()
            self.intake.set_arm_bottom()
            if self.intake.on_target():
                self.state = ARM_UP
                self.is_running = False
