import wpilib

from networktables import NetworkTable

ENCODER_ROTATION = 962
WHEEL_DIAMETER = 7.5625
class Drive:
	'''
		The sole interaction between the robot and its driving system
		occurs here. Anything that wants to drive the robot must go
		through this class.
	'''

	def __init__(self, robotDrive, navx):
		'''
			Constructor. 
			
			:param robotDrive: a `wpilib.RobotDrive` object
		'''
		self.isTheRobotBackwards = False
		# set defaults here
		self.y = 0
		self.rotation = 0
		self.squaredInputs = False
		self.navx = navx
		
		self.angle_constant = .040
		self.drive_constant = .0009
		
		self.gyro_enabled = True
		
		self.robotDrive = robotDrive
		
		self.sd = NetworkTable.getTable('SmartDashboard')
		
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
		return self.navx.getAngle()
	
	def reset_gyro_angle(self):
		'''Resets the gyro angle'''
		self.navx.reset()

	
	def set_angle_constant(self, constant):
		'''Sets the constant that is used to determine the robot turning speed'''
		self.angle_constant = constant
		
	def reset_drive_encoders(self):
		self.robotDrive.frontLeftMotor.setSensorPosition(0)	
		self.robotDrive.frontRightMotor.setSensorPosition(0)
		
		
	def return_drive_encoder_position(self):
		return (self.robotDrive.frontLeftMotor.getEncPosition()+self.robotDrive.frontRightMotor.getEncPosition())/2
	
	def drive_distance(self, inches):
		gear_ratio = 50 / 12
		target_position = (gear_ratio * ENCODER_ROTATION * inches) / WHEEL_DIAMETER
		self.drive.encoderDrive(target_position)
		
	def encoder_drive(self, target_position):
		target_offset = target_position - self.return_drive_encoder_position()
		
		if abs(target_offset)> 50:
			self.y = target_offset * self.drive_constant
			self.y = max(min(1, self.y), -.1)
			
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
			self.rotation = angleOffset * self.angle_constant
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
			self.robotDrive.arcadeDrive(self.y, -self.rotation, self.squaredInputs)
		else:
			self.robotDrive.arcadeDrive(-self.y, -self.rotation, self.squaredInputs)
			
		
		# by default, the robot shouldn't move
		self.y = 0
		self.rotation = 0
		self.update_sd()
		
	def update_sd(self):
		self.sd.putValue('NavX | SupportsDisplacement', self.navx._isDisplacementSupported())
		self.sd.putValue('NavX | IsCalibrating', self.navx.isCalibrating())
		self.sd.putValue('NavX | IsConnected', self.navx.isConnected())
		self.sd.putValue('NavX | Angle', self.navx.getAngle())
		self.sd.putValue('NavX | Pitch', self.navx.getPitch())
		self.sd.putValue('NavX | Yaw', self.navx.getYaw())
		self.sd.putValue('NavX | Roll', self.navx.getRoll())
		self.sd.putValue('NavX | Y-Velocity', self.navx.getVelocityY())
		self.sd.putValue('NavX | X-Velocity', self.navx.getVelocityX())
		self.sd.putValue('NavX | Y-Position', self.navx.getDisplacementY())
		self.sd.putValue('NavX | X-Position', self.navx.getDisplacementX())		