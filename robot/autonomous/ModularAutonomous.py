from robotpy_ext.autonomous import state, timed_state, StatefulAutonomous
from .GenericAutonomous import LowBar, ChevalDeFrise, Portcullis, Charge
from components import intake as Intake, drive as Drive
from networktables.networktable import NetworkTable

class ModularAutonomous(LowBar, ChevalDeFrise, Portcullis, Charge):
    MODE_NAME = "Modular_Autonomous"
    DEFAULT = False
    
    sd = NetworkTable
    intake = Intake.Arm
    drive = Drive.Drive
    
    def initialize(self):
        LowBar.initialize(self)
        ChevalDeFrise.initialize(self)
        Portcullis.initialize(self)
        self.position = 2
    @state(first = True)
    def startModularAutonomous(self):
        print(self.sd.getValue('robotDefense')+'Start')
        print("%s ROBOT POSITION" % self.position)
        self.intake.manualZero()
        self.drive.reset_gyro_angle()
        self.next_state(self.sd.getValue('robotDefense')+'Start')
        #self.next_state('LowBarStart')
    @state
    def transition(self):
        #if self.sd.getNumber('robotPosition') > 2:
        if self.position > 3:
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
        if self.drive.drive_distance(-20):
            self.next_state("rotate_to_goal")
    
    @state
    def rotate_to_goal(self):
        self.intake.set_arm_middle()
        if self.drive.angle_rotation(-60*self.rotateConst):
            self.next_state('drive_to_goal')
            
    @state
    def drive_to_goal(self):
        if self.drive.drive_distance(5):
            self.next_state('shoot')
    
    @state
    def shoot(self):
        self.intake.outtake()
               