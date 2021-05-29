import json

class propertyClass:

    def __init__(self, inp_path):
        with open(inp_path, "r") as f:
            inp_dic = json.load(f)
        
        # Engine Input Variables
        self.engine.name           = inp_dic.get("engine name")                     # Engine name
        self.engine.Mfg            = inp_dic.get("engine Mfg")                      # Engine manufacturer
        self.engine.engfile        = inp_dic.get("engine engfile")                  # Name of output engine file

        # Settings
        self.settings.efficiency   = inp_dic.get("settings efficiency")             # Combustion efficiency
        self.settings.flightType   = inp_dic.get("settings flightType")             # Flight dynamics type
        self.settings.cnv          = inp_dic.get("settings cnv")                    # Psi to Pa
        self.settings.optAltFac    = inp_dic.get("settings optAltFac")              # Optimization altitude factor  [N/A]
        self.settings.dPtol        = inp_dic.get("settings dPtol")                  # Pressure drop tolerance       [Pa]
        self.settings.npr_inc      = inp_dic.get("settings npr_inc")                # Pressurant increment
        self.settings.OF_i         = inp_dic.get("settings OF_i")                   # initial OF value
        self.settings.OF_f         = inp_dic.get("settings OF_f")                   # final OF value
        self.settings.num_OF       = inp_dic.get("settings num_OF")                 # final OF timestep
        self.settings.OF           = inp_dic.get("settings OF")                     # Design Ox/Fuel ratio          [double]
        self.settings.fluidModel   = inp_dic.get("settings fluidModel")             # Fluid model for nitrous oxide
        self.settings.LRail        = inp_dic.get("settings LRail")                  # Launch rail length
        self.settings.numTanks     = inp_dic.get("settings numTanks")  

        # Mass Budget
        self.mass.url              = inp_dic.get("mass url") 
        #self.mass.data             = get_mass_budget(self.mass.url)

        ###############################################################
        # DEFINE ROCKET DESIGN VARIABLES

        # Engine burn time                                  [s]
        self.design.tBurn          = inp_dic.get("design tBurn") 
        # Design Ox mdot                                    [kg/s]
        self.design.mDotox         = inp_dic.get("design mDotox")
        # Launch angle                                      [degrees]
        self.design.thetaL         = inp_dic.get("design thetaL")
        # Rocket diameter                                   [m]
        self.design.diameter       = inp_dic.get("design diameter")
        # Design chamber pressure                           [psi]
        self.design.Pcc            = inp_dic.get("design Pcc")
        # Design OF ratio                                   [double]
        self.design.OF             = inp_dic.get("design OF")
        # Injector discharge coeff.                         [double]
        self.design.injCd          = inp_dic.get("design injCd")

        ###############################################################
        # DEFINE SIMULATION PARAMETERS

        self.sim.numpt             = inp_dic.get("sim numpt")                       # Discretization points         [integer]
        self.sim.relax             = inp_dic.get("sim relax")                       # Relaxation factor             [double, 0 < relax < ]
        self.sim.altConvCrit       = inp_dic.get("sim altConvCrit")                 # Altitude convergence crit     [m]
        self.sim.altBO             = inp_dic.get("sim altBO")

        # Masses
        self.mass.dry              = inp_dic.get("mass dry")                        # self.mass.data.Dry_Mass

        ###############################################################
        # DEFINE PROPELLANT AND PRESSURANT TANKS
        
        # Fuel pressurant parameters
        self.fPres.name            = inp_dic.get("fPres name")                      # Nitrogen                      [char]
        self.fPres.frac            = inp_dic.get("fPres frac")                      # Fraction                      [#]
        self.fPres.MW              = inp_dic.get("fPres MW")                        # Molar mass                    [g/mol]
        self.fPres.Cp              = inp_dic.get("fPres Cp")                        # Heat capacity                 [J/kmol K]
        self.fPres.mTank           = inp_dic.get("fPres mTank")                     # self.mass.data.Fuel_Pressurant_Tank
        self.fPres.lTank           = inp_dic.get("fPres lTank")                     # READ FROM MASS MUDGET         [kg]
        self.fPres.vTank           = inp_dic.get("fPres vTank")                     # READ FROM MASS BUDGET         [m^3]
        self.fPres.tTank           = inp_dic.get("fPres tTank")
        self.fPres.offset          = inp_dic.get("fPres offset")                    # Distance till next comp.      [m]
        self.fPres.qdot            = inp_dic.get("fPres qdot")                      # Heat flux                     [W]
        self.fPres.Tinit           = inp_dic.get("fPres Tinit")
        self.fPres.Pinit           = inp_dic.get("fPres Pinit")*self.settings.cnv
        self.fPres.Rhoinit         = inp_dic.get("fPres Rhoinit")                   #py.CoolProp.CoolProp.PropsSI('D', 'T', self.fPres.Tinit, 'P', self.fPres.Pinit, self.fPres.name)
        self.fPres.mInit           = self.fPres.vTank * self.fPres.Rhoinit


        # Fuel parameters
        self.fuel.isPropellant     = inp_dic.get("fuel isPropellant")               # Propellant flag               [bool]
        self.fuel.fluidtype        = inp_dic.get("fuel fluidtype")                  # Propellant type               [char]
        self.fuel.name             = inp_dic.get("fuel name")                       # Propellant name               [char]
        self.fuel.isPressurized    = inp_dic.get("fuel isPressurized")              # Pressurization flag           [bool]
        self.fuel.pressurantOrder  = inp_dic.get("fuel pressurantOrder")            # Pressurant order              [str]
        self.fuel.pressurant       = inp_dic.get("fuel pressurant")                 # self struct name             [str]
        self.fuel.blowdownMode     = inp_dic.get("fuel blowdownMode")               # Blowdown mode                 [str]
        self.fuel.frac             = inp_dic.get("fuel frac")                       # Fraction                      [#]
        self.fuel.MW               = inp_dic.get("fuel MW")                         # Molar mass                    [g/mol]
        self.fuel.tTank            = inp_dic.get("fuel tTank")
        self.fuel.mTank            = inp_dic.get("fuel mTank")                      # self.mass.data.Fuel_Tank
        self.fuel.lTank            = inp_dic.get("fuel lTank")                      # READ FROM MASS MUDGET         [m]
        self.fuel.ullage           = inp_dic.get("fuel ullage")
        self.fuel.mInit            = inp_dic.get("fuel mInit")                      # self.mass.data.Fuel_Mass   # Initial mass           [m]
        self.fuel.Tinit            = inp_dic.get("fuel Tinit")
        self.fuel.Pinit            = inp_dic.get("fuel Pinit")*self.settings.cnv
        self.fuel.Rhoinit          = inp_dic.get("fuel Rhoinit")                    #py.CoolProp.CoolProp.PropsSI('D', 'T', self.fuel.Tinit, 'P', self.fuel.Pinit, 'Ethanol')
        self.fuel.vTank            = self.fuel.mInit * (1 + self.fuel.ullage) / self.fuel.Rhoinit             
        self.fuel.lTank            = self.fuel.vTank / (math.pi*(0.5*self.design.diameter - self.fuel.tTank)**2)    
        self.fuel.order            = inp_dic.get("fuel order")                      # Order inside rocket           [integer]
        self.fuel.offset           = inp_dic.get("fuel offset")                     # Distance till next comp.      [m]
        

        ###############################################################

        # Oxidizer pressurant parameters
        self.oxPres.name           = 'N2'                 # Nitrogen                      [str]
        self.oxPres.frac           = 100                  # Fraction                      [#]
        self.oxPres.MW             = 28                   # Molar mass                    [g/mol]
        self.oxPres.Cp             = 0.28883e5            # Heat capacity                 [J/kmol K]
        self.oxPres.mTank          = 0.788 #self.mass.data.Ox_Pressurant_Tank
        self.oxPres.lTank          = 0.2                  # READ FROM MASS BUDGET         [m]
        self.oxPres.vTank          = 0.002                # READ FROM MASS BUDGET         [m^3]
        self.oxPres.tTank         = 0.003175
        self.oxPres.offset         = 0.1                  # Distance till next comp.      [m]
        self.oxPres.qdot           = 300                  # Heat flux                     [W]
        self.oxPres.Tinit          = 298
        self.oxPres.Pinit          = 3500*self.settings.cnv
        self.oxPres.Rhoinit        = 250.78            #py.CoolProp.CoolProp.PropsSI('D', 'T', self.oxPres.Tinit, 'P', self.oxPres.Pinit, self.oxPres.name)
        self.oxPres.mInit          = self.oxPres.vTank * self.oxPres.Rhoinit


        # Oxidizer parameters
        self.ox.isPropellant       = True                 # Propellant flag               [bool]
        self.ox.fluidtype          = 'Oxidizer'           # Propellant type               [str]
        self.ox.name               = 'N2O'                # Propellant name               [str]
        self.ox.isPressurized      = True                 # Pressurization flag           [bool]
        self.ox.pressurantOrder    = 'fwd'                # Pressurant order              [str]
        self.ox.pressurant         = 'oxPres'             # self struct name             [str]
        self.ox.blowdownMode       = 'constantPressure'   # Blowdown mode                 [str]
        self.ox.frac               = 100                  # Fraction                      [#]
        self.ox.MW                 = 44.013               # Molar mass                    [g/mol]
        self.ox.mInit              = 7         #self.mass.data.Ox_Mass
        self.ox.Tinit              = 278
        self.ox.Pinit              = 525*self.settings.cnv
        self.ox.Rhoinit            = 882.4013          #py.CoolProp.CoolProp.PropsSI('D', 'T', self.ox.Tinit, 'P', self.ox.Pinit, self.ox.name)
        self.ox.ullage             = 0.05
        self.ox.tTank              = 0.003175
        self.ox.mTank              = 4.8       #self.mass.data.Ox_Tank
        self.ox.vTank              = self.ox.mInit * (1 + self.ox.ullage) / self.ox.Rhoinit             
        self.ox.lTank              = self.ox.vTank / (math.pi*(0.5*self.design.diameter - self.ox.tTank)**2)                  
        self.ox.order              = 2                    # Order inside rocket           [integer]
        self.ox.offset             = 0.31                 # Distance till next comp.      [m]
        
        self.props = cellss(4,3)
        self.props[0][0] = 'Pressurant'
        self.props[0][1] = self.fPres
        self.props[0][2] = 0
        self.props[1][0] = 'Fuel'
        self.props[1][1] = self.fuel
        self.props[1][2] = 1
        self.props[2][0] = 'Pressurant'
        self.props[2][1] = self.oxPres
        self.props[2][2] = 0
        self.props[3][0] = 'Oxidizer'
        self.props[3][1] = self.ox
        self.props[3][2] = 3