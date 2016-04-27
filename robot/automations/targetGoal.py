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
    
    
    idealHeight = tunable(-11)
    heightThreshold = tunable(10)
    
    def on_enable(self):
        self.atGoal = False
        
    def target(self):
        if not self.drive.enable_camera:
            self.drive.enable_camera_tracking()
        if self.present or self.atGoal:
            self.engage()
    
    
    @state(first = True)
    def lower_arms(self):
        self.intake.set_arm_middle()
        if self.intake.get_position()>2000:
            self.next_state('align')
    
    @state
    def align(self):
        if self.drive.align_to_tower():
            self.next_state('camera_assisted_drive')
            
    @state
    def camera_assisted_drive(self):
        if self.targetHeight < self.heightThreshold:#> -12:
            self.drive.move(max(abs(self.idealHeight-self.targetHeight)/55, .5), 0)
            #self.drive.align_to_tower()
        else:
            self.atGoal = True
            self.next_state('shoot')
    
    @state
    def shoot(self):
        self.shootBall.shoot()
    