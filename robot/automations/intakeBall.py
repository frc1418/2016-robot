import wpilib

# Define step numbers for state machine.
START_SPIN = 0
ARM_DOWN = 1
ARM_UP = 2


class IntakeBall():
    def __init__(self, intake):
        self.intake = intake
        self.is_running = False
        self.state = START_SPIN
        self.timer = wpilib.Timer()
        self.timer.start()

    def get_running(self):
        """Return bool: is intake currently running?"""
        return self.is_running

    def go(self):
        """Actually intake ball."""
        # Tell program ball intake is running.
        self.is_running = True

        # If state machine is at 0, start spinning intake motor
        if self.state == START_SPIN:
            # Reset timer
            self.timer.reset()
            # Start motor
            self.intake.intake()
            # If time is up, move on to the next step
            if self.timer.hasPeriodPassed(1):
                self.state = ARM_DOWN
        # If state machine is at 1, put arm down
        if self.state == ARM_DOWN:
            # Move arm to middle position
            self.intake.set_arm_middle()
            # Spin intake motor
            self.intake.intake()
            # If time is up, move on to next step
            if self.timer.hasPeriodPassed(2):
                self.state = ARM_UP
        # If state machine is at 2, put arm back up
        if self.state == ARM_UP:
            # Move arm to top position
            self.intake.set_arm_top()
            # If arm has reached desired position
            if self.intake.on_target():
                # Note that ball intake has finished.
                self.is_running = False
                # Reset statemachine
                self.state = 0