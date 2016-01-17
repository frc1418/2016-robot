import wpilib

from networktables import NetworkTable

class Drive(object):
	'''
		The sole interaction between the robot and its driving system
		occurs here. Anything that wants to drive the robot must go
		through this class.
	'''

	def __init__(self, robotDrive):
		'''
			Constructor. 
			
			:param robotDrive: a `wpilib.RobotDrive` object
		'''
		self.isTheRobotBackwards = False
		# set defaults here
		self.y = 0
		self.rotation = 0
		#self.gyro = gyro
		
		self.angle_constant = .040
		self.gyro_enabled = True
		
		self.robotDrive = robotDrive
		
		# Strafe stuff
		
		sd = NetworkTable.getTable('SmartDashboard')
		
		
		
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
		if squaredInputs:
			if y >= 0.0:
				y = (y * y)
			else:
				y = -(y * y)
		
		self.y = y
		self.rotation = max(min(1.0, rotation), -1) / 2.0

	
	def set_gyro_enabled(self, value):
		'''Enables the gyro
			:param value: Whether or not the gyro is enabled
			:type value: Boolean
		'''
		self.gyro_enabled = value
	
	def return_gyro_angle(self):
		''' Returns the gyro angle'''
		return self.gyro.getAngle()
	
	def reset_gyro_angle(self):
		'''Resets the gyro angle'''
		self.gyro.reset()

	
	def set_angle_constant(self, constant):
		'''Sets the constant that is used to determine the robot turning speed'''
		self.angle_constant = constant
	
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
	
	
	# Actually tells the motors to do something
	#
	
	def doit(self):
		''' actually makes the robot drive'''
		if(self.isTheRobotBackwards):
			self.robotDrive.arcadeDrive(-self.y, self.rotation)
		else:
			self.robotDrive.arcadeDrive(self.y, self.rotation)

		# print('x=%s, y=%s, r=%s ' % (self.x, self.y, self.rotation))
		
		# by default, the robot shouldn't move
		self.x = 0
		self.y = 0
		self.rotation = 0
	
