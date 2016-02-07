import wpilib

from networktables import NetworkTable
from common.driveEncoders import DriveEncoders
import math

ENCODER_ROTATION = 1023
WHEEL_DIAMETER = 7.639
class Drive:
	'''
		The sole interaction between the robot and its driving system
		occurs here. Anything that wants to drive the robot must go
		through this class.
	'''	

	def __init__(self, robotDrive, navx, rf_encoder, lf_encoder):
		'''
			Constructor. 
			
			:param robotDrive: a `wpilib.RobotDrive` object
			:type rf_encoder: DriveEncoders()
			:type lf_encoder: DriveEncoders()
			
		'''
		self.sd = NetworkTable.getTable('SmartDashboard')
		self.isTheRobotBackwards = False
		# set defaults here
		self.y = 0
		self.rotation = 0
		self.squaredInputs = False
		self.navx = navx
		
		self.angle_constant = self.sd.getAutoUpdateValue('Drive | Drive_Angle', 0.2)
		self.drive_constant = self.sd.getAutoUpdateValue('Drive | Drive_Constant', .000095)
		self.drive_max = self.sd.getAutoUpdateValue('Drive | Max Enc Speed', .5)
		self.gyro_enabled = True
		
		self.robotDrive = robotDrive
		
		self.rf_encoder = rf_encoder
		self.lf_encoder = lf_encoder
		
		
		self.navx = navx
		
		
		
		
				
	#
	# Verb functions -- these functions do NOT talk to motors directly. This
	# allows multiple callers in the loop to call our functions without 
	# conflicts.
	#
	
	def move(self, y, rotation, squaredInputs=False):
		'''
			Causes the robot to move
		
			:param x: The speed that the robot should drive in the X direction. 1 is right [-1.0..1.0] 
			:param y: The speed that the robot should drive in the Y direction. -1 is forward. [-1.0..1.0] 
			:param rotation:  The rate of rotation for the robot that is completely independent of the translation. 1 is rotate to the right [-1.0..1.0]
			:param squaredInputs: If True, the x and y values will be squared, allowing for more gradual speed. 
		'''
		self.y = y
		self.rotation = max(min(1.0, rotation), -1)
		self.squaredInputs = squaredInputs

	
	def set_gyro_enabled(self, value):
		'''Enables the gyro
			:param value: Whether or not the gyro is enabled
			:type value: Boolean
		'''
		self.gyro_enabled = value
	
	def return_gyro_angle(self):
		''' Returns the gyro angle'''
		return self.navx.getYaw()
	
	def reset_gyro_angle(self):
		'''Resets the gyro angle'''
		self.navx.reset()

	
	def set_angle_constant(self, constant):
		'''Sets the constant that is used to determine the robot turning speed'''
		self.angle_constant = constant
		
	def reset_drive_encoders(self):
		self.lf_encoder.zero()
		self.rf_encoder.zero()
		
		
	def return_drive_encoder_position(self):
		#print((self.lf_encoder.get() + self.rf_encoder.get())/2)
		return (self.lf_encoder.get() + self.rf_encoder.get())/2
	
	def get_inches_to_ticks(self, inches):
		gear_ratio = 50 / 12
		target_position = (gear_ratio * ENCODER_ROTATION * inches) / (math.pi*WHEEL_DIAMETER)
		return target_position
	
	def drive_distance(self, inches):
		return self.encoder_drive(self.get_inches_to_ticks(inches))
		
	def encoder_drive(self, target_position):
		target_offset = target_position - self.return_drive_encoder_position()
		
		if abs(target_offset)> 1000:
			self.y = target_offset * self.drive_constant.value
			self.y = max(min(self.drive_max.value, self.y), -self.drive_max.value)
			
			return False
		return True
		
		
	def angle_rotation(self, target_angle):
		'''
			Adjusts the robot so that it points at a particular angle. Returns True 
		    if the robot is near the target angle, False otherwise
		   
		    :param target_angle: Angle to point at, in degrees
		    
		    :returns: True if near angle, False otherwise
		'''
		if not self.gyro_enabled:
			return False
		
		angleOffset = target_angle - self.return_gyro_angle()
		
		if angleOffset < -1 or angleOffset > 1:
			self.rotation = angleOffset * self.angle_constant.value
			self.rotation = max(min(0.3, self.rotation), -0.3)
			
			return False
		
		return True
	def set_direction(self, direction):
		'''Used to reverse direction'''
		self.isTheRobotBackwards = bool(direction)
	
	def switch_direction(self):
		'''when called the robot will reverse front/back'''
		self.isTheRobotBackwards = not self.isTheRobotBackwards
		
	def doit(self):
		''' actually makes the robot drive'''
		

		if(self.isTheRobotBackwards):
			self.robotDrive.arcadeDrive(-self.y, -self.rotation, self.squaredInputs)
		else:
			self.robotDrive.arcadeDrive(self.y, -self.rotation, self.squaredInputs)
			
		
		# by default, the robot shouldn't move
		self.y = 0
		self.rotation = 0
		self.update_sd()
		
	def update_sd(self):
		self.sd.putValue('NavX | Angle', self.navx.getAngle())
		self.sd.putValue('NavX | Pitch', self.navx.getPitch())
		self.sd.putValue('NavX | Yaw', self.navx.getYaw())
		self.sd.putValue('NavX | Roll', self.navx.getRoll())
		self.sd.putValue('Drive | Encoder', self.return_drive_encoder_position())
		self.sd.putValue('Drive | Y', self.y)