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
        self.register_sd_var('Rotate_Angle', 46)
        self.register_sd_var('Ramp_Distance', 6)
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
        self.register_sd_var('Drive_Bar_Distance', 10)
        self.register_sd_var('Drive_Distance', 18)
        self.register_sd_var('Ramp_Distance', 6)
        self.register_sd_var('Max_Drive_Speed', .5)
        self.register_sd_var('RotateSpeed', .4)
        self.register_sd_var('RotateAngle', 46)
    
    @timed_state(duration = 1, next_state='drive_under_bar', first=True)
    def lower_arm(self, initial_call):
        self.drive.reset_drive_encoders()
        self.intake.set_arm_bottom()
            
        if self.intake.on_target(): 
            self.next_state('drive_under_bar')
    @state
    def drive_under_bar(self):
        if self.drive.drive_distance(self.Drive_Bar_Distance*12, max_speed=self.Max_Drive_Speed):
            self.next_state('drive_forward')
    
    @state
    def drive_forward(self):
        self.intake.set_target_position(1000)
        if self.drive.drive_distance(self.Drive_Distance*12, max_speed=self.Max_Drive_Speed):
            self.next_state('lower_arm2')
       
    @timed_state(duration=1, next_state='rotate')     
    def lower_arm2(self):
        self.intake.set_arm_bottom()
    
    #@state
    #def find_tower(self, initial_call):
    #    if initial_call:
    #        self.drive.enable_camera_tracking()
    #        
    #    if not self.present:
    #        self.drive.move(0, self.RotateSpeed)
    #    else:
    #        self.next_state('rotate')
    #
    #@state
    #def rotate(self, initial_call):
    #    if initial_call:
    #        self.drive.reset_gyro_angle()
    #    
    #    if self.drive.align_to_tower():
    #        self.drive.disable_camera_tracking()
    #        self.next_state('stay_on_target')
    #
    #@timed_state(duration=2, next_state='drive_to_ramp')
    #def stay_on_target(self):
    #    self.drive.align_to_tower()
    #####   
    
    @state
    def rotate(self, initial_call):
        if initial_call:
            self.drive.reset_gyro_angle()
            self.drive.enable_camera_tracking()
            
        if self.drive.angle_rotation(self.RotateAngle):
            self.next_state('test_camera')
    
    @timed_state(duration = 1, next_state='drive_to_ramp')
    def test_camera(self):
        if self.present:
            self.next_state('rotate_to_align')
    
    @timed_state(duration=1, next_state='camera_drive')
    def rotate_to_align(self, initial_call):
        if initial_call:
            self.drive.reset_gyro_angle()
        
        if self.drive.align_to_tower():
            self.next_state('camera_drive')

    
    @state
    def camera_drive(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
        
        self.drive.align_to_tower()
        
        if self.drive.drive_distance(self.Ramp_Distance*12, max_speed=self.Max_Drive_Speed):
            self.next_state('lower_to_shoot')      
            
    @state
    def drive_to_ramp(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
            self.drive.disable_camera_tracking()
    
        if self.drive.drive_distance(self.Ramp_Distance*12, max_speed=self.Max_Drive_Speed):
            self.next_state('lower_to_shoot')
            
    @timed_state(duration = 1, next_state='shoot')
    def lower_to_shoot(self):
        self.intake.set_arm_middle()
        
        if self.intake.on_target():
            self.next_state('shoot')
        
    
    @timed_state(duration = 2, next_state='intakeBall')
    def shoot(self):
        self.intake.outtake()
    
    @timed_state(duration = 2, next_state = 'shoot')
    def intakeBall(self):
        self.intake.intake()
    