import numpy as np
import DMpkg as rocket

class fluidClass:
    def __init__(self, input, inputTag) -> None:
        # what's the difference between input and inputTag

        self.phase                  = 0   # 1 if pressurant, 2 else
        if inputTag["fluidtype"] == 'Pressurant':
            self.phase              = 1
        elif inputTag["fluidtype"] == "Fuel" or inputTag["fluidtype"] == "Oxidizer":
            self.phase              = 2
        else:
            raise Exception("Invalid inputTag entered")
        
        self.m                      = np.zeros((input['sim']['numpt'], self.phase))
        self.mdot                   = np.zeros((input['sim']['numpt'], self.phase))
        self.n                      = np.zeros((input['sim']['numpt'], self.phase))
        self.P                      = np.zeros((input['sim']['numpt'], self.phase))
        self.T                      = np.zeros((input['sim']['numpt'], self.phase))
        self.l                      = np.zeros((input['sim']['numpt'], self.phase))
        self.cg                     = np.zeros((input['sim']['numpt'], self.phase))
        self.rho                    = np.zeros((input['sim']['numpt'], self.phase))

        self.MW                     = inputTag['MW']
        self.rho                    = 8314/self.MW
        self.name                   = inputTag['name']


    def setInitialConditions(self, inputStruct):

        self.IC                     = rocket.propertyClass()
        self.IC.m                   = inputStruct.m
        self.IC.T                   = inputStruct.T
        self.IC.P                   = inputStruct.P
        self.IC.rho                 = inputStruct.rho
        if type(self.IC.m) == float:
            self.IC.n                   = self.IC.m/self.MW
        elif type(self.IC.m) == list:
            self.IC.n                   = self.IC.m[0]/self.MW
        
        self.initializeMass(self.IC.m)
        self.initializeTemperature(self.IC.T)
        self.initializePressure(self.IC.P)
        self.initializeDensity(self.IC.rho)
        self.initializeAmount(self.IC.n)


    def initializeMass(self, initValue):
        self.m[0]                   = initValue

    # do we need an initializeDensity function?
    def initializeDensity(self, initValue):
        self.rho                 = initValue
    
    def initializeTemperature(self, initValue):
        self.T[0]                   = initValue
    
    def initializePressure(self, initValue):
        self.P[0]                   = initValue
    
    def initializeAmount(self, initValue):
        self.n[0]                   = initValue
    
    def initializeMdot(self, initValue):
        self.mdot[0]                = initValue

    def getM(self, i):
        return self.m[i]
    
    def getP(self, i):
        return self.P[i]
    
    def getT(self, i):
        return self.T[i]
    
    def getN(self, i):
        return self.n[i]
