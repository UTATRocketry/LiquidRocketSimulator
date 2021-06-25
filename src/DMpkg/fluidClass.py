import numpy as np
import DMpkg as rocket

class fluidClass:
    def __init__(self, input, inputTag) -> None:

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


    def setInitialConditions(self, inputTag):

        self.IC.m                   = inputTag["mInit"]
        self.IC.T                   = inputTag["Tinit"]
        self.IC.P                   = inputTag["Pinit"]
        self.IC.rho                 = inputTag["Rhoinit"]
        self.IC.n                   = self.IC.m/self.MW
        
        self.initializeMass(self, self.IC.m)
        self.initializeTemperature(self, self.IC.T)
        self.initializePressure(self, self.IC.P)
        self.initializeDensity(self, self.IC.rho)
        self.initializeAmount(self, self.IC.n)


    def initializeMass(self, initValue):
        self.m[0]                   = initValue
    
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

        
