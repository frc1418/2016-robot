from robotpy_ext.autonomous import state, timed_state, StatefulAutonomous
from .GenericAutonomous import LowBar, ChevalDeFrise, Portcullis, Charge, Default
from components import intake as Intake, drive as Drive
from networktables.networktable import NetworkTable
from networktables.util import ntproperty

class ModularAutonomous(LowBar, ChevalDeFrise, Portcullis, Charge, Default):
    MODE_NAME = "Modular_Autonomous"
    DEFAULT = False
    
    sd = NetworkTable
    intake = Intake.Arm
    drive = Drive.Drive
    present = ntproperty('/components/autoaim/present', False)
    # robotDefense = ntproperty('/SmartDashboard/robotDefense', 'Default')
    # position = ntproperty('/SmartDashboard/robotPosition', 1)
    
    def initialize(self):
        LowBar.initialize(self)
        ChevalDeFrise.initialize(self)
        Portcullis.initialize(self)
        
    @state(first=True)
    def startModularAutonomous(self):
        print(self.sd.getValue('robotDefense', 'Default') + 'Start')
        self.intake.manualZero()
        self.drive.reset_gyro_angle()
        self.next_state(self.sd.getValue('robotDefense', 'LowBar') + 'Start')
        self.position = int(self.sd.getValue('robotPosition', '1'))
    @state
    def transition(self):
        # if self.sd.getNumber('robotPosition') > 2:
        if self.position > 2:
            self.rotateConst = 1
            self.drive_distance = (48 * (4 - self.position))
        else:
            self.drive_distance = (48 * (self.position - 1))
            self.rotateConst = -1
        if self.position == 1 or self.position == 4:
            self.next_state('drive_to_wall')
        else:
            self.next_state('rotate')
    
    @state
    def rotate(self):
        if self.drive.angle_rotation(90 * self.rotateConst):
            self.drive.reset_drive_encoders()
            self.next_state('drive_to_position')
    
    @state
    def drive_to_position(self):
        if self.drive.drive_distance(self.drive_distance):
            self.next_state('rotate_back')
        # self.drive.angle_rotation(90*self.rotateConst)
        # self.drive.angle_rotation(90*self.rotateConst)
        
        
    @state
    def rotate_back(self):
        if self.drive.angle_rotation(0):
            self.next_state('drive_to_wall')
    
    @state
    def drive_to_wall(self):
        if self.drive.wall_goto() < .1:
            self.next_state('reverse_to_angle')
            
    @state
    def reverse_to_angle(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
            self.intake.set_arm_middle()
        if self.drive.drive_distance(-25):
            self.next_state("find_tower")
    
    @state
    def find_tower(self, initial_call):
        if initial_call:
            self.drive.enable_camera_tracking()
            
        if not self.present:
            self.drive.move(0, -.7 * self.rotateConst)
        else:
            self.next_state('rotate_to_target')
    
    @state
    def rotate_to_target(self, initial_call):
        if initial_call:
            self.drive.reset_gyro_angle()
        
        if self.drive.align_to_tower():
            self.next_state('drive_to_goal')
    @state
    def drive_to_goal(self):
        if self.drive.drive_distance(2):
            self.next_state('shoot')
    
    @state
    def shoot(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
        self.drive.drive_distance(-2.5)
        self.intake.outtake()
               
class BallModularAutonomous(ModularAutonomous):   
    MODE_NAME = "Ball_Modular_Autonomous"
    DEFAULT = False
    
    sd = NetworkTable
    intake = Intake.Arm
    drive = Drive.Drive

    def initialize(self):
        LowBar.initialize(self)
        ChevalDeFrise.initialize(self)
        Portcullis.initialize(self)
        
        self.register_sd_var('Drive_Distance', -5)
        self.register_sd_var('Rotate_Angle', 180)
        self.register_sd_var('Collect_Distance', 0.5)

    @state(first=True)
    def startModularAutonomous(self):
        print(self.sd.getValue('robotDefense', 'Default') + 'Start')
        self.intake.manualZero()
        self.drive.reset_gyro_angle()
        self.next_state('drive_to_ball')
        
    @timed_state(duration = 4, next_state='lower_arms')
    def drive_to_ball(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
            self.intake.set_arm_middle()
            
        #Drive distance is negative here because we have to back up to make sure the arms dont extend too far!
        if self.drive.drive_distance(self.Drive_Distance):
            self.next_state('collect')
                
    @state
    def collect(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
            
        self.intake.intake()
        if self.drive.drive_distance(self.Collect_Distance):
            self.next_state('back_up')

    @state
    def back_up(self,initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
            
        if self.drive.drive_distance(-(self.Collect_Distance+self.Drive_Distance)):
            self.next_state('turn_around')
        
    @state
    def turn_around(self,initial_call):
        if initial_call:
            self.drive.reset_gyro_angle()
            
        if self.drive.angle_rotation(self.Rotate_Angle):
            self.next_state(self.sd.getValue('robotDefense', 'LowBar') + 'Start')
            self.position = int(self.sd.getValue('robotPosition', '1'))
            print('test '+(self.sd.getValue('robotDefense', 'LowBar') + 'Start'))
            print('test '+self.sd.getValue('robotPosition', '1'))
    