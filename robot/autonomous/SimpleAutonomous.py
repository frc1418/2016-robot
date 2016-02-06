from robotpy_ext.autonomous import state, timed_state, StatefulAutonomous
import wpilib

class LowGoal(StatefulAutonomous):
    MODE_NAME='Low Goal'
    DEFAULT = False
    
    def initialize(self):
        self.register_sd_var('Drive_Distance', 15*12)
    
    @timed_state(duration = 10, next_state='rotate', first = True)
    def drive_forward(self):
        #self.intake.set_arm_middle()
        if self.drive.drive_distance(15*12):
            pass
            #self.next_state('rotate')
            #self.next_state('rotate')
        #self.drive.move(1, 0)
        #self.drive.angle_rotation(0)
    
    #@timed_state(duration = 2)
    #def rotate(self):
    #    self.drive.angle_rotation(0)

class DirectPortcullis(StatefulAutonomous):
    MODE_NAME = "DirectPorcullis"
    DEFAULT = True
    
    def initialize(self):
        self.register_sd_var("Drive_Encoder_Distance", 2.45)
        self.register_sd_var("DriveThru_Encoder_Distance", 5)
        self.register_sd_var("Drive_Encoder_Thresh", 100)
        self.register_sd_var("P", 2)
        self.register_sd_var("I", 0)
        self.register_sd_var("D", 0)
        
        
        
    #self.lf_motor.setPID(self.P, self.I, self.D)
    #self.lr_motor.changeControlMode(wpilib.CANTalon.ControlMode.Follower)
    #self.rf_motor.setPID(self.P, self.I, self.D)
    #self.rr_motor.changeControlMode(wpilib.CANTalon.ControlMode.Follower)
    
    @state(first = True)
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
   
    @state
    def drive_thru(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
        self.intake.set_arm_top()
            
        if self.drive.drive_distance(self.DriveThru_Encoder_Distance*12):
            self.next_state('end')
    
    @timed_state(duration = 5)
    def end(self):
        pass
        
        
            
        
            
    