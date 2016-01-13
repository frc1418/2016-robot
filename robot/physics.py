from pyfrc.physics.drivetrains import four_motor_drivetrain

class PhysicsEngine:
    
    
    def __init__(self, controller):
        self.controller = controller
        
        # keep track of the tote encoder position
        
        # keep track of the can encoder position
        
    
    def update_sim(self, hal_data, now, tm_diff):
        
        # Simulate the tote forklift
        
        # Simulate the can forklift
        
        # Do something about the distance sensors?
        
        
        # Simulate the drivetrain
        lf_motor = hal_data['pwm'][0]['value']*-1
        lr_motor = hal_data['pwm'][1]['value']*-1
        rf_motor = -hal_data['pwm'][2]['value']
        rr_motor = -hal_data['pwm'][3]['value']
        
        fwd, rcw = four_motor_drivetrain(lr_motor, rr_motor, lf_motor, rf_motor)
        self.controller.drive(fwd, rcw, tm_diff)