from robotpy_ext.autonomous import state, timed_state, StatefulAutonomous
from components import intake, drive as Drive
import wpilib
from networktables import NetworkTable
from magicbot.magic_tunable import tunable

class ChevalDeFrise(StatefulAutonomous):
    MODE_NAME = "ChevalDeFrise"
    DEFAULT = False
    
    intake = intake.Arm
    drive = Drive.Drive
    
    def initialize(self):
        self.register_sd_var("Drive_to_distance", 4.2)
        self.register_sd_var("Drive_on_distance", 1)
        
    @timed_state(duration = 2, next_state='lower_arms', first = True)
    def drive_to(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
        
        if self.drive.drive_distance(self.Drive_to_distance*12):
            self.next_state('lower_arms')
            
    @timed_state(duration = .4, next_state='drive_on')
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
        
    @timed_state(duration = 2)
    def drive_over(self, initial_call):
        self.intake.set_arm_top()
        
        self.drive.move(0.7, 0)

class SonicCheval(StatefulAutonomous):
    MODE_NAME = "SonicCheval"
    DEFAULT = False
    
    '''This autonomous utilizes the ultrasonic sensor mounted on the front
        of the robot to tell when we are ready to lower the arms'''
    
    intake = intake.Arm
    drive = Drive.Drive
    
    ultrasonic = wpilib.AnalogInput
    
    targetDistance = tunable(.13)
    driveOnDistance = tunable(1)
    driveOffDistance = tunable(4)
    
    @state(first = True)
    def drive_to_cheval(self):
        '''Drives forward toward the cheval'''
        self.drive.move(.4, 0)
        if self.ultrasonic.getVoltage() < self.targetDistance:
            self.next_state('lower_arms')
    
    @state
    def lower_arms(self, initial_call):
        '''Lowers arms onto cheval'''
        if initial_call:
            self.intake.set_arm_bottom()
        if self.intake.on_target():
            self.next_state('drive_on')
    
    @state
    def drive_on(self, initial_call):
        '''Drives forward onto the cheval'''
        if initial_call:
            self.drive.reset_drive_encoders()
        if self.drive.drive_distance(self.driveOnDistance):
            self.next_state('raise_arms')
    
    @state
    def raise_arms(self, initial_call):
        '''Raises arms to protect them when coming down'''
        self.intake.set_arm_top()
        self.next_state('drive_off')
    
    @state
    def drive_off(self, initial_call):
        '''Drives off cheval'''
        if initial_call:
            self.drive.reset_drive_encoders()
        self.drive.drive_distance(self.driveOffDistance*12)

class ArmCheval(StatefulAutonomous):
    MODE_NAME = "ArmCheval"
    DEFAULT = False
    
    intake = intake.Arm
    drive = Drive.Drive
    
    def initialize(self):
        #TODO: Figure out positions for the arm
        self.register_sd_var("Correct_arm_position", 2700)
        self.register_sd_var("Drive_on_distance", 1)
        
    @timed_state(duration = 2, next_state='drive_back', first = True)
    def drive_to(self, initial_call):
        self.drive.move(0.3,0)
        
    @state
    def drive_back(self, initial_call):
        self.intake.set_arm_bottom()
        self.drive.move(-0.2,0)
        
        if self.intake.get_position() > self.Correct_arm_position:
            self.next_state('drive_on')
        
    @timed_state(duration = 2, next_state='drive_over')
    def drive_on(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
            
        if self.drive.drive_distance(self.Drive_on_distance*12):
            self.next_state('drive_over')
        
    @timed_state(duration = 2)
    def drive_over(self, initial_call):
        self.intake.set_arm_top()
        
        self.drive.move(0.7, 0)  