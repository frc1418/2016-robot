from robotpy_ext.autonomous import timed_state, StatefulAutonomous

class LowGoal(StatefulAutonomous):
    MODE_NAME='Low Goal'
    DEFAULT = True
    
    def initialize(self):
        pass
    
    @timed_state(duration = 10, next_state='rotate', first = True)
    def drive_forward(self):
        self.intake.set_arm_middle()
        if self.drive.drive_distance(60):
            pass
            #self.next_state('rotate')
        #self.drive.move(1, 0)
        #self.drive.angle_rotation(0)
    
    @timed_state(duration = 2)
    def rotate(self):
        self.drive.angle_rotation(-45)