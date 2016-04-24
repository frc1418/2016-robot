import components.intake as Intake
from magicbot import StateMachine, state, timed_state

class shootBall(StateMachine):
    intake = Intake.Arm
    
    def on_enable(self):
        self.is_running = False
        
    def get_running(self):
        return self.is_running
    
    def shoot(self):
        self.begin()
        
    def stop(self):
        self.done()    
        
    @state(first = True)
    def lower_arms(self):
        self.intake.set_arm_middle()
        if self.intake.get_position()>2000:
            self.next_state('fire')
            
    @timed_state(duration = 1)
    def fire(self):
        self.intake.outtake()