from robotpy_ext.autonomous import state, timed_state, StatefulAutonomous

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

class Portcullis(StatefulAutonomous):
    MODE_NAME = 'Portcullis'
    DEFAULT = True
    
    def initialize(self):
        self.register_sd_var('Drive_Distance', (54))
    
    @state(first = True)
    def drive_forward(self):
        if self.drive.drive_distance(self.Drive_Distance):
            self.next_state('raise_portcullis')
    
    @state
    def raise_portcullis(self, initial_call):
        if not initial_call and not self.portcullis.get_running():
            self.next_state('drive_forward_2')
        self.portcullis.doit()
            
            
    @timed_state(duration = 5)
    def drive_forward_2(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()
        self.drive.drive_distance(60)
            
    