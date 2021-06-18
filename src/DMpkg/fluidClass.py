import numpy as np
import DMpkg as rocket
from DMpkg.utilitiesClass import cellss

class fluidClass:
    def __init__(self, input, inputTag) -> None:

        self.phase           = 0
        if input['fuel']['isPropellant'] == 'true' and input['fuel']['fluidtype']:
            self.phase       = 1
            if input['ox']['isPropellant'] == 'true' and input['ox']['fluidtype']:
                self.phase   = 2
        
        self.m              = np.zeros((input['sim']['numpt'], self.phase))
        self.mdot           = np.zeros((input['sim']['numpt'], self.phase))
        self.n              = np.zeros((input['sim']['numpt'], self.phase))
        self.P              = np.zeros((input['sim']['numpt'], self.phase))
        self.T              = np.zeros((input['sim']['numpt'], self.phase))
        self.l              = np.zeros((input['sim']['numpt'], self.phase))
        self.cg             = np.zeros((input['sim']['numpt'], self.phase))
        self.rho            = np.zeros((input['sim']['numpt'], self.phase))

        self.MW             = inputTag['MW'] #in the input file there's 4 of them; do these calculations for each?
        self.rho            = 8314/self.MW
        self.name           = inputTag['name']


    def setInitialConditions(self, input):

        ########################################
        # what do I do with this section: where does the data come from?
        # obj.IC.m    = input.m;
        # obj.IC.T    = input.T;
        # obj.IC.P    = input.P;
        # obj.IC.rho  = input.rho;
        # obj.IC.n    = obj.IC.m/obj.MW;
        ########################################
        
        self.initializeMass(self, self.IC.m)
        self.initializeTemperature(self, self.IC.T)
        self.initializePressure(self, self.IC.P)
        self.initializeDensity(self, self.IC.rho)
        self.initializeAmount(self, self.IC.n)


    def initializeMass(self, initValue):
        self.m[0: self.phase] = initValue
    
    


            