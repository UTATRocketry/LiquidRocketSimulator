import DMpkg as rocket
import numpy as np
class tankSystemClass:
    
    def tankSystemClass(input):
        self.input = input
        self.designVars = input.design
        self.tanks = cell(size(input.props,1),1)
        self.tank_inputs = input.props
        self.create_tanks()
        # other properties m,cg,l should not need to be initialized as they are arrays
        return self

    def create_tanks(obj):

        for i in range(0,length(self.tank_inputs)):
            type = self.tank_inputs[i][0]
            if (type== 'Fuel') or (type == 'Oxidizer'):
                self.tanks[i][0]      = propellantTankClass(self.input, self.input.props[i][1])
            elif (type== 'Pressurant'):
                self.tanks[i][0]      = pressurantTankClass(self.input, self.input.props[i][1])
            else:
                error('Incorrect tank type.')
        return self
                
            
        
       
    def getCG(obj):
            
        totalLength = 0
        totalMass = 0 
        totalMoment = 0 

        # run getCG for each tank

        for i in range(1,size(self.tanks,1)):
            self.tanks[i][1].getCG()
                
            momCurr = np.multiply(self.tanks[i][1].m ,(totalLength + self.tanks[i][1].offset + self.tanks[i][1].cg))
                
            totalLength = totalLength + self.tanks[i][1].l + self.tanks[i][1].offset 
            totalMoment = totalMoment + momCurr
            totalMass = totalMass + self.tanks[i][1].m
            
            
        self.cg  = np.divide(totalMoment , totalMass)
        self.m   = totalMass
        self.l = totalLength

 