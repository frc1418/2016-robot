from pyfrc.physics.drivetrains import four_motor_drivetrain
import wpilib

class PhysicsEngine:
    
    
    def __init__(self, controller):
        self.controller = controller
        
        # keep track of the tote encoder position
        
        # keep track of the can encoder position
        self.armAct = 500
        self.prev_armAct = 500
        
        self.controller.add_device_gyro_channel('navxmxp_spi_4_angle')
        self.iErr = 0
    def update_sim(self, hal_data, now, tm_diff):
        # Simulate the arm
        try:
            armDict = hal_data['CAN'][25] # armDict is the dictionary of variables assigned to CANTalon 25
            lfDict = hal_data['CAN'][5]
            rfDict = hal_data['CAN'][15]
            
            armPercentVal = int(armDict['value']*tm_diff*2) # Encoder position increaser when in PercentVbus mode based on time and thrust value
            posVal = int(tm_diff*1023) # Encoder Position difference when in Position mode based on time
            armDict['limit_switch_closed_for'] = True
            armDict['limit_switch_closed_rev'] = True
            
            lWheelPercentVal = int(lfDict['value']*tm_diff*10)
            rWheelPercentVal = int(rfDict['value']*tm_diff*10)
    
        except:
            pass
        
        else:
            
            if armDict['mode_select'] == wpilib.CANTalon.ControlMode.PercentVbus: # If manual operation
                self.armAct += armPercentVal # Add the calculated encoder change value to the 'actual value'
                armDict['enc_position'] += armPercentVal # Add the calculated encoder change value to the recorded encoder value
            elif armDict['mode_select'] == wpilib.CANTalon.ControlMode.Position: #If in auto mode
                #err = armDict['value'] - armDict['enc_position']
                #self.iErr +=err*tm_diff
                #self.iErr = max(min(self.iErr, 300), -300)
                #output = (armDict['params'][1]*err)+(armDict['params'][2]*self.iErr)*250/(1023)
                #if abs(output) < 300:
                #    output = 0
                if armDict['enc_position'] < armDict['value']: #If the current position is less than the target position
                    armDict['enc_position'] += posVal # Add calculated encoder value to recorded value
                    self.armAct += posVal
                else: # If the current position is more than the target position
                    armDict['enc_position'] -= posVal # Subtract calculated encoder position
                    self.armAct -=posVal
                #output*=tm_diff
                #armDict['enc_position'] += output
                #armDict['enc_position'] = int(armDict['enc_position'])
                #self.armAct += output
            if self.armAct in range(-50, 0): # If the measured encoder value is within this range
                armDict['limit_switch_closed_rev'] = False # Fake closing the limit switch
                armDict['enc_position'] = 0
            if self.armAct in range(2700, 2800):
                armDict['limit_switch_closed_for'] = False
                armDict['enc_position'] = 2764
            
            lfDict['analog_in_position']+=lWheelPercentVal
            rfDict['analog_in_position']+=rWheelPercentVal
              
            #armDict['enc_position'] = max(min(armDict['enc_position'], 1440), 0) # Keep encoder between these values
            self.armAct = max(min(self.armAct, 2764), 0)
            armDict['enc_velocity'] = ((self.armAct - self.prev_armAct) / tm_diff)/1440
            self.prev_armAct = self.armAct
        
        
        # Simulate the drivetrain
        lf_motor = -hal_data['CAN'][5]['value']/1023
        lr_motor = -hal_data['CAN'][10]['value']/1023
        rf_motor = -hal_data['CAN'][15]['value']/1023
        rr_motor = -hal_data['CAN'][20]['value']/1023
        
        fwd, rcw = four_motor_drivetrain(lr_motor, rr_motor, lf_motor, rf_motor)
        self.controller.drive(fwd, rcw, tm_diff)