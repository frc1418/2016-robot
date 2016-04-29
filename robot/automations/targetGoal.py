from networktables.util import ntproperty
from components import drive, intake
from magicbot import StateMachine, state
from automations import shootBall
from magicbot.magic_tunable import tunable

class TargetGoal(StateMachine):
    
    
    intake = intake.Arm
    drive = drive.Drive
    shootBall = shootBall.ShootBall
    
    present = ntproperty('/components/autoaim/present', False)
    targetHeight = ntproperty('/components/autoaim/target_height', 0)
    
    
    idealHeight = tunable(-7)
    heightThreshold = tunable(-7)
    
    shoot = False
        
    def target(self):
        self.engage()
        self.shoot = False
        
    def target_shoot(self):
        self.engage()
        self.shoot = True
    
    @state(first=True)
    def align(self, initial_call):
        if initial_call:
            self.drive.enable_camera_tracking()
        
        if self.drive.align_to_tower() and self.shoot:
            self.next_state('camera_assisted_drive')
            
    @state
    def camera_assisted_drive(self):
        if self.targetHeight > self.heightThreshold:#> -12:
            self.drive.move(max(abs(self.idealHeight-self.targetHeight)/55, .5), 0)
            self.drive.align_to_tower()
        else:
            self.next_state('shoot')
    
    @state
    def shoot(self):
        self.drive.align_to_tower()
        self.shootBall.shoot()
    
    def done(self):
        self.drive.disable_camera_tracking()
        StateMachine.done(self)