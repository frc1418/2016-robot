from robotpy_ext.autonomous import state, timed_state, StatefulAutonomous
from components import intake, drive
import wpilib
from magicbot.magic_tunable import tunable

class LowBar(StatefulAutonomous):
    DEFAULT = False

    intake = intake.Arm
    drive = drive.Drive
    def initialize(self):
        self.register_sd_var('Drive_Distance', 17.8)
        self.register_sd_var('Rotate_Angle', 55)
        self.register_sd_var('Ramp_Distance', 8.4)

    @state
    def LowBarStart(self):
        self.next_state('lower_arm')

    @timed_state(duration = 1, next_state='drive_forward')
    def lower_arm(self, initial_call):
        self.intake.set_arm_bottom()

        if self.intake.on_target():
            self.next_state('drive_forward')

    @state
    def drive_forward(self):
        if self.drive.drive_distance(self.Drive_Distance*12):
            self.next_state('transition')

class ChevalDeFrise(StatefulAutonomous):
    DEFAULT = False

    """This autonomous utilizes the ultrasonic sensor mounted on the front
        of the robot to tell when we are ready to lower the arms"""

    intake = intake.Arm
    drive = drive.Drive

    ultrasonic = wpilib.AnalogInput

    targetDistance = tunable(.13)
    driveOnDistance = tunable(1)
    driveOffDistance = tunable(4)

    def drive_to_cheval(self):
        """Drives forward toward the cheval"""
        self.drive.move(.4, 0)
        if self.ultrasonic.getVoltage() < self.targetDistance:
            self.next_state('lower_arms')

    @state
    def lower_arms(self, initial_call):
        """Lowers arms onto cheval"""
        if initial_call:
            self.intake.set_arm_bottom()
        if self.intake.on_target():
            self.next_state('drive_on')

    @state
    def drive_on(self, initial_call):
        """Drives forward onto the cheval"""
        if initial_call:
            self.drive.reset_drive_encoders()
        if self.drive.drive_distance(self.driveOnDistance):
            self.next_state('raise_arms')

    @state
    def raise_arms(self, initial_call):
        """Raises arms to protect them when coming down"""
        self.intake.set_arm_top()
        self.next_state('drive_off')

    @state
    def drive_off(self, initial_call):
        """Drives off cheval"""
        if initial_call:
            self.drive.reset_drive_encoders()
        if self.drive.drive_distance(self.driveOffDistance*12):
            self.next_state('transition')


class Portcullis(StatefulAutonomous):
    DEFAULT = False

    intake = intake.Arm
    drive = drive.Drive
    def initialize(self):
        self.register_sd_var('A0_Drive_Encoder_Distance', 4.90)
        self.register_sd_var('A0_Arm_To_Position', 500)
        self.register_sd_var('A0_DriveThru_Speed', 0.4)

    @state
    def A0Start(self):
        self.next_state('A0_lower_arm')

    @timed_state(duration = 1.5, next_state='A0_drive_forward')
    def A0_lower_arm(self, initial_call):
        #self.intake.set_arm_bottom()
        self.intake.set_manual(1)

        #if self.intake.on_target():
        #    self.next_state('A0_drive_forward')

    @state
    def A0_drive_forward(self, initial_call):
        if initial_call:
            self.drive.reset_drive_encoders()

        self.drive.angle_rotation(0)
        if self.drive.drive_distance(self.A0_Drive_Encoder_Distance*12):
            self.next_state('A0_raise_arm')

    @timed_state(duration = 0.8, next_state='A0_drive_thru')
    def A0_raise_arm(self):
        self.intake.set_target_position(self.A0_Arm_To_Position)

        if self.intake.on_target():
            self.next_state('A0_drive_thru')

    @timed_state(duration = 3, next_state = 'transition')
    def A0_drive_thru(self):
        self.intake.set_arm_top()
        self.drive.angle_rotation(0)
        self.drive.move(self.A0_DriveThru_Speed, 0)
        #self.drive.angle_rotation(0)
class Charge(StatefulAutonomous):
    DEFAULT = False

    @timed_state(duration = 1.75)
    def E0Start(self, initial_call):
        self.drive.move(1,0)

class Default(StatefulAutonomous):
    DEFAULT = False

    @state
    def DefaultStart(self):
        pass