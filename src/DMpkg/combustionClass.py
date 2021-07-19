from DMpkg.propertyClass import propertyClass
from DMpkg.houbolt_jr_single import houbolt_jr_single
import DMpkg as rocket
import numpy as np

class combustionClass:
    def __init__(self, input) -> None:
        self.input = input
        self.util = rocket.utilitiesClass(self.input)

    def getPropellantTags(self):
        self.fuelTag = self.input["fuel"]
        self.oxidizerTag = self.input["ox"]

    def get_CEA(self):
        houbolt_jr                     = rocket.cea(Pcc=self.input["design"]["Pcc"], OF=self.input["design"]["OF"], area_ratio=rocket.nozzleClass().exp, Pamb=14.7, 
                                                    oxName= self.input["ox"]["name"], fuelName= self.input["fuel"]["name"]) #are these meant to be default values? where to get params from?
        # area ratio is throat area / nozzle area (from nozzleClass)
        self.output = propertyClass()
        self.output.gamm_e             = houbolt_jr.exit_MolWt_gamma
        self.output.rho_e              = houbolt_jr.MachNumber
        self.output.Isp                = houbolt_jr.Isp
        self.output.Te                 = houbolt_jr.T_e
        self.output.Pe                 = houbolt_jr.P_e
        self.output.Re                 = self.output.Pe / (self.output.rho_e * self.output.Te)
        self.output.gamm               = houbolt_jr.Chamber_MolWt_gamma
        self.output.cstar              = houbolt_jr.Cstar
        self.output.Tcc                = houbolt_jr.temperatures[0]

