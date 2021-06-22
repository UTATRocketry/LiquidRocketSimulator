import DMpkg as rocket
import numpy as np
class nozzleClass: 
    
    def __init__(self, input = None, utilities = None, propulsion = None, airframe = None) -> None: 

        obj.input       = input
        obj.util        = utilitiesClass(obj.input)
        obj.combustion  = combustionClass(obj.input)

        obj.exp         = propertyClass()

        obj.throat      = propertyClass()
        obj.throat.r    = []
        obj.throat.d    = []
        obj.throat.A    = []
        obj.throat.T    = []
        obj.throat.P    = []
            
        obj.exit        = propertyClass()
        obj.exit.r      = []
        obj.exit.d      = []
        obj.exit.A      = []
        obj.exit.T      = []
        obj.exit.P      = []

        obj.designVars  = propertyClass()

    def get(obj, alt, g):
            
        atmos                   = obj.util.stdAtmos(alt * obj.input.settings.optAltFac)

        obj.expansionRatio(g, atmos.P, obj.designVars.Pcc * obj.input.settings.cnv)
        comb                    = obj.combustion.get(obj.designVars.OF,   \
                                                        obj.designVars.Pcc,  \
                                                        obj.exp) #this will need to be changed if combustion.get changes
        obj.areas(comb)
        obj.dimensions()
    

    def areas(obj, comb):

        Pcc                     = obj.designVars.Pcc * obj.input.settings.cnv
        mdot                    = obj.designVars.mDotox * (1 + 1/obj.designVars.OF)


        A                       = sqrt(comb.Tcc)/Pcc
        B                       = sqrt(comb.Re/comb.gamm)
        C                       = (comb.gamm+1)/(2*(comb.gamm-1))

        obj.throat.A            = mdot*A*B*((comb.gamm+1)/2)^C
        obj.exit.A              = obj.throat.A * obj.exp
    
        
    def dimensions(obj):
        obj.throat.r            = sqrt(obj.throat.A / pi)
        obj.throat.d            = obj.throat.r * 2
            
        obj.exit.r              = sqrt(obj.exit.A / pi)
        obj.exit.d              = obj.exit.r * 2            
    

    def expansionRatio(obj, gamma, P_e, P_0):

        A                       = ((gamma+1)/2)^(1/(gamma-1))
        B                       = (P_e/P_0)^(1/gamma)
        C                       = ((gamma + 1)/(gamma - 1))
        D                       = 1-(P_e/P_0)^((gamma - 1)/gamma)

        obj.exp                 = 1/(A*B*sqrt(C*D))
