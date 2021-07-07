import DMpkg as rocket
import numpy as np
from DMpkg.pressurantTankClass import pressurantTankClass
from DMpkg.propellantTankClass import propellantTankClass

from DMpkg.utilitiesClass import cellss
class tankSystemClass:
    
    def tankSystemClass(self, input):
        self.input = input
        self.designVars = input["design"]
        self.tanks = cellss(len(input.props,1),1) # can't change to numpy array as elmts of array are propellant tank class objects (line 19)
        self.tank_inputs = input["props"]
        self.create_tanks()
        # other properties m,cg,l should not need to be initialized as they are arrays
        return self

    def create_tanks(self):

        for i in range(0,len(self.tank_inputs)):
            type = self.tank_inputs[i][0]
            if (type== 'Fuel') or (type == 'Oxidizer'):
                self.tanks[i][0]      = propellantTankClass(self.input, self.input.props[i][1])
            elif (type== 'Pressurant'):
                self.tanks[i][0]      = pressurantTankClass(self.input, self.input.props[i][1])
            else:
                raise Exception('Incorrect tank type.')
        return self
                
            
        
       
    def getCG(self):
            
        totalLength = 0
        totalMass = 0 
        totalMoment = 0 

        # run getCG for each tank

        for i in range(1,len(self.tanks,1)):
            self.tanks[i][1].getCG()
                
            momCurr = np.multiply(self.tanks[i][0].m ,(totalLength + self.tanks[i][0].offset + self.tanks[i][0].cg)) # have to make sure m, offset, and cg are numpy arrays in propellantTankClass
            # are we sure the dot notation works here? do we need to index like a dictionary?
                
            totalLength = totalLength + self.tanks[i][0].l + self.tanks[i][0].offset 
            totalMoment = totalMoment + momCurr
            totalMass = totalMass + self.tanks[i][0].m
            
            
        self.cg  = np.divide(totalMoment, totalMass)
        self.m   = totalMass
        self.l = totalLength

 