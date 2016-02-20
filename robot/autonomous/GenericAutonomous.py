from robotpy_ext.autonomous import state, timed_state, StatefulAutonomous
from components import intake, drive
import wpilib

class LowBar(StatefulAutonomous):
    DEFAULT = False
    
    intake = intake.Arm
    drive = drive.Drive
    def initialize(self):
        self.register_sd_var('Drive_Distance', 17.2)
        self.register_sd_var('Rotate_Angle', 60)
        self.register_sd_var('Ramp_Distance', 8.4)
    
    @state
    def LowBarStart(self):
        self.next_state('lower_arm')
    
    @timed_state(duration = 1, next_state='drive_forward')
    def lower_arm(self, initial_call):
        self.intake.set_arm_bottom()
            
        if self.intake.on_target(): 
            self.next_state('drive_forward')
    
    @state
    def drive_forward(self):
        #self.intake.set_arm_middle()
        if self.drive.drive_distance(self.Drive_Distance*12):
            self.next_state('transition')
    
class ChevalDeFrise(StatefulAutonomous):
    DEFAULT = False
    
    intake = intake.Arm
    drive = drive.Drive
    def initialize(self):
        self.register_sd_var("Drive_to_distance", 4.2)
        self.register_sd_var("Drive_on_distance", 1)
    
    @state
    def A1Start(self):
        self.next_state('drive_to')
    
    @timed_state(duration = 2, next_state='lower_arms')
    def drive_to(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
        
        if self.drive.drive_distance(self.Drive_to_distance*12):
            self.next_state('lower_arms')
            
    @timed_state(duration = .2, next_state='drive_on')
    def lower_arms(self, initial_call):
        self.intake.set_arm_bottom()
        
        if self.intake.on_target():
            self.next_state('drive_on')
        
    @timed_state(duration = 2, next_state='drive_over')
    def drive_on(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
            
        if self.drive.drive_distance(self.Drive_on_distance*12):
            self.next_state('drive_over')
        
    @timed_state(duration = 4, next_state='transition')
    def drive_over(self, initial_call):
        self.intake.set_arm_top()
        
        self.drive.move(0.3, 0)
        
class Portcullis(StatefulAutonomous):
    DEFAULT = False
    
    intake = intake.Arm
    drive = drive.Drive
    def initialize(self):
        self.register_sd_var("Drive_Encoder_Distance", 5.10)
        self.register_sd_var("Arm_To_Position", 1000)
        self.register_sd_var("DriveThru_Speed", 0.4)
    
    @state
    def A0Start(self):
        self.next_state('lower_arm')
    
    @timed_state(duration = 2, next_state='drive_forward')
    def lower_arm(self, initial_call):
        self.intake.set_arm_bottom()
            
        if self.intake.on_target():
            self.next_state('drive_forward')
    
    @state
    def drive_forward(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
        
        if self.drive.drive_distance(self.Drive_Encoder_Distance*12):
            self.next_state('raise_arm')
    
    @timed_state(duration = 0.5, next_state='drive_thru')
    def raise_arm(self):
        self.intake.set_target_position(self.Arm_To_Position)
        
        if self.intake.on_target():
            self.next_state('drive_thru')
    
    @timed_state(duration = 3, next_state = 'transition')
    def drive_thru(self):
        self.intake.set_arm_top()
        
        self.drive.move(self.DriveThru_Speed, 0)

class Charge(StatefulAutonomous):
    DEFAULT = False
    
    @timed_state(duration = 3, first = True)
    def E0Start(self, initial_call):
        self.drive.move(1,0)