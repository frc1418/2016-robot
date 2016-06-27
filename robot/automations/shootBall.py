import components.intake as Intake
from magicbot import StateMachine, state, timed_state


class ShootBall(StateMachine):
    # Aliases
    intake = Intake.Arm

    def on_enable(self):
        """When initiated"""
        self.is_running = False

    def get_running(self):
        """Is ball being shot?"""
        return self.is_running

    def shoot(self):
        """When called, engage StateMachine to shoot"""
        self.engage()

    def stop(self):
        """When called, stop the ball shooting process"""
        self.done()

    @state(first=True, must_finish=True)
    # First state, lower arm.
    def lower_arms(self):
        """Lower arm in preparation for shot"""
        # Move arm to middle
        self.intake.set_arm_middle()
        # If close enough to desired position
        if self.intake.get_position() > 2000:
            # Move to shooting step
            self.next_state('fire')

    @timed_state(duration=1, must_finish=True)
    def fire(self):
        """Eject ball"""
        # Shoot it yo
        self.intake.outtake()