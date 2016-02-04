
import wpilib
from networktables.networktable import NetworkTable
import logging
logger = logging.getLogger("arm")

forward = 1
reverse = -1
off = wpilib.Relay.Value.kOff


class ArmMode:
    MANUAL = 1
    AUTO = 2

class Arm:
    
    def __init__ (self, motor, followMotor, leftBallMotor, init_down_speed):
        
        
        self.target_position = None
        self.target_index = None
        
        self.init_down_speed = init_down_speed
        
        self.isCalibrating = False
        self.isCalibrated = False
        
        self.want_manual = False
        self.manual_value = 0
        
        self.want_auto = False
        
        self.mode = ArmMode.MANUAL
        self.last_mode = ArmMode.MANUAL
        
        #self.manual_value = -.25
        self.manual_value = 0
        # These need to be set by subclasses
        self.wanted_pid = None
        self.current_pid = (0, 0, 0)
        self.new_pid = None
        
        self.sd = NetworkTable.getTable('SmartDashboard')
        
        self.motor = motor
        self.followMotor = followMotor
        self.followMotor.changeControlMode(wpilib.CANTalon.ControlMode.Follower)
        self.followMotor.reverseOutput(True)
        self.leftBallMotor = leftBallMotor
        
        self.now_enc = 0
        
        self.leftBallSpeed = 0
                
        self.positions = [
            self.sd.getAutoUpdateValue('Arm | Bottom', 25),
            self.sd.getAutoUpdateValue('Arm | Middle', -230),
            self.sd.getAutoUpdateValue('Arm | Top', -1200),
          ]
        self.position_threshold = self.sd.getAutoUpdateValue("Arm|On Target Threshold", 170)
        self.wanted_pid = (
            self.sd.getAutoUpdateValue('Arm |P', 2),
            self.sd.getAutoUpdateValue('Arm |I', 0), 
            self.sd.getAutoUpdateValue('Arm |D', 0)
        )
        
        self.calibrate_timer = wpilib.Timer()
        self.time_calibrating = 0
        self.start = 0
        self.calibrate_error = False
        self.enc_avg = []
    
    def set_arm_top(self):
        self._set_position(2)
        
    def set_arm_middle(self):
        self._set_position(1)
        
    def set_arm_bottom(self):
        self._set_position(0)
    
    def get_limit_switch(self):
        return self.limit.get()
    
    def get_position(self):
        '''
        :returns: Tote lift encoder position
        :rtype: int
        '''
        return self.motor.getEncPosition()
    def get_target_position(self):
        return self.target_position
    
    def set_manual(self, value):
        '''
            :param value: Motor value between -1 and 1
        '''
        self.want_manual = True
        self.manual_value = value
    
    
    def _detect_position_index(self, offset, pos_idx):
        '''Returns the current position index'''
        
        if self.mode == ArmMode.AUTO:
            return self.target_index
        
        if not self.isCalibrated:
            return None
        
        # If we're not in auto mode, we need to try and detect where the arm is... 
        current_pos = self.get_position()
        
        for i, pos in enumerate(self.positions):
            pos_value = pos.value
            if current_pos < pos_value + offset:
                return i + pos_idx
            
        return (len(self.positions) - 1) + pos_idx
    
    def raise_arm(self):
        '''Raises the arm by one position'''   
        target_index = self._detect_position_index(30, -1)
        if target_index == -1:
            target_index = 0
        
        if target_index is None:
            index = 1
        else:
            index = target_index + 1
            
        if index >= len(self.positions):
            index = len(self.positions)-1
        
        self._set_position(index)
        
    
    def lower_arm(self):
        '''Lowers the arm by one position'''
        
        target_index = self._detect_position_index(-30, 0)
        
        if target_index is None:
            index = 0
        else:
            index = target_index - 1
            
        if index < 0:
            index = 0
        
        self._set_position(index)
    
    def _set_position(self, index):
        '''Sets position to index of positions list'''
        self.want_auto = True
        self.target_index = index
        self.target_position = self.positions[index].value 
        
    def on_target(self):
        '''
        :returns:  Is the encoder at the set target
        :rtype: Bool
        '''
        if abs(self.get_position()-self.target_position)< self.position_threshold.value:
            return True
        elif self.target_index == 0 and self.motor.isFwdLimitSwitchClosed():
            return True
        elif self.target_index == 2 and self.motor.isRevLimitSwitchClosed():
            return True
        
        return False
    
    def overide_calibrate(self):
        '''in case of calibration faliure, this can be called to ignore it.'''
        self.motor.set(0)
        self.motor.setSensorPosition(0)
            
        self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Position)
        self.isCalibrated = True

    
    def _calibrate(self):
        '''Moves the motor towards the limit switch to reset the encoder to 0'''
        if not self.isCalibrated:
            if not self.isCalibrating:
                self.calibrate_timer.start()
                self.isCalibrating = True
            
            if self.calibrate_timer.hasPeriodPassed(3):
                ArmMode.AUTO = ArmMode.MANUAL
                self.set_manual(0)
                self.mode = ArmMode.MANUAL
            
            if not self.motor.isFwdLimitSwitchClosed():
                self.motor.set(1)
                
            else:
                self.motor.set(0)
                self.motor.setSensorPosition(0)
            
                self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Position)
                self.isCalibrated = True
                self.isCalibrating = False
    
    def intake(self):
        self.leftBallSpeed = reverse
    
    def outtake(self):
        self.leftBallSpeed = forward

    def manualZero(self):
        self.motor.set(0)
        self.motor.setSensorPosition(0)
    
        self.isCalibrated = True
        
        self.on_calibrate()
        
    def test_enc(self):
        self.want_auto = True
        self.target_position = self.motor.getEncPosition()-13    
    
        
    def doit(self):
        '''Actually does stuff'''
        #self.followMotor.reverseOutput(self.followMotorReverse)
        if self.want_manual:
            self.mode = ArmMode.MANUAL
        elif self.want_auto:
            self.mode = ArmMode.AUTO
            
        if self.last_mode != self.mode:
            if self.mode == ArmMode.AUTO:
                self.new_pid = [e.value for e in self.wanted_pid]
                if self.isCalibrated:
                    # Only switch the control mode if we're not calibrating!
                    self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Position)
            if self.mode == ArmMode.MANUAL:
                self.motor.changeControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
            if self.mode != ArmMode.MANUAL and self.mode != ArmMode.AUTO:
                raise ValueError("INVALID MODE")
                
            self.last_mode = self.mode
            
        if self.mode == ArmMode.MANUAL:
            self.motor.set(self.manual_value)
            self.target_index = -1
            if self.isCalibrated:
                self.mode = ArmMode.AUTO
                self.target_position = self.motor.getEncPosition()
        
        elif self.mode == ArmMode.AUTO:
            self._calibrate()
            
            if self.isCalibrated:
                
                # Update the PID values if necessary
                if self.current_pid != self.new_pid:
                    self.motor.setPID(*self.new_pid)
                    self.current_pid = self.new_pid
                self.motor.set(self.target_position)
                
        else:
            self.motor.set(0)
        
        if self.motor.isFwdLimitSwitchClosed():
            self.motor.setSensorPosition(0)
            
        if self.motor.isRevLimitSwitchClosed():
            self.motor.setSensorPosition(-1140)
            
        self.followMotor.set(self.motor.getDeviceID())
        
        self.leftBallMotor.set(self.leftBallSpeed)
        
        self.leftBallSpeed = off
            
        self.want_auto = False
        self.want_manual = False
        
        self.manual_value = 0
        
        self.update_sd("Arm")
        
    def update_sd(self, name):
        '''Puts refreshed values to SmartDashboard'''
        self.sd.putValue('Arm|Manual Value', self.manual_value)
        self.sd.putValue('%s|Encoder' % name, self.motor.getEncPosition())
        self.sd.putValue("Arm|Reverse Limit Switch", self.motor.isRevLimitSwitchClosed())
        self.sd.putValue("Arm|Forward Limit Switch", self.motor.isFwdLimitSwitchClosed())
        self.sd.putValue('%s|Calibrated' % name, self.isCalibrated)
        self.sd.putValue('Arm|Encoder Velocity', self.motor.getEncVelocity())
        
        if self.target_position is None:
            self.sd.getAutoUpdateValue('%s|Target Position' % name, -1)
        else:
            self.sd.getAutoUpdateValue('%s|Target Position' % name, self.target_index)
        