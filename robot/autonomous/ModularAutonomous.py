from robotpy_ext.autonomous import state, timed_state, StatefulAutonomous
from .GenericAutonomous import LowBar, ChevalDeFrise, Portcullis
from components import intake as Intake, drive as Drive
from networktables.networktable import NetworkTable

class ModularAutonomous(LowBar, ChevalDeFrise, Portcullis):
    MODE_NAME = "Modular_Autonomous"
    DEFAULT = True
    
    sd = NetworkTable
    intake = Intake.Arm
    drive = Drive.Drive
    
    @state(first = True)
    def startModularAutonomous(self):
        #self.next_state(self.sd.getValue('robotDefense')+'Start')
        self.next_state('LowBarStart')
    
    @state
    def transition(self):
        # if self.sd.getNumber('robotPosition') > 3:
        if 2 > 3:
            self.rotateConst = 1
        else:
            self.rotateConst = -1
        self.next_state('rotate')
    
    @state
    def rotate(self):
        if self.drive.angle_rotation(90*self.rotateConst):
            self.drive.reset_drive_encoders()
            self.next_state('drive_to_position')
    
    @state
    def drive_to_position(self):
        if self.drive.drive_distance(50):
            self.next_state('rotate_back')
        self.drive.angle_rotation(90*self.rotateConst)
        
    @state
    def rotate_back(self):
        if self.drive.angle_rotation(0):
            #self.next_state('drive_to_line')
            self.done()