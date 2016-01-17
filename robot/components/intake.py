import wpilib
import enum
Forward = 1
Reverse = 2

class ArmMode(enum.Enum):
    MANUAL = 1
    AUTO = 2
class Intake(object):
    
    def __init__(self, leftBall, rightBall, arm):
        self.leftBall = leftBall
        self.rightBall = rightBall
       
        self.arm = arm
        self.arm.setPID(10,0,0)
        
        self.leftBallSpeed = 0
        self.rightBallSpeed = 0
        self.armState = 0
        
        self.target_index = None #The index we want the arm to and where it is at when you call it
        self.target_position = None
        self.positions = [1440,
                          800,
                          0]
        
        self.isCalibrated = False
        
        self.shootArmUp = False
        self.shooting = False
        
        self.mode = ArmMode.MANUAL
        self.last_mode = ArmMode.MANUAL
        self.want_auto = False
        self.manual_value = 0
        
    def get_target_position(self):
        return self.target_position
    
    
    def set_manual(self, value):
        self.manual_value = value
        
        
    def _calibrate(self):
        if not self.isCalibrated:
            if not self.arm.isFwdLimitSwitchClosed():
                self.arm.changeControlMode(wpilib.CANTalon.ControlMode.PercentVbus)
                raise
                self.set_manual(1)
            else:
                self.set_manual(0)
                self.arm.setSensorPosition(0)
                self.target_index = 2
                self.target_position = 0
                self.arm.changeControlMode(wpilib.CANTalon.ControlMode.Position)
                self.isCalibrated = True
    
    
    def _set_position(self, index):
        self.want_auto = True
        self.target_index = index
        self.target_position = self.positions[index]
        
        
    def _detect_position_index(self):
        if not self.isCalibrated:
            return None
        return self.target_index
    
    def on_target(self):
        '''
        :returns:  Is the encoder at the set target
        :rtype: Bool
        '''
        if abs(self.get_position()-self.target_position)<170:
            return True
        return False
    
    
    def raise_arm(self):
        index = self._detect_position_index()
        
        if index is None:
            index = 1
            
        if index == 2:
            self.target_index = 2
        else:
            self.target_index = index + 1
        
        self._set_position(self.target_index)
        
        
    def lower_arm(self):
        index = self._detect_position_index()
        
        if index is None:
            index = 0
            
        if index == 0:
            self.target_index = 0
        else:
            self.target_index = index - 1
        self._set_position(self.target_index)
    def intake(self):
        self.leftBallSpeed = Forward
        self.rightBallSpeed = Reverse
    
    
    def outtake(self):
        self.leftBallSpeed = Reverse
        self.rightBallSpeed = Forward
        
              
    def shoot(self):
        self.shooting = not self.shooting
            
    
    
    def doit(self):
        if self.want_auto:
            self.mode = ArmMode.AUTO
        
        if self.last_mode != self.mode:
            if self.mode == ArmMode.AUTO:
                if self.isCalibrated:
                    self.arm.changeControlMode(wpilib.CANTalon.ControlMode.Position)
        
        if self.mode == ArmMode.MANUAL:
            self.arm.set(self.manual_value)
                
        if self.mode == ArmMode.AUTO:
            self._calibrate()
            if self.shooting:
                if not self.shootArmUp:
                    self._set_position(1)
                    self.shootArmUp = True
                if self.on_target():
                    self.outtake()
                    self.lower_arm()
                    self.shooting = False
            if self.isCalibrated:
                self.arm.set(self.target_position)
        self.leftBall.set(self.leftBallSpeed)
        self.rightBall.set(self.rightBallSpeed)
        
        self.leftBallSpeed = 0
        self.rightBallSpeed = 0