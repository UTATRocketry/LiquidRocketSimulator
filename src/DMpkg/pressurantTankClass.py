import numpy as np
import DMpkg as rocket
import math

class pressurantTankClass:
    '''
        Properties
        name            % Propellant name                           (str)
        type            % Propellant type                           (str)
        tank_input      % Tag for tank                              (str)
        input           % Input structure                           (struct)
        tank            % Tank body                                 (struct)
        pressurant      % Pressurant Gas                            (fluidClass)
        cg              % CG of propellant tank system              (double)
        m               % Mass of propellant tank system            (double)
        l               % length of propellant tank system          (double)
        offset          % Distance offset before tank system        (double)
        util            % Utilities                                 (utilitiesClass)
        designVars
    '''
    def __init__(self, input, inputTag) -> None:
        
        try:
            self.input                              = input
            self.tank_input                         = inputTag
        except ValueError or KeyError or input == None or inputTag == None:
            raise Exception("Invalid inputs - pressurantTankClass")
        
        self.name                                   = self.tank_input.name
        self.cg                                     = np.zeros(input['sim']['numpt'], 1)
        self.offset                                 = self.tank_input["offset"]
        self.m                                      = self.tank_input["mInit"]*np.ones(input['sim']['numpt'], 1)
        self.l                                      = self.tank_input["lTank"]
        
        self.tank.m                                 = self.tank_input["mTank"]
        self.tank.V                                 = self.tank_input["vTank"]
        self.tank.cg                                = self.l/2            
        
        self.util                                   = rocket.utilitiesClass(input)

        # Initialize propellant liquid phase
        self.pressurant                             = rocket.fluidClass(self.input, self.tank_input)

        self.initstruct.m                           = self.tank_input["mInint"]
        self.initstruct.T                           = self.tank_input["Tinint"]
        self.initstruct.P                           = self.tank_input["Pinint"]
        self.initstuct.rho                          = self.util.cp()                          
        

