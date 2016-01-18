import wpilib
import math

class SharpIR2Y0A02:
    '''
        Sharp IR sensor GP2Y0A02YK0F
        
        Long distance sensor: 20cm to 150cm
        
        Output is in centimeters
        
        Distance can be calculated using 62.28*x ^ -1.092
    '''
    
    def __init__(self,num):
        self.distance = wpilib.AnalogInput(num)
        
    def getDistance(self):
        '''Returns distance in centimeters'''
        
        # Don't allow zero/negative values
        v = max(self.distance.getVoltage(), 0.00001)
        d = 62.28*math.pow(v, -1.092)
        
        # Constrain output 
        return max(min(d, 145.0), 22.5)
    
    def getVoltage(self):
        return self.distance.getVoltage()

class SharpIRGP2Y0A41SK0F:
    '''
        Sharp IR sensor GP2Y0A41SK0F
        
        Short distance sensor: 4cm to 40cm
        
        Output is in centimeters=
    '''
    
    #short Distance
    def __init__(self,num):
        self.distance = wpilib.AnalogInput(num)

    def getDistance(self):
        '''Returns distance in centimeters'''
        
        # Don't allow zero/negative values
        v = max(self.distance.getVoltage(), 0.00001)
        d = 12.84*math.pow(v, -0.9824)
        
        # Constrain output 
        return max(min(d, 25), 4.0)
    
    def getVoltage(self):
        return self.distance.getVoltage()

class CombinedSensor:
    def __init__(self, longDist, longOff, shortDist, shortOff):
        self.longDistance = longDist
        self.shortDistance = shortDist
        self.longOff = longOff
        self.shortOff = shortOff
        
    def getDistance(self):
        
        long = self.longDistance.getDistance()
        short = self.shortDistance.getDistance()
        
        #if short < 25:
        #    return short - self.shortOff
        #else:
        return max(long - self.longOff, 0)
