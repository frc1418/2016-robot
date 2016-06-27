import wpilib

# Define constants
ARM_DOWN = 1
DRIVE_ENC = 2
DRIVE = 3
ARM_MIDDLE = 4
ARM_UP = 5


class PortcullisLift:

    def __init__(self, sd, drive, intake, drive_speed=-.5):
        self.intake = intake
        self.drive = drive
        self.sd = sd

        # Get set speeds from NetworkTables
        self.drive_speed = self.sd.getAutoUpdateValue('Portcullis | Drive Speed', .3)
        self.drive_reverse_speed = self.sd.getAutoUpdateValue('Portcullis | Reverse Speed', -.05)
        self.drive_speed_2 = self.sd.getAutoUpdateValue('Portcullis | Drive Speed_2', .5)

        # By default, not running.
        self.is_running = False
        # Default state is first.
        self.state = ARM_DOWN

        # Start timer
        self.timer = wpilib.Timer()
        self.timer.start()

    def get_running(self):
        """Return True if portcullis lift is in progress, False if not"""
        return self.is_running

    def go(self):
        """Actually lift portcullis."""
        # Note that process is now running.
        self.is_running = True
        # If state machine is at 1, put arm at the bottom
        # Add state machine to put the arm at the bottom first
        if self.state == ARM_DOWN:
            # Move arm to lowest position
            self.intake.set_arm_bottom()
            # If arm has moved to desired position
            if self.intake.on_target():
                # Reset the timer
                self.timer.reset()
                # Move on to the next state
                self.state = DRIVE
        # If state machine is at 2, drive forward
        if self.state == DRIVE:
            # Move forward set amount
            self.drive.move(self.drive_speed.value, 0)
            # If robot is done moving that amount
            if self.timer.hasPeriodPassed(1):
                # Reset timer and switch to next state
                self.timer.reset()
                self.state = ARM_MIDDLE
        # If on third state, move arm up halfway and move a bit
        if self.state == ARM_MIDDLE:
            # Move forward predefined amount
            self.drive.move(self.drive_reverse_speed.value, 0)
            # Move arm to top
            self.intake.set_arm_top()
            # If halfway done, move to next state
            # (the reason it works like this is complicated and not important)
            if self.timer.hasPeriodPassed(.5):
                self.state = ARM_UP
        # If on final state
        if self.state == ARM_UP:
            # Move arm to top
            self.intake.set_arm_top()
            # If everything's done
            if self.drive.drive_distance(36):
                # Note that process has finished
                self.is_running = False
                # Switch state back to first
                self.state = ARM_DOWN