from robotpy_ext.autonomous import state, timed_state, StatefulAutonomous
from components import intake, drive as Drive
import wpilib
from networktables import NetworkTable

class DirectPortcullis(StatefulAutonomous):
    MODE_NAME = 'DirectPorcullis'
    DEFAULT = False

    intake = intake.Arm
    drive = Drive.Drive
    def initialize(self):
        self.register_sd_var('Drive_Encoder_Distance', 4.10)
        self.register_sd_var('Arm_To_Position', 1000)
        self.register_sd_var('DriveThru_Speed', 0.4)

    @timed_state(duration = 2, next_state='drive_forward', first = True)
    def lower_arm(self, initial_call):
        self.intake.set_arm_bottom()

        if self.intake.on_target():
            self.next_state('drive_forward')

    @state
    def drive_forward(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()

        if self.drive.drive_distance(self.Drive_Encoder_Distance*12):
            self.next_state('raise_arm')

    @timed_state(duration = 0.5, next_state='drive_thru')
    def raise_arm(self):
        self.intake.set_target_position(self.Arm_To_Position)

        if self.intake.on_target():
            self.next_state('drive_thru')

    @timed_state(duration = 5)
    def drive_thru(self):
        self.intake.set_arm_top()

        self.drive.move(self.DriveThru_Speed, 0)