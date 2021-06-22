import DMpkg as rocket
import numpy as np
class tankSystemClass:
    
    def tankSystemClass(input):
        obj.input = input
        obj.designVars = input.design
        obj.tanks = cell(size(input.props,1),1)
        obj.tank_inputs = input.props
        obj.create_tanks()
        # other properties m,cg,l should not need to be initialized as they are arrays
        return obj

    def create_tanks(obj):

        for i in range(0,length(obj.tank_inputs)):
            type = obj.tank_inputs[i][0]
            if (type== 'Fuel') or (type == 'Oxidizer'):
                obj.tanks[i][0]      = propellantTankClass(obj.input, obj.input.props[i][1])
            elif (type== 'Pressurant'):
                obj.tanks[i][0]      = pressurantTankClass(obj.input, obj.input.props[i][1])
            else:
                error('Incorrect tank type.')
        return obj
                
            
        
       
    def getCG(obj):
            
        totalLength = 0
        totalMass = 0 
        totalMoment = 0 

        # run getCG for each tank

        for i in range(1,size(obj.tanks,1)):
            obj.tanks[i][1].getCG()
                
            momCurr = obj.tanks[i][1].m *(totalLength + obj.tanks[i][1].offset + obj.tanks[i][1].cg)
                
            totalLength = totalLength + obj.tanks[i][1].l + obj.tanks[i][1].offset 
            totalMoment = totalMoment + momCurr
            totalMass = totalMass + obj.tanks[i][1].m
            
            
        obj.cg  = totalMoment / totalMass
        obj.m   = totalMass
        obj.l = totalLength

 