import wpilib
import enum

class Swerve(enum.Enum):
    DRIVE = 0
    ROTATE = 1
    
class MyRobot(wpilib.SampleRobot):
    
    def robotInit(self):
        self.timercounter = 0

        # #INITIALIZE JOYSTICKS##
        self.joystick1 = wpilib.Joystick(0)
        self.joystick2 = wpilib.Joystick(1)

        
        # #INITIALIZE MOTORS##
        self.lf_wheel = (wpilib.Victor(0), wpilib.CANTalon(1))
        self.lr_wheel = (wpilib.Victor(2), wpilib.CANTalon(3))
        self.rf_wheel = (wpilib.Victor(4), wpilib.CANTalon(5))
        self.rr_wheel = (wpilib.Victor(6), wpilib.CANTalon(7))
                
        # #SMART DASHBOARD
        
        # #ROBOT DRIVE##
        #self.robot_drive = wpilib.RobotDrive(self.lf_motor, self.lr_motor, self.rf_motor, self.rr_motor)
        self.robot_drive = wpilib.RobotDrive(self.lf_wheel(Swerve.DRIVE),self.lr_wheel(Swerve.DRIVE),self.rf_wheel(Swerve.DRIVE),self.rr_wheel(Swerve.DRIVE))
    def disabled(self):
        # self.talon.setSensorPosition(0)
        wpilib.Timer.delay(.01)
    
    def operatorControl(self):
        # self.myRobot.setSafetyEnabled(True)
        
        while self.isOperatorControl() and self.isEnabled():
            '''
            self.angle = self.joystick1.getDirectionDegrees()
            self.magnitude = self.joystick1.getMagnitude()
            self.rotation = self.joystick2.getX() #no greater than 1, no less than -1
            
            Vtx = self.magnitude*COS(RADIANS(self.angle+90)) #no greater than 1, no less than -1
            Vty = self.magnitude*SIN(RADIANS(self.angle+90)) #no greater than 1, no less than -1
            
            #Velocity in (x,y)            
            lf = (Vtx - self.rotation * 1, Vty + self.rotation * -1)
            lr = (Vtx - self.rotation * -1, Vty + self.rotation * -1)
            rf = (Vtx - self.rotation * 1, Vty + self.rotation * 1)
            rr = (Vtx - self.rotation * -1 , Vty + self.rotation * 1)
            
            #(speed, angle) in (x,y)            
            lf2 = (sqrt((lf(0)*lf(0))+(lf(1)*lf(1))), atan2(lf(0),lf(1)))
            lr2 = (sqrt((lr(0)*lr(0))+(lr(1)*lr(1))), atan2(lr(0),lr(1)))
            rf2 = (sqrt((rf(0)*rf(0))+(rf(1)*rf(1))), atan2(rf(0),rf(1)))
            rr2 = (sqrt((rr(0)*rr(0))+(rr(1)*rr(1))), atan2(rr(0),rr(1)))
            '''
            
            self.x = joystick1.getX()
            self.y = joystick1.getY()
            self.rotation = self.joystick2.getX() #no greater than 1, no less than -1

            self.robot_drive.arcadeDrive(self.x,self.y)
            
            lf_wheel(Swerve.ROTATE).set(self.rotation)
            lr_wheel(Swerve.ROTATE).set(self.rotation) 
            rf_wheel(Swerve.ROTATE).set(self.rotation)
            rr_wheel(Swerve.ROTATE).set(self.rotation)
                                
            
            
            wpilib.Timer.delay(0.005)
            
if __name__ == '__main__':
    wpilib.run(MyRobot)
