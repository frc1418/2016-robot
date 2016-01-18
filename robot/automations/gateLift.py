class GateLift():
    def __init__(self, drive, intake, drive_speed=-1, drive_time=5):
        self.intake = intake
        self.drive = drive
        
        self.drive_speed = drive_speed
        self.drive_time = drive_time
        
        self.is_running = False
        
    def get_running(self):
        return self.is_running
    
    def go(self):
        self.drive.drive_straight(self.drive_time, self.drive_speed)
        self.intake.set_arm_top()
        
        self.is_running = True
    
    def override(self):
        self.drive.set_manual()
        self.intake.set_manual()
        
        self.is_running = False