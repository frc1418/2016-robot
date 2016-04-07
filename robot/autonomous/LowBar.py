from robotpy_ext.autonomous import state, timed_state, StatefulAutonomous
from components import intake, drive as Drive
import wpilib
from networktables.util import ntproperty
from networktables import NetworkTable

class LowGoal(StatefulAutonomous):
    MODE_NAME='LowGoal'
    DEFAULT = False
    
    intake = intake.Arm
    drive = Drive.Drive
    sd = NetworkTable
    def initialize(self):
        self.register_sd_var('Drive_Distance', 18)
        self.register_sd_var('Rotate_Angle', 45)
        self.register_sd_var('Ramp_Distance', 6.9)
        self.register_sd_var('Max_Drive_Speed', .5)
    
    @timed_state(duration = 1, next_state='drive_forward', first = True)
    def lower_arm(self, initial_call):
        
        self.drive.reset_drive_encoders()
        self.intake.set_arm_bottom()
            
        if self.intake.on_target(): 
            self.next_state('drive_forward')
    
    @state
    def drive_forward(self):
        #self.intake.set_arm_middle()
        if self.drive.drive_distance(self.Drive_Distance*12, max_speed=self.Max_Drive_Speed):
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
        
        if self.drive.drive_distance(self.Ramp_Distance*12, max_speed=self.Max_Drive_Speed):
            self.next_state('lower_to_shoot')
            
    @timed_state(duration = 1, next_state='shoot')
    def lower_to_shoot(self):
        self.intake.set_arm_middle()
        
        if self.intake.on_target():
            self.next_state('shoot')
        
    
    @timed_state(duration = 15)
    def shoot(self, initial_call):
        self.intake.outtake()
        
class CameraLowGoal(StatefulAutonomous):
    MODE_NAME='CameraLowGoal'
    DEFAULT = False
    
    intake = intake.Arm
    drive = Drive.Drive
    sd = NetworkTable
    present = ntproperty('/components/autoaim/present', False)
    
    def initialize(self):
        self.register_sd_var('Drive_Distance', 18)
        self.register_sd_var('Ramp_Distance', 6.9)
        self.register_sd_var('Max_Drive_Speed', .5)
        self.register_sd_var('RotateSpeed', .7)
    
    @timed_state(duration = 1, next_state='drive_forward', first = True)
    def lower_arm(self, initial_call):
        
        self.drive.reset_drive_encoders()
        self.intake.set_arm_bottom()
            
        if self.intake.on_target(): 
            self.next_state('drive_forward')
    
    @state
    def drive_forward(self):
        #self.intake.set_arm_middle()
        if self.drive.drive_distance(self.Drive_Distance*12, max_speed=self.Max_Drive_Speed):
            self.next_state('find_tower')
    
    @state
    def find_tower(self, initial_call):
        if initial_call:
            self.drive.enable_camera_tracking()
            
        if not self.present:
            self.drive.move(0, self.RotateSpeed)
        else:
            self.next_state('rotate')
    
    @state
    def rotate(self, initial_call):
        if initial_call:
            self.drive.reset_gyro_angle()
        
        if self.drive.align_to_tower():
            self.drive.disable_camera_tracking()
            self.next_state('drive_to_ramp')
    @state
    def drive_to_ramp(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
        
        if self.drive.drive_distance(self.Ramp_Distance*12, max_speed=self.Max_Drive_Speed):
            self.next_state('lower_to_shoot')
            
    @timed_state(duration = 1, next_state='shoot')
    def lower_to_shoot(self):
        self.intake.set_arm_middle()
        
        if self.intake.on_target():
            self.next_state('shoot')
        
    
    @timed_state(duration = 15)
    def shoot(self, initial_call):
        self.intake.outtake()