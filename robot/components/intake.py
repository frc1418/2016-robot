
import wpilib
from networktables.networktable import NetworkTable
import logging
logger = logging.getLogger("arm")
import enum

forward = wpilib.Relay.Value.kForward
reverse = wpilib.Relay.Value.kReverse
off = wpilib.Relay.Value.kOff


class ArmMode(enum.Enum):
    MANUAL = 1
    AUTO = 2

class Arm:
    
    def __init__ (self, motor, followMotor, leftBallMotor, rightBallMotor, init_down_speed):
        
        
        self.target_position = None
        self.target_index = None
        
        self.init_down_speed = init_down_speed
        
        self.isCalibrated = False
        
        self.want_manual = False
        self.manual_value = 0
        
        self.want_auto = False
        
        self.mode = ArmMode.MANUAL
        self.last_mode = ArmMode.MANUAL
        
        # These need to be set by subclasses
        self.wanted_pid = None
        self.current_pid = (0, 0, 0)
        self.new_pid = None
        
        self.sd = NetworkTable.getTable('SmartDashboard')
        
        self.motor = motor
        self.followMotor = followMotor
        self.followMotor.changeControlMode(wpilib.CANTalon.ControlMode.Position)
        self.leftBallMotor = leftBallMotor
        self.rightBallMotor = rightBallMotor
        
        self.leftBallSpeed = 0
        self.rightBallSpeed = 0
                
        self.positions = [
            self.sd.getAutoUpdateValue('Arm | Bottom', 1440),
            self.sd.getAutoUpdateValue('Arm | Middle', 800),
            self.sd.getAutoUpdateValue('Arm | Top', 0),
            self.sd.getAutoUpdateValue('Encoder Pos', self.motor.getEncPosition()),
            self.sd.getAutoUpdateValue('Arm fwd Limit Switch', self.motor.isFwdLimitSwitchClosed()),
            self.sd.getAutoUpdateValue('Arm rev Limit Switch', self.motor.isRevLimitSwitchClosed())
          ]
        
        self.wanted_pid = (
            self.sd.getAutoUpdateValue('Arm |P', 10),
            self.sd.getAutoUpdateValue('Arm |I', 0), 
            self.sd.getAutoUpdateValue('Arm |D', 0)
        )
        
            
    
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
        target_index = self._detect_position_index(-170, -1)
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
        
        target_index = self._detect_position_index(170, 0)
        
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
        if abs(self.get_position()-self.target_position)<170:
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
            if not self.motor.isFwdLimitSwitchClosed():
                self.motor.set(self.init_down_speed)
            else:
                self.motor.set(0)
                self.motor.setSensorPosition(0)
            
                self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Position)
                self.isCalibrated = True
    
    def intake(self):
        self.leftBallSpeed = forward
        self.rightBallSpeed = reverse
    
    def outtake(self):
        self.leftBallSpeed = reverse
        self.rightBallSpeed = forward

    def manualZero(self):
        self.motor.set(0)
        self.motor.setSensorPosition(0)
    
        self.isCalibrated = True
        
        self.on_calibrate()

                
    def doit(self):
        '''Actually does stuff'''
        if self.want_manual:
            self.mode = ArmMode.MANUAL
        elif self.want_auto:
            self.mode = ArmMode.AUTO
            
        if self.last_mode != self.mode:
            if self.mode == ArmMode.MANUAL:
                self.motor.changeControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
            elif self.mode == ArmMode.AUTO:
                self.new_pid = [e.value for e in self.wanted_pid]
                if self.isCalibrated:
                    # Only switch the control mode if we're not calibrating!
                    self.motor.changeControlMode(wpilib.CANTalon.ControlMode.Position)
            else:
                raise ValueError("INVALID MODE")
                
            self.last_mode = self.mode
            
        if self.mode == ArmMode.MANUAL:
            self.motor.set(self.manual_value)
            self.target_index = -1
        
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
        
        self.followMotor.set(self.motor.getEncPosition())
        self.leftBallMotor.set(self.leftBallSpeed)
        self.rightBallMotor.set(self.rightBallSpeed)
        
        self.leftBallSpeed = off
        self.rightBallSpeed = off
            
        self.want_auto = False
        self.want_manual = False
        self.manual_value = 0
        
    def update_sd(self, name):
        '''Puts refreshed values to SmartDashboard'''
        self.sd.putNumber('%s|Encoder' % name, self.motor.getEncPosition())
        self.sd.putBoolean('%s|Calibrated' % name, self.isCalibrated)
        self.sd.putBoolean('%s|Manual' % name, self.mode == ArmMode.MANUAL)
        self.sd.putBoolean('%s|Limit' % name, self.get_limit_switch())
        
        if self.target_position is None:
            self.sd.putNumber('%s|Target Position' % name, -1)
        else:
            self.sd.putNumber('%s|Target Position' % name, self.target_index)
        