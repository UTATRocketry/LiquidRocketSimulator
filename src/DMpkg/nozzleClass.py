import DMpkg as rocket
import numpy as np
class nozzleClass: 
    
    def __init__(self, input = None, utilities = None, propulsion = None, airframe = None) -> None: 

        self.input       = input
        self.util        = utilitiesClass(self.input)
        self.combustion  = combustionClass(self.input)

        self.exp         = propertyClass()

        self.throat      = propertyClass()
        self.throat.r    = []
        self.throat.d    = []
        self.throat.A    = []
        self.throat.T    = []
        self.throat.P    = []
            
        self.exit        = propertyClass()
        self.exit.r      = []
        self.exit.d      = []
        self.exit.A      = []
        self.exit.T      = []
        self.exit.P      = []

        self.designVars  = propertyClass()

    def get(self, alt, g):
            
        atmos                   = self.util.stdAtmos(alt * self.input.settings.optAltFac)

        self.expansionRatio(g, atmos.P, self.designVars.Pcc * self.input.settings.cnv)
        comb                    = self.combustion.get(self.designVars.OF,   \
                                                        self.designVars.Pcc,  \
                                                        self.exp) #this will need to be changed if combustion.get changes
        self.areas(comb)
        self.dimensions()
    

    def areas(self, comb):

        Pcc                     = self.designVars.Pcc * self.input.settings.cnv
        mdot                    = self.designVars.mDotox * (1 + 1/self.designVars.OF)


        A                       = sqrt(comb.Tcc)/Pcc
        B                       = sqrt(comb.Re/comb.gamm)
        C                       = (comb.gamm+1)/(2*(comb.gamm-1))

        self.throat.A            = mdot*A*B*((comb.gamm+1)/2)^C
        self.exit.A              = self.throat.A * self.exp
    
        
    def dimensions(self):
        self.throat.r            = sqrt(self.throat.A / pi)
        self.throat.d            = self.throat.r * 2
            
        self.exit.r              = sqrt(self.exit.A / pi)
        self.exit.d              = self.exit.r * 2            
    

    def expansionRatio(self, gamma, P_e, P_0):

        A                       = ((gamma+1)/2)^(1/(gamma-1))
        B                       = (P_e/P_0)^(1/gamma)
        C                       = ((gamma + 1)/(gamma - 1))
        D                       = 1-(P_e/P_0)^((gamma - 1)/gamma)

        self.exp                 = 1/(A*B*sqrt(C*D))
