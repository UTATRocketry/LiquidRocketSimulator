from propertyClass import *
import math
from utilitiesClass import *

def houbolt_jr_single():

    input                       = propertyClass()
    input.engine                = propertyClass()
    input.settings              = propertyClass()
    input.mass                  = propertyClass()
    input.design                = propertyClass()
    input.sim                   = propertyClass()
    input.fPres                 = propertyClass()
    input.fuel                  = propertyClass()
    input.oxPres                = propertyClass()
    input.ox                    = propertyClass()

    # Engine Input Variables
    input.engine.name           = 'utat_test'          # Engine name
    input.engine.Mfg            = 'UTAT'               # Engine manufacturer
    input.engine.engfile        = 'utat_test.rse'      # Name of output engine file

    # Settings
    input.settings.efficiency   = 0.9                  # Combustion efficiency
    input.settings.flightType   = '2DOF'               # Flight dynamics type
    input.settings.cnv          = 6894.757             # Psi to Pa
    input.settings.optAltFac    = 0.66                 # Optimization altitude factor  [N/A]
    input.settings.dPtol        = 700                  # Pressure drop tolerance       [Pa]
    input.settings.npr_inc      = 1e-6                 # Pressurant increment
    input.settings.OF_i         = 1                    # initial OF value
    input.settings.OF_f         = 5                    # final OF value
    input.settings.num_OF       = 20                   # final OF timestep
    input.settings.OF           = 3                    # Design Ox/Fuel ratio          [double]
    input.settings.fluidModel   = 'empirical'          # Fluid model for nitrous oxide
    input.settings.LRail        = 5                    # Launch rail length
    input.settings.numTanks     = 0

    # Mass Budget
    input.mass.url              = '1aMlNNq1Of8uMEjFZNS5RNAU0nOtnL61rxDccyHFwKFM'
    # input.mass.data             = get_mass_budget(input.mass.url)

    ###############################################################
    # DEFINE ROCKET DESIGN VARIABLES

    # Engine burn time                                  [s]
    input.design.tBurn          = 8.4
    # Design Ox mdot                                    [kg/s]
    input.design.mDotox         = 0.8
    # Launch angle                                      [degrees]
    input.design.thetaL         = 3
    # Rocket diameter                                   [m]
    input.design.diameter       = 0.1524
    # Design chamber pressure                           [psi]
    input.design.Pcc            = 350
    # Design OF ratio                                   [double]
    input.design.OF             = 3
    # Injector discharge coeff.                         [double]
    input.design.injCd          = 0.4

    ###############################################################
    # DEFINE SIMULATION PARAMETERS

    input.sim.numpt             = 100                  # Discretization points         [integer]
    input.sim.relax             = 0.3                  # Relaxation factor             [double, 0 < relax < ]
    input.sim.altConvCrit       = 50                   # Altitude convergence crit     [m]
    input.sim.altBO             = 1000

    # Masses
    input.mass.dry              = 50.41        #input.mass.data.Dry_Mass

    ###############################################################
    # DEFINE PROPELLANT AND PRESSURANT TANKS
    
    # Fuel pressurant parameters
    input.fPres.name            = 'N2'                 # Nitrogen                      [char]
    input.fPres.frac            = 100                  # Fraction                      [#]
    input.fPres.MW              = 28                   # Molar mass                    [g/mol]
    input.fPres.Cp              = 0.28883e5            # Heat capacity                 [J/kmol K]
    input.fPres.mTank           = 1.78     #input.mass.data.Fuel_Pressurant_Tank
    input.fPres.lTank           = 0.2                  # READ FROM MASS MUDGET         [kg]
    input.fPres.vTank           = 0.002                # READ FROM MASS BUDGET         [m^3]
    input.fPres.tTank           = 0.003175
    input.fPres.offset          = 0.0                  # Distance till next comp.      [m]
    input.fPres.qdot            = 300                  # Heat flux                     [W]
    input.fPres.Tinit           = 298
    input.fPres.Pinit           = 3500*input.settings.cnv
    input.fPres.Rhoinit         = 250.78 #py.CoolProp.CoolProp.PropsSI('D', 'T', input.fPres.Tinit, 'P', input.fPres.Pinit, input.fPres.name)
    input.fPres.mInit           = input.fPres.vTank * input.fPres.Rhoinit


    # Fuel parameters
    input.fuel.isPropellant     = True                 # Propellant flag               [bool]
    input.fuel.fluidtype        = 'Fuel'               # Propellant type               [char]
    input.fuel.name             = 'C2H5OH'             # Propellant name               [char]
    input.fuel.isPressurized    = True                 # Pressurization flag           [bool]
    input.fuel.pressurantOrder  = 'fwd'                # Pressurant order              [str]
    input.fuel.pressurant       = 'fPres'              # Input struct name             [str]
    input.fuel.blowdownMode     = 'constantMdot'       # Blowdown mode                 [str]
    input.fuel.frac             = 100                  # Fraction                      [#]
    input.fuel.MW               = 46.07                # Molar mass                    [g/mol]
    input.fuel.tTank            = 0.003175
    input.fuel.mTank            = 3         #input.mass.data.Fuel_Tank
    input.fuel.lTank            = 0.27                 # READ FROM MASS MUDGET         [m]
    input.fuel.ullage           = 0.05
    input.fuel.mInit            = 2.33         #input.mass.data.Fuel_Mass   # Initial mass           [m]
    input.fuel.Tinit            = 298
    input.fuel.Pinit            = 525*input.settings.cnv
    input.fuel.Rhoinit          = 788.40        #py.CoolProp.CoolProp.PropsSI('D', 'T', input.fuel.Tinit, 'P', input.fuel.Pinit, 'Ethanol')
    input.fuel.vTank            = input.fuel.mInit * (1 + input.fuel.ullage) / input.fuel.Rhoinit             
    input.fuel.lTank            = input.fuel.vTank / (math.pi*(0.5*input.design.diameter - input.fuel.tTank)**2)    
    input.fuel.order            = 1                    # Order inside rocket           [integer]
    input.fuel.offset           = 0.31                 # Distance till next comp.      [m]
    

    ###############################################################

    # Oxidizer pressurant parameters
    input.oxPres.name           = 'N2'                 # Nitrogen                      [str]
    input.oxPres.frac           = 100                  # Fraction                      [#]
    input.oxPres.MW             = 28                   # Molar mass                    [g/mol]
    input.oxPres.Cp             = 0.28883e5            # Heat capacity                 [J/kmol K]
    input.oxPres.mTank          = 0.788 #input.mass.data.Ox_Pressurant_Tank
    input.oxPres.lTank          = 0.2                  # READ FROM MASS BUDGET         [m]
    input.oxPres.vTank          = 0.002                # READ FROM MASS BUDGET         [m^3]
    input.oxPres.tTank         = 0.003175
    input.oxPres.offset         = 0.1                  # Distance till next comp.      [m]
    input.oxPres.qdot           = 300                  # Heat flux                     [W]
    input.oxPres.Tinit          = 298
    input.oxPres.Pinit          = 3500*input.settings.cnv
    input.oxPres.Rhoinit        = 250.78            #py.CoolProp.CoolProp.PropsSI('D', 'T', input.oxPres.Tinit, 'P', input.oxPres.Pinit, input.oxPres.name)
    input.oxPres.mInit          = input.oxPres.vTank * input.oxPres.Rhoinit


    # Oxidizer parameters
    input.ox.isPropellant       = True                 # Propellant flag               [bool]
    input.ox.fluidtype          = 'Oxidizer'           # Propellant type               [str]
    input.ox.name               = 'N2O'                # Propellant name               [str]
    input.ox.isPressurized      = True                 # Pressurization flag           [bool]
    input.ox.pressurantOrder    = 'fwd'                # Pressurant order              [str]
    input.ox.pressurant         = 'oxPres'             # Input struct name             [str]
    input.ox.blowdownMode       = 'constantPressure'   # Blowdown mode                 [str]
    input.ox.frac               = 100                  # Fraction                      [#]
    input.ox.MW                 = 44.013               # Molar mass                    [g/mol]
    input.ox.mInit              = 7         #input.mass.data.Ox_Mass
    input.ox.Tinit              = 278
    input.ox.Pinit              = 525*input.settings.cnv
    input.ox.Rhoinit            = 882.4013          #py.CoolProp.CoolProp.PropsSI('D', 'T', input.ox.Tinit, 'P', input.ox.Pinit, input.ox.name)
    input.ox.ullage             = 0.05
    input.ox.tTank              = 0.003175
    input.ox.mTank              = 4.8       #input.mass.data.Ox_Tank
    input.ox.vTank              = input.ox.mInit * (1 + input.ox.ullage) / input.ox.Rhoinit             
    input.ox.lTank              = input.ox.vTank / (math.pi*(0.5*input.design.diameter - input.ox.tTank)**2)                  
    input.ox.order              = 2                    # Order inside rocket           [integer]
    input.ox.offset             = 0.31                 # Distance till next comp.      [m]
    
    input.props = cellss(4,3)
    input.props[0][0] = 'Pressurant'
    input.props[0][1] = input.fPres
    input.props[0][2] = 0
    input.props[1][0] = 'Fuel'
    input.props[1][1] = input.fuel
    input.props[1][2] = 1
    input.props[2][0] = 'Pressurant'
    input.props[2][1] = input.oxPres
    input.props[2][2] = 0
    input.props[3][0] = 'Oxidizer'
    input.props[3][1] = input.ox
    input.props[3][2] = 3

    return input


