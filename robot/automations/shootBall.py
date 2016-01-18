import wpilib

class shootBall():
    def __init__(self, intake):
        self.intake = intake
        self.is_running = False
        self.state = 0
        
    def get_running(self):
        return self.is_running

    def go(self):
        self.is_running = True 

        if self.state == 0:
            self.intake.set_arm_middle()
            self.state = 1
        if self.state == 1 and self.intake.on_target():
            self.state = 2
            self.intake.outtake()
        if self.state == 2:
            self.state = 3
            self.intake.outtake()
            self.intake.set_arm_bottom()
        if self.state == 3:
            self.intake.outtake()
            if(self.intake.on_target):
                self.override()
                
    def override(self):
        self.intake.set_manual(0)
        self.is_running=False