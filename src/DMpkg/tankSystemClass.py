import DMpkg as rocket
import numpy as np
from utilitiesClass import cellss

class tankSystemClass:
    
    def __init__(self, input):
        self.input = input
        self.designVars = input.design
        self.tanks = cellss(len(input.props,1),1) # doesn't strictly store values?
        self.tank_inputs = input.props
        self.create_tanks()
        # other properties m,cg,l should not need to be initialized as they are arrays

    def create_tanks(self):

        for i in range(0,len(self.tank_inputs)):
            type = self.tank_inputs[i][0]
            if (type== 'Fuel') or (type == 'Oxidizer'):
                self.tanks[i][0]      = rocket.propellantTankClass(self.input, self.input.props[i][1])
            elif (type== 'Pressurant'):
                self.tanks[i][0]      = rocket.pressurantTankClass(self.input, self.input.props[i][1])
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
                
            momCurr = self.tanks[i][1].m *(totalLength + self.tanks[i][1].offset + self.tanks[i][1].cg)
                
            totalLength = totalLength + self.tanks[i][1].l + self.tanks[i][1].offset 
            totalMoment = totalMoment + momCurr
            totalMass = totalMass + self.tanks[i][1].m
            
            
        self.cg  = totalMoment / totalMass
        self.m   = totalMass
        self.l = totalLength

 