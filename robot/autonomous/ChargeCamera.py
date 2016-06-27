from automations import targetGoal
from robotpy_ext.autonomous import state, timed_state, StatefulAutonomous
from components import intake, drive as Drive

class ChargeCamera(StatefulAutonomous):
    MODE_NAME = 'ChargeCamera'
    DEFAULT = False

    intake = intake.Arm
    drive = Drive.Drive
    targetGoal = targetGoal.TargetGoal

    def initialize(self):
        self.register_sd_var('Rotate_Angle', -40)
        self.register_sd_var('Max_Drive_Speed', .5)
        self.register_sd_var('Drive_Distance', 10)

    @timed_state(duration = 2, first = True, next_state='drive_forward')
    def charge(self, initial_call):
        self.drive.move(1,0)

    @state
    def drive_forward(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()

        if self.drive.drive_distance(self.Drive_Distance*12, max_speed=self.Max_Drive_Speed):
            self.next_state('rotate')
        else:
            self.drive.angle_rotation(0)

    @state
    def rotate(self):
        if self.drive.angle_rotation(self.Rotate_Angle) or self.targetGoal.present:
            self.next_state('autoshoot')

    @state
    def autoshoot(self):
        self.targetGoal.target_shoot()
