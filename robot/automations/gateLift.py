class GateLift(AutoFunctionality):
    def __init__(self, drive, intake, drive_speed=0.5, drive_time=2):
        self.intake = intake
        self.drive = drive
        self.drive_time = drive_time
        self.drive_speed = drive_speed
        
        self.override_button = None
        
        self.running = False
    
    def get_running(self):
        return self.running
    
    def go(self):
        self.intake.set_arm_top()
        self.drive.drive_straight(self.drive_time, self.drive_speed);
    
    def override(self):
        self.drive.want_manual = True
        self.intake.want_manual = True