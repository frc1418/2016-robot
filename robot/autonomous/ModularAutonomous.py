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
    #robotDefense = ntproperty('/SmartDashboard/robotDefense', 'Default')
    #position = ntproperty('/SmartDashboard/robotPosition', 1)
    
    def initialize(self):
        LowBar.initialize(self)
        ChevalDeFrise.initialize(self)
        Portcullis.initialize(self)
        
    @state(first = True)
    def startModularAutonomous(self):
        print(self.sd.getValue('robotDefense', 'Default')+'Start')
        self.intake.manualZero()
        self.drive.reset_gyro_angle()
        self.next_state(self.sd.getValue('robotDefense', 'LowBar')+'Start')
        self.position = int(self.sd.getValue('robotPosition', '1'))
    @state
    def transition(self):
        #if self.sd.getNumber('robotPosition') > 2:
        if self.position > 2:
            self.rotateConst = 1
            self.drive_distance = (48*(4-self.position))
        else:
            self.drive_distance = (48*(self.position-1))
            self.rotateConst = -1
        if self.position == 1 or self.position == 4:
            self.next_state('drive_to_wall')
        else:
            self.next_state('rotate')
    
    @state
    def rotate(self):
        if self.drive.angle_rotation(90*self.rotateConst):
            self.drive.reset_drive_encoders()
            self.next_state('drive_to_position')
    
    @state
    def drive_to_position(self):
        if self.drive.drive_distance(self.drive_distance):
            self.next_state('rotate_back')
        #self.drive.angle_rotation(90*self.rotateConst)
        #self.drive.angle_rotation(90*self.rotateConst)
        
        
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
        if self.drive.drive_distance(-25):
            self.next_state("rotate_to_goal")
    
    @state
    def rotate_to_goal(self):
        #self.intake.set_arm_middle()
        self.intake.set_target_position(2300)
        
        if self.drive.angle_rotation(-55*self.rotateConst):
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
               