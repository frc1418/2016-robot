import wpilib

from networktables import NetworkTable
from enum import Enum


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
		self.gyro_enabled = True
		
		self.robotDrive = robotDrive
		
		self.sd = NetworkTable.getTable('SmartDashboard')
		#Auto / Manual
		
		self.want_manual = False
		self.want_auto = False
		self.navx = navx
		turnController = wpilib.PIDController(.03, 0, 0, 0, navx, output=self)
		turnController.setInputRange(-180.0,  180.0)
		turnController.setOutputRange(-1.0, 1.0)
		turnController.setAbsoluteTolerance(2)
		turnController.setContinuous(True)
		
		self.turnController = turnController
		self.rotateToAngle = False

		
		
				
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
	
	def angle_rotation(self, target_angle):
		'''
			Adjusts the robot so that it points at a particular angle. Returns True 
		    if the robot is near the target angle, False otherwise
		   
		    :param target_angle: Angle to point at, in degrees
		    
		    :returns: True if near angle, False otherwise
		'''
		self.rotateToAngle = True
		self.turnController.enable()
		self.turnController.setSetpoint(target_angle)
		self.rotation = self.output
	def set_direction(self, direction):
		'''Used to reverse direction'''
		self.isTheRobotBackwards = bool(direction)
	
	def switch_direction(self):
		'''when called the robot will reverse front/back'''
		self.isTheRobotBackwards = not self.isTheRobotBackwards
	
	def pidWrite(self, output):
		self.output = output
		
	def doit(self):
		''' actually makes the robot drive'''
		if(self.isTheRobotBackwards):
			self.robotDrive.arcadeDrive(self.y, -self.rotation, self.squaredInputs)
		else:
			self.robotDrive.arcadeDrive(-self.y, -self.rotation, self.squaredInputs)

		
		# by default, the robot shouldn't move
		self.x = 0
		self.y = 0
		self.rotation = 0
		if not self.rotateToAngle:
			self.turnController.disable()
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