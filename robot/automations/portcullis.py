import wpilib
ARM_DOWN = 1
DRIVE_ENC = 2
DRIVE = 3
ARM_MIDDLE = 4
ARM_UP = 5
class PortcullisLift:
 
    def __init__(self, sd, drive, intake, drive_speed=-.5):
        self.intake = intake
        self.drive = drive
        self.sd = sd
        
        self.drive_speed = self.sd.getAutoUpdateValue('Portcullis | Drive Speed', .3)
        self.drive_reverse_speed = self.sd.getAutoUpdateValue('Portcullis | Reverse Speed', -.05)
        self.drive_speed_2 = self.sd.getAutoUpdateValue('Portcullis | Drive Speed_2', .5)

        self.is_running = False
        self.state = ARM_DOWN
        
        self.timer = wpilib.Timer()
        self.timer.start()
    def get_running(self):
        return self.is_running
    
    
    def doit(self):
        self.is_running = True
        #Add state machine to put the arm at the bottom first
        if self.state == ARM_DOWN:
            self.intake.set_arm_bottom()
            if self.intake.on_target():
                self.timer.reset()
                self.state = DRIVE
        if self.state == DRIVE:
            self.drive.move(self.drive_speed.value, 0)
            if self.timer.hasPeriodPassed(1):
                self.timer.reset()
                self.state = ARM_MIDDLE
        if self.state == ARM_MIDDLE:
            self.drive.move(self.drive_reverse_speed.value, 0)
            self.intake.set_arm_top()
            if self.timer.hasPeriodPassed(.5):
                self.state = ARM_UP
        if self.state == ARM_UP:
            self.intake.set_arm_top()
            #self.drive.move(self.drive_speed_2.value, 0)
            if self.drive.drive_distance(36):
            #if #self.intake.on_target():
                self.is_running = False
                self.state = ARM_DOWN
                
        
    