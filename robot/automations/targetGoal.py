from networktables.util import ntproperty
from components import drive, intake
from magicbot import StateMachine, state
from automations import shootBall
from magicbot.magic_tunable import tunable


class TargetGoal(StateMachine):
    # Aliases
    intake = intake.Arm
    drive = drive.Drive
    shootBall = shootBall.ShootBall

    # Fetch NetworkTables values
    present = ntproperty('/components/autoaim/present', False)
    targetHeight = ntproperty('/components/autoaim/target_height', 0)

    idealHeight = tunable(-7)
    heightThreshold = tunable(-7)

    shoot = False

    def target(self):
        """When called, seek target"""
        self.engage()
        self.shoot = False

    def target_shoot(self):
        """When called, seek target then shoot"""
        self.engage()
        self.shoot = True

    @state(first=True)
    def align(self, initial_call):
        """First state: turn robot to be facing tower"""
        # If it's the first time
        if initial_call:
            # Then turn on vision system
            self.drive.enable_camera_tracking()

        # If it's inline with the tower and it's been told to shoot when done aiming,
        if self.drive.align_to_tower() and self.shoot:
            # Then move on to shooting state.
            self.next_state('camera_assisted_drive')

    @state
    def camera_assisted_drive(self):
        """Second state: go forward to shooting location"""
        # If target is close
        if self.targetHeight > self.heightThreshold:
            # Move forward, guided by threshold
            self.drive.move(max(abs(self.idealHeight-self.targetHeight)/55, .5), 0)
            # Align to tower. Pretty self explanitory.
            self.drive.align_to_tower()
        else:
            # Otherwise, move on to next step, shooting.
            self.next_state('shoot')

    @state
    def shoot(self):
        """Align to tower and fire ball."""
        self.drive.align_to_tower()
        self.shootBall.shoot()

    def done(self):
        """Finish up, disable everything."""
        # Kill camera tracking
        self.drive.disable_camera_tracking()
        # Stop state machine
        StateMachine.done(self)