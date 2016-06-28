from magicbot import StateMachine, timed_state, state
from components import light, intake as Intake

class LightSwitch(StateMachine):
    # Aliases
    light = light.Light
    intake = Intake.Arm

    def on_enable(self):
        """Runs when light is initiated"""
        self.counter = 0

    def switch(self):
        """Turn off/on"""
        self.counter = 0
        self.engage()

    @state(first=True, must_finish=True)
    def firstState(self):
        """Figure out if it needs to turn on or off"""
        if self.light.on:
            self.next_state('off')
        else:
            self.light.turnOn()
            self.done()

    @timed_state(duration = .25, next_state='on', must_finish = True)
    def off(self, initial_call):
        """
            Turns light off.
            Needs to turn on and off two extra times to switch through the three
            flashlight intensities.
        """
        if initial_call:
            self.counter += 1

        self.light.turnOff()
        if self.counter > 2:
            self.done()

    @timed_state(duration = .25, next_state = 'off', must_finish = True)
    def on(self):
        """Turns light on. This doesn't need to switch multiple times."""
        self.light.turnOn()
