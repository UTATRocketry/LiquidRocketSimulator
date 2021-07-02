from src.DMpkg.houbolt_jr_single import houbolt_jr_single
import DMpkg as rocket
import numpy as np
import math

class propellantTankClass:

    '''properties (Access = public)

        name            # Propellant name                           (str)
        type            # Propellant type                           (str)
        tank_input      # Tag for tank                              (str)
        input           # Input structure                           (struct)
        tank            # Tank body                                 (struct)
        propellant      # Liquid phase                              (fluidClass)
        pressurant      # Pressurant vapor phase                    (fluidClass)
        cg              # CG of propellant tank and contents        (double)
        m               # Mass of propellant tank and contents      (double)
        l               # Length of propellant tank and contents    (double)
        ullage          # Ullage volume                             (double)
        offset          # Distance offset before tank system        (double)

        isPressurized   # Pressurization flag                       (bool)
        pressurantOrder # Pressurant tank arrangment                (bool)
        util            # Utilities                                 (utilitiesClass)
        designVars
        
        prop_name
        pres_name
        prop_name_cp
        pres_name_cp
    '''

    #-----------------------------------------------------------------------
    #   METHOD: propellantTankClass
    #   Constructs propellantTankClass given required inputs.
    #
    #   INPUTS \..........................................................
    #     - <input> (struct): A structure that contains all input variables
    #     - <inputTag> (str): A tag that identifies the field name in
    #                         <input> that contains data relevant to the
    #                         specifid tank being created.
    #   OUTPUTS ............................................................
    #     - <self> (class):    Returns created propellantTankClass
    #-----------------------------------------------------------------------
    def __init__(self,input, tankTag):
            
        # Populate general properties
        self.input           = houbolt_jr_single()                            # Input
        self.tank_input      = tankTag                          # Input field for this tank
        self.name            = self.tank_input.get("name")                         # Propellant name
        self.type            = self.tank_input.get("fluidtype")                     # Propellant type
        self.m               = np.zeros((input.sim.numpt, 1))        # Mass
        self.l               = self.tank_input.get("lTank")
        self.cg              = np.zeros((input.sim.numpt, 1))        # CG
        self.offset          = self.tank_input.get("offset")                        # Offset distance
            
        # Create utilities property
        self.util            = rocket.utilitiesClass(input)

        # Populate tank struct
        self.tank            = rocket.propertyClass()
        self.tank.t          = self.tank_input.get("tTank")                         # Wall thickness
        self.tank.m          = self.tank_input.get("mTank")                         # Mass
        self.tank.v          = self.tank_input.get("vTank")                         # Volume
        self.tank.cg         = self.tank_input.get("lTank")/2                       # CG location
            
        self.prop_name       = self.propName()
        self.prop_name_cp    = self.propName_cp()
        self.pres_name       = self.presName()
        self.pres_name_cp    = self.presName_cp()  
    
        rho                 = self.util.cp('D', 'T', self.tank_input.get("Tinit"), 'P', self.tank_input.get("Pinit"), self.prop_name_cp)
        self.tank.ullage     = self.tank.v - self.tank_input.get("mInit") / rho

        # Initialize propellant liquid phase
        self.propellant      = rocket.twoPhaseFluidClass(input, tankTag)

        initStruct.T        = [self.tank_input.get("Tinit"), self.tank_input.get("Tinit")]
        initStruct.P        = [self.tank_input.get("Pinit"), self.tank_input.get("Pinit")]
        initStruct.m        = [self.tank_input.get("mInit"), 0]
        initStruct.rho      = [self.util.cp('D', 'T', self.tank_input.get("Tinit"), 'P', self.tank_input.get("Pinit"), self.prop_name_cp), \
                                self.util.cp('D', 'T', self.tank_input.get("Tinit"), 'Q', 1, self.prop_name_cp)]
            
        self.propellant.setInitialConditions(initStruct)

        # Initialize pressurant vapor phase
        exec("self.pressurant      = rocket.FluidClass(input, self.input.(" + self.tank_input.get("pressurant")+"))")    # come back to this when fluidclass inputs are done

        initStruct.T        = self.tank_input.get("Tinit")
        initStruct.P        = self.tank_input.get("Pinit")
        initStruct.m        = self.tank.ullage*self.util.cp('D', 'T', initStruct.T, 'P', initStruct.P, self.pres_name_cp)
        initStruct.rho      = self.util.cp('D', 'T', self.tank_input.get("Tinit"), 'P', self.tank_input.get("Pinit"), self.prop_name_cp)
            
        self.pressurant.setInitialConditions(initStruct)

        # Flag tank if its pressurized
        self.isPressurized   = self.tank_input.get("isPressurized")
        self.pressurantOrder = self.tank_input.get("pressurantOrder")

        # Select blowdown def
        self.setBlowdownCharacteristics()
        return self
         
            
             
        
    #-----------------------------------------------------------------------
    #   METHOD: simulateBlowdown
    #   Selects and calls appropriate blowdown def deping on the
    #   type of blowdown specified in the input file.
    #
    #   INPUTS: NONE
    #   OUTPUTS: NONE
    #-----------------------------------------------------------------------
    def getBlowdown(self):

        if self.type == 'Oxidizer':
            if self.tank_input.get("blowdownMode") == 'unpressurized':
                self.OX_Blowdown()
            elif self.tank_input.get("blowdownMode") == 'constantPressure':
                self.OX_constantPressureBlowdown()
            else:
                raise Exception('Blowdown mode #s has not been specialized'+ self.input.design.presMode)
        elif self.type == 'Fuel':
            if self.tank_input.get("blowdownMode") == 'constantMdot':
                self.FUEL_constantMdotBlowdown()
            else:
                raise Exception('Blowdown mode #s has not been specialized'+ self.input.design.presMode)
        else:
            raise Exception('Propellant type #s unknown. Type can either be Oxidizer or Fuel'+ self.type)
            
        

    #-----------------------------------------------------------------------
    #   METHOD: setBlowdownFunction
    #   Selects the defs that computes the blowdown characteristics for
    #   the given propellant.
    #
    #   INPUTS: NONE
    #   OUTPUTS: NONE
    #-----------------------------------------------------------------------
    def setBlowdownCharacteristics(self):

        if self.type =='Oxidizer':
            if (self.name== 'N2O'):
                self.propellant.bdChars  = self.bdChars_NITROUSOXIDE
            else:
                raise Exception('Oxidizer type #s has no mass flow rate def specified'+ self.name)
                    

        elif self.type == 'Fuel':
            self.propellant.bdChars      = self.bdChars_LIQUIDS_MDOT

        else:
            raise Exception('Blowdown def for propellant type #s has not been specialized.'+ self.type)
            
        

    #-----------------------------------------------------------------------
    #   METHOD: constantPressureBlowdown
    #   Performs propellant blowdown using the constant tank pressure
    #   pressurization mode. Uses the selected blowdown def from
    #   setBlowdownFunction() to compute the blowdown characteristics at
    #   each time step.
    #
    #   INPUTS: NONE
    #   OUTPUTS: NONE
    #-----------------------------------------------------------------------
    def OX_Blowdown(self):
        inp                  = rocket.propertyClass()
        inp.mDot             = self.designVars.mDotox
        inp.T                = self.tank_input.get("Tinit")
        inp.V                = self.tank.v
        inp.mTank            = self.tank.m
        inp.P                = self.propellant.IC.P
        inp.n                = self.propellant.IC.n
        inp.Cd               = self.designVars.injCd
        inp.Pe               = self.designVars.Pcc * self.input.settings.cnv
        inp.model            = self.input.settings.fluidModel
        inp.nPres            = self.pressurant.m[0][0]/self.pressurant.MW
            
        self.tank.r          = self.designVars.diameter/2
        Vhat_l              = self.propellant.MW / self.util.cp('D', 'T', inp.T[0], 'P', inp.P[0], 'N2O')
        inp                  = self.findAinj(inp, Vhat_l, self.propellant.MW, inp.P[0] - inp.Pe, inp.Cd)

        self.propellant.mdot[0][0]   = inp.mDot
            
        dt                  = self.designVars.dt

        for i in range(1,self.input.sim.numpt):

            out             = self.propellant.bdChars(inp)

            self.propellant.n[i]      = self.propellant.n[i-1, :] + out.dn * dt
            self.propellant.T[i]      = self.propellant.T[i-1, 0] + out.dT * dt
            self.propellant.mdot[i][0]   = out.mDot
            self.propellant.P[i]      = [out.P, out.P]
            self.propellant.rho[i][0]    = self.util.cp('D', 'T', self.propellant.T[i][1], 'P', self.propellant.P[i][0], 'N2O')
            self.pressurant.n[i][0]      = inp.nPres

            inp.T                        = self.propellant.T[i][0]
            inp.n                        = self.propellant.n[i]
            inp.P                        = self.propellant.P[i][0]
            

        self.propellant.m        = self.propellant.n * self.propellant.MW
        self.pressurant.m        = self.pressurant.n * self.pressurant.MW
            
        self.propellant.l[:, 0]  = np.divide(self.propellant.m[:, 0] , (self.propellant.rho[:, 0] * (self.tank.r - self.tank.t)^2 * math.pi)) # this line doesn't work (what are we trying to do with np.divide)
        self.propellant.l[:, 1]  = self.l - self.propellant.l[0]
                
        
    #-----------------------------------------------------------------------
    #   METHOD: constantPressureBlowdown
    #   Performs propellant blowdown using the constant tank pressure
    #   pressurization mode. Uses the selected blowdown def from
    #   setBlowdownFunction() to compute the blowdown characteristics at
    #   each time step.
    #
    #   INPUTS: NONE
    #   OUTPUTS: NONE
    #-----------------------------------------------------------------------
    def OX_constantPressureBlowdown(self):

        inp.mDot             = self.designVars.mDotox
        inp.T                = self.tank_input.get("Tinit")
        inp.V                = self.tank.v
        inp.mTank            = self.tank.m
        inp.P                = self.propellant.IC.P
        inp.n                = self.propellant.IC.n
        inp.Cd               = self.designVars.injCd
        inp.Pe               = self.designVars.Pcc * self.input.settings.cnv
        inp.nPres            = self.pressurant.m[1][1]/self.pressurant.MW
        inp.model            = self.input.settings.fluidModel
            
        self.tank.r          = self.designVars.diameter/2
        Vhat_l              = self.propellant.MW / self.util.cp('D', 'T', inp.T[0], 'P', inp.P[0], 'N2O')
        inp                  = self.findAinj(inp, Vhat_l, self.propellant.MW, inp.P[0], inp.Pe, inp.Cd)

        self.propellant.mdot[0][0]   = inp.mDot
        dt                  = self.designVars.dt

        for i in range(1,self.input.sim.numpt):

            out             = self.propellant.bdChars(inp)
            dP              = self.propellant.P[i - 1, 0] - out.P

            while (dP > self.input.settings.dPtol):

                inp.nPres        = inp.nPres + self.input.settings.npr_inc
                out             = self.propellant.bdChars(inp)
                dP              = self.propellant.P[i - 1, 0]   - out.P
                

            self.propellant.n[i]      = self.propellant.n[i-1] + out.dn * dt
            self.propellant.T[i]      = self.propellant.T[i-1][0] + out.dT * dt
            self.propellant.mdot[i][0]   = out.mDot
            self.propellant.P[i]      = [out.P, out.P]
            self.propellant.rho[i][0]    = self.util.cp('D', 'T', self.propellant.T[i][0], 'P', self.propellant.P[i][0], 'N2O')

            self.pressurant.n[i][0]      = inp.nPres

            inp.T                        = self.propellant.T[i][0]
            inp.n                        = self.propellant.n[i]
            inp.P                        = self.propellant.P[i][0]
            

        self.propellant.m        = self.propellant.n * self.propellant.MW
        self.pressurant.m        = self.pressurant.n * self.pressurant.MW
            
        self.propellant.l[0]  = np.divide(self.propellant.m[:, 0] , (self.propellant.rho[:, 0]) * (self.tank.r - self.tank.t)^2 * pi)
        self.propellant.l[1]  = self.l - self.propellant.l[1]
        self.pressurant.l        = self.propellant.l[:, 1]
 
        mdot    = np.divide([self.pressurant.m[1,0]       - self.pressurant.m[0, 0], np.divide((self.pressurant.m[2:-1, 0]   - self.pressurant.m[0:-3, 0]),2), self.pressurant.m[-1, 0]     - self.pressurant.m(- 2, 0)],dt)

        self.pressurant.mdot     = mdot
        

    def FUEL_constantMdotBlowdown(self):

        mdot    = self.designVars.mDotox / self.designVars.OF
        T       = self.tank_input.get("Tinit")

        self.propellant.mdot[0][0] = mdot
        dt                  = self.designVars.dt

        for i in range(1, self.input.sim.numpt):

            out = self.bdChars_LIQUIDS_MDOT(mdot)
            self.propellant.m[i][0]      = self.propellant.m(i-1, 1) + out.mDot * dt
            self.propellant.mdot[i][0]   = mdot
            self.propellant.T[i][0]      = T
                
            

        

    def bdChars_LIQUIDS_MDOT(mdot):
        output = rocket.propertyClass()
        output.mDot = -mdot
        return output
        

    # Nitrous oxide blowdown
    def bdChars_NITROUSOXIDE(self, input):

        u = self.util

        # Input: T, nPres, nVap, nLiq, V, mTank, Cd, Ainj, Pe
        if strcmp(input.model, 'empirical'):

            # Molar specific vol. of liq. N2O [m^3/kmol]
            Vhat_l      = u.noxProp.Coefs.Q2                    ^ \
                            (1 + (1 - input.T/u.noxProp.Coefs.Q3)  ^ \
                            u.noxProp.Coefs.Q4)                   / \
                            u.noxProp.Coefs.Q1

            # Molar c_V of He [J/(kmol*K)]
            CVhat_Pres  = u.nitrogen.Coefs.C1                   + \
                            u.nitrogen.Coefs.C2*input.T           + \
                            u.nitrogen.Coefs.C3*input.T^2         + \
                            u.nitrogen.Coefs.C4*input.T^3         + \
                            u.nitrogen.Coefs.C5*input.T^4         - u.R

            a           = u.noxProp.Coefs.D3/input.T
            b           = u.noxProp.Coefs.D5/input.T

            # Molar c_V of N2O gas [J/(kmol*K)]
            CVhat_g     = u.noxProp.Coefs.D1                    + \
                            u.noxProp.Coefs.D2*(a/sinh(a))^2      + \
                            u.noxProp.Coefs.D4*(b/cosh(b))^2      - u.R

            # Molar c_V of N2O liq approx. = c_P [J/(kmol*K)]
            CVhat_l     = u.noxProp.Coefs.E1                    + \
                            u.noxProp.Coefs.E2*input.T            + \
                            u.noxProp.Coefs.E3*input.T^2          + \
                            u.noxProp.Coefs.E4*input.T^3          + \
                            u.noxProp.Coefs.E5*input.T^4

            # Reduced temperature.
            Tr          = input.T/u.noxProp.Tc

            # Heat of vaporization of N2O [J/kmol]
            delta_Hv    = u.noxProp.Coefs.T1*(1 - Tr)           ^ \
                            (u.noxProp.Coefs.T2                    + \
                            u.noxProp.Coefs.T3*Tr                 + \
                            u.noxProp.Coefs.T4*Tr^2)

            # Vapour P of N20 (Pa).
            P_sat       = exp(u.noxProp.Coefs.V1                + \
                            u.noxProp.Coefs.V2/input.T            + \
                            u.noxProp.Coefs.V3*log(input.T)       + \
                            u.noxProp.Coefs.V4*input.T^u.noxProp.Coefs.V5)

            # Derivative of vapour P with respect to T.
            dP_sat      = (-u.noxProp.Coefs.V2/(input.T^2)      + \
                            u.noxProp.Coefs.V3/input.T            + \
                            u.noxProp.Coefs.V4*u.noxProp.Coefs.V5 * \
                            input.T^(u.noxProp.Coefs.V5-1))       * \
                            exp(u.noxProp.Coefs.V1                + \
                            u.noxProp.Coefs.V2/input.T            + \
                            u.noxProp.Coefs.V3*log(input.T)       + \
                            u.noxProp.Coefs.V4*input.T^u.noxProp.Coefs.V5)

        elif strcmp(input.model, 'coolprop'):
            # Molar specific vol. of liq. N2O [m^3/kmol]
            Vhat_l      = self.propellant.MW / u.cp('D', 'T', input.T[0], 'P', input.P[0], 'N2O')

            # Molar c_V of Pressurant gas [J/(kmol*K)]
            CVhat_Pres  = self.pressurant.MW * u.cp('O', 'T', input.T[0], 'P', input.P[0], self.pressurant.name)

            # Molar c_V of N2O gas [J/(kmol*K)]
            CVhat_g     = self.propellant.MW * u.cp('O', 'T', input.T[0], 'Q', 1, 'N2O') - self.util.R

            # Molar c_V of N2O liq approx. = c_P [J/(kmol*K)]
            CVhat_l     = self.propellant.MW * u.cp('C', 'T', input.T[0], 'Q', 1, 'N2O')

            # Heat of vaporization of N2O [J/kmol]
            Hv          = u.cp('H', 'T', input.T[0], 'Q', 1, 'N2O')
            Hl          = u.cp('H', 'T', input.T[0], 'Q', 0, 'N2O')
            delta_Hv    = self.propellant.MW * (Hv - Hl)

            # Vapour P of N20 (Pa).
            P_sat       = u.cp('P', 'T', input.T[0], 'Q', 0, 'N2O')

            # Derivative of vapour P with respect to T.
            dP_sat      = u.cp('d(P)/d(T)|D', 'T', input.T, 'Q', 1, 'N2O')
        else:
            raise Exception('Function has not been specialized for model type #s.' + input.model)
            

        # Specific heat of tank, Aluminum [J/kg*K]
        c_P         = (4.8 + 0.00322*input.T)*155.239

        # Simplified expression definitions for solution:
        P           = (input.nPres + input.n[2])*self.util.R*input.T/(input.V - input.n[0]*Vhat_l)
        a           = input.mTank*c_P + input.nPres*CVhat_Pres + input.n[2]*CVhat_g + input.n[0]*CVhat_l
        RT          = P*Vhat_l
        e           = -delta_Hv + self.util.R*input.T
            
        if (input.Pe/P <= 0.5439):
            k       = 1.3
            g       = -0.5*(k+1)/(k-1)
            f       = -input.Cd*input.Ainj * P * sqrt(k/(input.T*self.propellant.R)) * (0.5*(k+1))^g
        else:
            #disp('propellantTankClass > bdChars_NIROUSOXIDE(): WARNING, Fluid is not choked.')
            f       = -input.Cd*input.Ainj*sqrt(abs(2/self.propellant.MW*(P - input.Pe)/Vhat_l))
            
            
        j           = -Vhat_l*P_sat
        k           = (input.V - input.n[0]*Vhat_l)*dP_sat
        r           = self.util.R*input.T
        q           = self.util.R*input.n[2]

        Z           = (-f*(-j*a + (q - k)*RT))/(a*(r + j) + (q - k)*(e - RT))
        W           = (-Z*(r*a + (q - k)*e))/(-j*a + (q - k)*RT)
        dT          = (RT*W + e*Z)/a

        # Time derivative of tank conditions
        output.mDot     = -f*self.propellant.MW         # Mass flow rate
        output.dn       = [W, Z]                       # Time derivative of nitrous amount
        output.dT       = [dT, dT]                     # Time derivative of tank temperature
        output.P        = P
        
        return output


    # Find required injector orifice area to supply desired mass flow rate
    def findAinj(self, input, Vh, MW, P, Pcc, Cd):

        if (Pcc/P <= 0.5439):
            k           = 1.3
            g           = -0.5*(k+1)/(k-1)
            input.Ainj  = input.mDot / (Cd * P * sqrt(k/(input.T*self.propellant.R)) * (0.5*(k+1))^g)
        else:
            print('WARNING, Fluid is not choked.')
            input.Ainj  = (input.mDot/MW/Cd)*sqrt(0.5*Vh*MW/(P - Pcc))
            
            
        out         = self.propellant.bdChars(input)

        if out.mDot > self.designVars.mDotox:

            while out.mDot > self.designVars.mDotox:
                input.Ainj  = input.Ainj - 0.000001
                out         = self.propellant.bdChars(input)
                

        elif out.mDot < self.designVars.mDotox:
            while out.mDot < self.designVars.mDotox:
                input.Ainj  = input.Ainj + 0.000001
                out         = self.propellant.bdChars(input)
                
            

        input.mDot = out.mDot
        
        return input

    def propName(self):
        name = self.tank_input.get("name")
        return name
        
    def propName_cp(self):
        name = self.tank_input.get("name")
            
        for i in range(0,size(self.util.coolprop_alias, 1)-1):
            if (name== self.util.coolprop_alias[i, 0]):
                name = self.util.coolprop_alias[i, 0]
        return name
            
        
        
    def presName(self):
        exec("name = self.input.(" + self.tank_input.get("pressurant") + ").name")
        return name

    def presName_cp(self):
        exec("name = self.input.("+self.tank_input.get("pressurant")+").name")
            
        for i in range(0,size(self.util.coolprop_alias, 1)-1):
            if (name == self.util.coolprop_alias[i, 0]):
                name = self.util.coolprop_alias[i, 1]


        return name
                
            
           
        
    # Get tank system CG
    def getCG(self):
            
        LiqPropMass     = self.propellant.m[:,0]
        LiqPropLen      = np.divide(self.propellant.l[:,0] , 2)
            
        VapPropMass     = self.propellant.m[:,1]
        VapPropLen      = np.divide(self.propellant.l[:,1] , 2)
            
        VapPresMass     = self.pressurant.m[:,0]
        VapMass         = VapPresMass + VapPropMass
            
        sum_moms        = np.multiply(self.tank.m ,(self.tank.cg))                \
                        + np.multiply(LiqPropMass , (LiqPropLen + 2*VapPropLen))  \
                        + np.multiply(VapMass     , (VapPropLen))
            
        sum_mass        = LiqPropMass + VapMass + self.tank.m
            
        self.cg          = np.divide(sum_moms , sum_mass)
        self.m           = sum_mass
        
    

