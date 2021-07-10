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

            # what's the difference between input and inputTag here?

        except ValueError or KeyError or input == None or inputTag == None:
            raise Exception("Invalid inputs - pressurantTankClass > __init__")
        
        self.name                                   = self.tank_input["name"]
        self.cg                                     = np.zeros(input['sim']['numpt'], 1)
        self.offset                                 = self.tank_input["offset"]
        self.m                                      = self.tank_input["mInit"]*np.ones(input['sim']['numpt'], 1)
        self.l                                      = self.tank_input["lTank"]
        
        self.tank.m                                 = self.tank_input["mTank"]
        self.tank.V                                 = self.tank_input["vTank"]
        self.tank.cg                                = self.l/2            
        
        self.util                                   = rocket.utilitiesClass(input)

        self.designVars                             = self.input["design"]

        # Initialize propellant liquid phase
        self.pressurant                             = rocket.fluidClass(self.input, self.tank_input)

        self.initstruct.m                           = self.tank_input["mInint"]
        self.initstruct.T                           = self.tank_input["Tinint"]
        self.initstruct.P                           = self.tank_input["Pinint"]
        self.initstuct.rho                          = self.util.coolprop('D', 'P', self.initStruct.P, 'T', self.initStruct.T, self.tank_input["name"])    

        self.pressurant.setInitialConditions(self)
        self.setBlowdownCharacteristics(self, input)

    '''
    %-----------------------------------------------------------------------
    %   METHOD: simulateBlowdown
    %   Selects and calls appropriate blowdown function depending on the
    %   type of blowdown specified in the input file.
    %
    %   INPUTS: NONE
    %   OUTPUTS: NONE
    %-----------------------------------------------------------------------
    '''
    def getBlowdown(self):
        
        if self.name == "N2":
            self.PRES_blowdown(self)
        else:
            raise Exception("pressurantTankClass > getBlowdown(): Function has not been specialized for fluid name" + self.name)

    '''
    %-----------------------------------------------------------------------
    %   METHOD: setBlowdownFunction
    %   Selects the functions that computes the blowdown characteristics for
    %   the given propellant.
    %
    %   INPUTS: NONE
    %   OUTPUTS: NONE
    %-----------------------------------------------------------------------
    '''
    def setBlowdownCharacteristics(self, input):

        if self.name == 'N2':
            self.pressurant.bdChars         = self.bdchars_NITROGEN(self, input)
        else:
            raise Exception("pressurantTankClass > getBlowdown(): Function has not been specialized for fluid name" + self.name)

    def PRES_blowdown(self):

        self.input.V                           = self.tank.V
        self.input.qdot                        = self.tank_input["qdot"]
        self.input.gas                         = self.name

        dt                                  = self.designVars["dt"]

        for i in range(2, self.input['sim']['numpt']):
            self.input.p                       = self.pressurant.P[i - 1]
            self.input.T                       = self.pressurant.T[i - 1]
            self.input.mdot                    = self.pressurant.mdot[i - 1]
            self.input.m                       = self.pressurant.m[i - 1]
                    
            bdChars                         = self.pressurant.bdChars

            self.pressurant.P(i, 1)         = self.pressurant.P(i-1, 1) + bdChars.dPdt * dt
            self.pressurant.T(i, 1)         = self.pressurant.T(i-1, 1) + bdChars.dTdt * dt
            self.pressurant.rho(i, 1)       = self.util.coolprop('D', 'P', self.pressurant.P(i, 1), 'T', self.pressurant.T(i, 1), self.tank_input["name"])
            self.pressurant.m(i, 1)         = self.pressurant.m(i-1, 1) - self.pressurant.mdot(i, 1) * dt
    
    def bd_Chars_NITROGEN(self, input):
        ma                                  = input.m
        V                                   = input.V
        T                                   = input.T
        P                                   = input.P
        mdot                                = input.mdot
        qdot                                = input.qdot

        R                                   = self.util.n2R
        cnv                                 = self.util.cnv

        Zt                                  = self.util.get_dZdT_N2(T, P/cnv)
        Zp                                  = self.util.get_dZdP_N2(T, P/cnv)/cnv
        Z                                   = self.util.coolprop('Z', 'P', P, 'T', T, 'N2')
        cv                                  = self.util.coolprop('O', 'P', P, 'T', T, 'N2')

        dPdt                                = (ma*R*Z**2 + P*V*Zt)*qdot/(V*cv*(ma*(Z - P*Zp))) - mdot*((cv + Z*R)*ma*Z + P*V*Zt)*(P/(ma*cv))/(ma*(Z - P*Zp))
        dZdt                                = (ma*R*Z**2 * Zp + V*Z*Zt)*dPdt/(ma*R*Z**2 + Zt*P*V) - Zt*(P*V*Z/ma)*mdot/(ma*R*Z**2 + Zt*P*V)
        dTdt                                = V*(dPdt/(ma*Z) - dZdt*P/(ma*Z**2) - mdot*P/(ma**2*Z))/R

        self.dPdT                           = dPdt
        self.dTdt                           = dTdt

    def setPressurantMdot(self, mdot):
        self.pressurant.mdot                = mdot

    def getCG(self):
        self.cg                             = self.pressurant.l[:1] / 2
        self.m                              = self.pressurant.m + self.tank.m
        

        

