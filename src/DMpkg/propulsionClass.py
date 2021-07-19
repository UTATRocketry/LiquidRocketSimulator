from DMpkg.utilitiesClass import utilitiesClass
from DMpkg.combustionClass import combustionClass
from DMpkg.tankSystemClass import tankSystemClass
from DMpkg.nozzleClass import nozzleClass
from DMpkg.houbolt_jr_single import houbolt_jr_single
import DMpkg as rocket
import numpy as np

class propulsionClass:
    def __init__(self,input) -> None:
        self.input = input
        self.util = utilitiesClass(self.input)
        
        self.info = self.input["engine"]
        #self.info is a dictionary (see input.yaml for properties)

        self.settings = self.input['settings']
        ofi = self.settings['OF_i']
        off = self.settings['OF_f']
        nf = self.settings['num_OF']
        self.settings['OF_Vec'] = np.linspace(ofi, off, num=nf) #create a vector

        #everything below this line a string in the matlab code. Not sure if this is a mistake or not

        self.performance = {"Mdotox" : None, "Mdotf" : None,
                         "Mdot" : None,
                         "Mf" : None,
                         "Mox" : None,
                         "Mprop" : None,
                         "Pcc" : None,
                         "Tcc" : None,
                         "Te" : None,
                         "cstar" : None}

        self.getPropellantTags()
        self.combustion                      = combustionClass(input) 
        self.nozzle                          = nozzleClass(input)
        
        self.propellants                     = tankSystemClass(input)
        self.settings['numTanks']            = np.shape(self.propellants.tanks)[0]

    def getPropellantTags(self):
        self.oxidizerTag = self.input['ox']
        self.fuelTag = self.input['fuel']

    def getCG(self):
        self.propellants.getCG() #this method does not return anything, but adds cg, m, and l instance variables to self.propellants
        self.cg = self.propellants.cg
        self.m = self.propellants.m
        self.l = self.propellants.l
        
    def setMassFlowRates(self):
 
        for i in range(self.settings['numTanks']):
            tank_type = self.propellants.tank_inputs[i][0]

            if tank_type == 'Oxidizer':
                self.performance['Mdotox'] = self.propellants.tanks[i][0].propellant.mdot
            elif tank_type == 'Fuel':
                self.performance['Mdotf'] = self.propellants.tanks[i][0].propellant.mdot
            elif tank_type == 'Pressurant':
                continue
            else:
                raise Exception('propulsionClass --> setMassFlowRates(): Unknown propellant type.')

        self.performance['Mdot'] = self.performance['Mdotox'] + self.performance['Mdotf']


    def Mdotox(self):
        return self.performance.get('Mdotox')
    
    def Mdot(self):
        return self.performance.get('Mdot')
    
    def Mox(self):
        return self.performance.get('Mox')
    
    def Mf(self):
        return self.performance.get('Mf')
    
    def Mprop(self):
        return self.performance.get('Mprop')
    
    def setOFratio(self):
        self.performance['OF'] = self.performance["Mdotox"]/self.performance['Mdotf']

    def getOF(self):
        return self.performance['OF']

    def getCstar(self):
        Pcc = self.input['design']['Pcc']
        cstar = np.zeros(self.settings['num_OF'])

        for i in range(len(cstar)):
            self.combustion.get_CEA() #obj.combustion.get(obj.settings.OF_Vec(i), Pcc, 1)

            cstar[i] = self.combustion.output.cstar

    def setPropMasses(self):

        for i in range(self.settings['numTanks']):
            tank_type = self.propellants.tank_inputs[i][0]
            
            if tank_type == 'Oxidizer':
                self.performance['Mox'] = self.propellants.tanks[i].m[:]
            elif tank_type == 'Fuel':
                self.performance['Mf'] = self.propellants.tanks[i].m[:]
            elif tank_type == 'Pressurant':
                continue
            else:
                raise Exception('rocketClass --> setPropMasses(): Unknown propellant type')

    def getBlowdown(self):

        tank_inputs = self.input['props']

        for i in range(self.settings['numTanks']):
            if tank_inputs[i][0] == 'Fuel' or tank_inputs[i][0] == 'Oxidizer':

                self.propellants.tanks[i].getBlowdown() # i'm assuming this works

                if tank_inputs[i][2] > 0:
                    # propellants.tanks contains a list of objects of type propellantTankClass
                    self.propellants.tanks[tank_inputs[i][2]].pressurant.mdot = self.propellants.tanks[tank_inputs[i][2]].pressurant.mdot + self.propellants.tanks[tank_inputs[i][0]].pressurant.mdot # idk what's happening here with the tank inputs

            for i in range(self.settings['numTanks']):

                if tank_inputs[i][0] == 'Fuel' or tank_inputs[i][0] == 'Oxidizer':
                    self.propellants.tanks[i][0].getBlowdown()

                    if tank_inputs[i][2] > 0:
                        self.propellants.tanks[tank_inputs[i][2]].pressurant.mdot = self.propellants.tanks[tank_inputs[i][2]].pressurant.mdot + self.propellants.tanks[tank_inputs[i][0]].pressurant.mdot # idk what's happening here with the tank inputs
            
            for i in range(self.settings['numTanks']):
                if tank_inputs[i][0] == 'Pressurant':
                    self.propellants.tanks[i][0].getBlowdown()
            
        self.setMassFlowRates()
        self.setOFratio()
        self.setPropMasses()