from robotpy_ext.autonomous import state, timed_state, StatefulAutonomous
import wpilib

class LowGoal(StatefulAutonomous):
    MODE_NAME='LowGoal'
    DEFAULT = False
    
    def initialize(self):
        self.register_sd_var('Drive_Distance', 9)
        self.register_sd_var('Rotate_Angle', 60)
        self.register_sd_var('Ramp_Distance', 4)
    
    @timed_state(duration = 2, next_state='drive_forward', first = True)
    def lower_arm(self, initial_call):
        self.intake.set_arm_bottom()
            
        if self.intake.on_target():
            self.next_state('drive_forward')
    
    @state
    def drive_forward(self):
        #self.intake.set_arm_middle()
        if self.drive.drive_distance(self.Drive_Distance*12):
            self.next_state('rotate')
    @state
    def rotate(self, initial_call):
        if initial_call:
            self.drive.reset_gyro_angle()
            
        self.intake.set_arm_top()
        
        if self.drive.angle_rotation(self.Rotate_Angle):
            self.next_state('drive_to_ramp')
    @state
    def drive_to_ramp(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
        
        if self.drive.drive_distance(self.Ramp_Distance*12):
            self.next_state('shoot')
    
    @timed_state(duration = 5)
    def shoot(self, initial_call):
        if initial_call:
            self.intake.outtake()
        else:
            self.intake.outtake()
            self.intake.set_arm_middle()
    
  
class ChevalDeFrise(StatefulAutonomous):
    MODE_NAME = "ChevalDeFrise"
    DEFAULT = True
    
    def initialize(self):
        self.register_sd_var("Drive_to_distance", 2.5)
        self.register_sd_var("Drive_on_distance", 0.5)
        
    @timed_state(duration = 2, next_state='lower_arms', first = True)
    def drive_to(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
        
        if self.drive.drive_distance(self.Drive_to_distance*12):
            self.next_state('lower_arms')
            
    @timed_state(duration = 2, next_state='drive_on')
    def lower_arms(self, initial_call):
        self.intake.set_arm_bottom()
        
        if self.intake.on_target():
            self.next_state('drive_on')
        
    @state
    def drive_on(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
            
        if self.drive.drive_distance(self.Drive_on_distance*12):
            self.next_state('drive_over')
        
    @timed_state(duration = 2)
    def drive_over(self, initial_call):
        if initial_call:
            self.intake.set_arm_top()
        
        self.drive.move(1, 0)
        
class DirectPortcullis(StatefulAutonomous):
    MODE_NAME = "DirectPorcullis"
    DEFAULT = False
    
    def initialize(self):
        self.register_sd_var("Drive_Encoder_Distance", 2.5)
        self.register_sd_var("DriveThru_Speed", 0.4)
    
    @timed_state(duration = 2, next_state='drive_forward', first = True)
    def lower_arm(self, initial_call):
        self.intake.set_arm_bottom()
            
        if self.intake.on_target():
            self.next_state('drive_forward')
    @state
    def drive_forward(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
        
        if self.drive.drive_distance(self.Drive_Encoder_Distance*12):
            self.next_state('drive_thru')
    
    @timed_state(duration = 5)
    def drive_thru(self):
        self.intake.set_arm_top()
        
        self.drive.move(self.DriveThru_Speed, 0)
        
        
            
        
            
    