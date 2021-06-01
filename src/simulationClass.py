from __init__ import *
from houbolt_jr_single import *
from get_mass_budget import *
from utilitiesClass import *
from rocketClass import *

class simulationClass:
    #define class attributes here

    def __init__(self, input_selector):
        if input_selector == None:
            print('ERROR: simulationClass constructor executed without input arguments')
        else:

            print('Message: Building simulationClass')
            
            self.input           = self.load_variables(input_selector)
            
            self.rocket          = rocketClass(self.input)
            self.util            = utilitiesClass(self.input)

            self.numpt           = self.input.get("sim").get("numpt")
            self.relax           = self.input.get("sim").get("relax")
            self.altConvCrit     = self.input.get("sim").get("altConvCrit")

            self.flight          = propertyClass()
            self.flight.t        = self.util.zeroArray
            self.flight.x        = self.util.zeroArray
            self.flight.y        = self.util.zeroArray
            self.flight.s        = self.util.zeroArray
            self.flight.u        = self.util.zeroArray
            self.flight.v        = self.util.zeroArray
            self.flight.V        = self.util.zeroArray
            self.flight.ax       = self.util.zeroArray
            self.flight.ay       = self.util.zeroArray
            self.flight.theta    = self.util.zeroArray
            self.flight.Ma       = self.util.zeroArray
            self.flight.g        = self.util.zeroArray
            self.flight.type     = self.input.get("flight").get("type")
            self.flight.altBO    = self.input.get("flight").get("altBO")

            self.setFlightDynamicsType()
            
    def load_variables(self, input_selector):            
            if (input_selector == 'houbolt_jr_batch'):
                input = houbolt_jr_batch()
                    
            elif (input_selector == 'houbolt_jr_single'):
                input = houbolt_jr_single()

            return input



    '''#-----------------------------------------------------------------------
    #   METHOD: setFlightDynamicsType
    #   Select method to compute flight trajectory
    #

    #   INPUTS: NONE
    #   OUTPUTS: NONE
    #-----------------------------------------------------------------------'''
    def setFlightDynamicsType(self):
        if self.flight.type == '2DOF':
            #self.flight.get = self.get2DOFflightDynamics()
            pass

        else: 
            error('Flight dynamics mode #s has not been specialized.', self.flight.type)


    '''#-----------------------------------------------------------------------
    #   METHOD: get2DOFflightDynamics
    #   Compute the 2D trajectory of the rocket's flight
    #
    #   INPUTS: NONE
    #   OUTPUTS: NONE
    #-----------------------------------------------------------------------'''
    #def get2DOFflightDynamics(self):

    #    # Make a copy of propulsion, utilities and flight
    #    prop                    = self.rocket.propulsion
    #    nozzle                  = prop.nozzle
    #    perf                    = prop.performance
    #    u                       = self.util
    #    fl                      = self.flight

    #    # Setup masses
    #    mdry                    = self.input.mass.dry * ones[self.input.sim.numpt]
    #    mprop                   = prop.getMprop()
    #    mdot                    = prop.getMdot()
    #    m                       = mdry + mprop

    #    # Misc.
    #    Cd                      = self.rocket.airframe.aero.cd                                      # Cd curve
    #    dt                      = self.designVars.dt                                                # Time step
    #    A                       = pi * (self.designVars.diameter/2)^2                               # Frontal area
    #    eff                     = prop.settings.efficiency                                         # Combustion efficiency
    #    OF                      = prop.getOF()                                                     # OF Ratios
    #    cnv                     = self.input.settings.cnv

    #    # Beginning of 2DOF flight dynamics
    #    atmos                   = u.stdAtmos(fl.y[1][1])

    #    # After engine ignition
    #    perf.Pcc[1][1]          = perf.cstar(OF[1][1])*mdot[1][1]/nozzle.throat.A/cnv              # Chamber Pressure
    #    combustion              = prop.combustion.get(OF[1][1], perf.Pcc[1][1], nozzle.exp)        # Compute combustion
    #    perf.Tcc[1][1]          = combustion.Tcc
    #    perf.Pe[1][1]           = combustion.Pe
    #    perf.Te[1][1]           = combustion.Te

    #    alt_corr                = (combustion.Pe - atmos.P) * nozzle.exit.A                        # Altitude correction

    #    perf.thrust[1][1]       = prop.performance.Mdot[1][1]* prop.settings.efficiency* combustion.Isp * u.g0 + alt_corr

    #    fl.Ay[1][1]             = perf.thrust[1][1]*cosd(fl.theta[1][1]) / m[1][1] - u.g0
    #    fl.Ax[1][1]             = perf.thrust[1][1]*sind(fl.theta[1][1]) / m[1][1]

    #    fl.theta[1][1]          = self.designVars.thetaL
        
    #    # Time stepping
    #    for i in range(2, self.input.sim.numpt):

    #        # Atmospheric conditions
    #        atmos               = u.stdAtmos(fl.y[i-1][1])                                       # Get atmospheric conditions

    #        # Combustion
    #        perf.Pcc[i][1]      = (perf.cstar(OF[i])*mdot[i]/nozzle.throat.A)/cnv                  # Chamber pressure (Pa)
    #        combustion          = prop.combustion.get(OF[i], perf.Pcc[i], nozzle.exp)              # Compute combustion

    #        perf.Isp[i][1]      = combustion.Isp                                                   # Isp
    #        perf.Pe[i][1]       = combustion.Pe                                                    # Exit pressure
    #        perf.Te[i][1]       = combustion.Te
    #        perf.Tcc[i][1]      = combustion.Tcc

    #        # Compute forces on rocket
    #        alt_corr            = (perf.Pe[i][1] - atmos.P) * nozzle.exit.A                        # Altitude correction

    #        perf.thrust[i][1]   = perf.Mdot[i][1] * perf.Isp[i][1]    * u.g0 * eff + alt_corr   # Thrust
    #        fl.drag[i][1]       = 0.5 * atmos.rho * Cd(fl.Ma[i-1][1]) * (fl.V[i-1][1]^2) * A      # Drag
            
    #        # Accelerations
    #        fl.Ay[i][1]         =(perf.thrust[i][1] - fl.drag[i][1])* cosd(fl.theta[i-1][1]) / m[i][1] - u.g0
    #        fl.Ax[i][1]         =(perf.thrust[i][1] - fl.drag[i][1])* sind(fl.theta[i-1][1]) / m[i][1]
    #        # Speeds
    #        fl.u[i][1]          = fl.u[i-1][1] + fl.Ax[i][1] * dt                                  # Velocity in x direction at time t
    #        fl.v[i][1]          = fl.v[i-1][1] + fl.Ay[i][1] * dt                                  # Velocity in y direction at time t
    #        fl.V[i][1]          = sqrt(fl.u[i][1]^2 + fl.v[i][1]^2)                                  # Total velocity at time t

    #        # Positions
    #        fl.y[i][1]          = fl.y[i-1][1] + fl.v[i][1] * dt + 0.5 * fl.Ay(i,1) * dt^2
    #        fl.x[i][1]          = fl.x[i-1][1] + fl.u[i][1] * dt + 0.5 * fl.Ax(i,1) * dt^2
    #        fl.s[i][1]          = sqrt(fl.x[i][1]^2 + fl.y[i][1]^2)                                # Total distance at time t

    #        # Loads and mach number
    #        fl.Ma[i][1]         = fl.V[i][1]/atmos.a                                               # Mach number at time t
    #        fl.g[i][1]          = sqrt(fl.Ay[i][1]^2 + fl.Ax[i][1]^2) / u.g0                    # Acceleration (G)
    #        fl.force[i][1]      = m[i][1]*(sqrt(fl.Ay[i][1]^2 + fl.Ax[i][1]^2))+ fl.drag[i][1]

    #        # Gravity turn
    #        if (i > 2) and (fl.s[i][1] > self.input.settings.LRail) :                                      # If clear from launch rail

    #            vt              = [fl.u[i-1][1], fl.v[i-1][1]]                                     # Velocity at i-1
    #            vtp             = [fl.u[i][1], fl.v[i][1]]                                     # Velocity at i
    #            mag             = abs(fl.V[i][1]) * abs(fl.V[i-1][1])                              # Product of total velocitues
    #            dtheta          = acosd(min(dot(vt, vtp)/mag, 1))                                  # delta theta
    #            fl.theta[i][1]  = fl.theta[i-1][1] + dtheta                                        # Update theta
    #        else:

    #            fl.theta[i][1]      = fl.theta[i-1][1]                                             # Update theta
            
        

    #    # Write to classes
    #    fl.m                    = m
    #    fl.altBO                = fl.y[: 1]
    #    self.flight             = fl
    #    prop.performance        = perf
    
    '''#-------------------------------------------------------------------------------------------
    #   METHOD: setDesignVariables
    #   Set design variables for all classes that utilize them
    #   
    #   INPUTS: NONE
    #   OUTPUTS: NONE
    #-------------------------------------------------------------------------------------------  '''      
    #def setDesignVars(self, var):
        
    #    self.designVars                              = var
    #    self.rocket.propulsion.designVars            = var
    #    self.rocket.airframe.designVars              = var
    #    self.rocket.propulsion.combustion.designVars = var
    #    self.rocket.propulsion.nozzle.designVars     = var
        
    #    for i in range(1,size(self.rocket.propulsion.propellants.tanks),1):
    #        self.rocket.propulsion.propellants.tanks[i][1].designVars            = var
        
    
    
    #'''#-------------------------------------------------------------------------------------------
    ##   METHOD: buildDesignVariables
    ##   Build the designVars property that holds all possible
    ##   combinations of design variables
    ##   
    ##   INPUTS: NONE
    ##   OUTPUTS: NONE
    ##-------------------------------------------------------------------------------------------'''
    #def buildDesignVariables(self):
        
    #    des = self.input.design
    #    num_simulations = length(des.tBurn)   
    #    self.batch_vars = cells(num_simulations, 1)
    #    local = []
        
    #    for i in range(1,num_simulations):
                                    
    #        local.tBurn         = self.input.design.tBurn[i]
    #        local.thetaL        = self.input.design.thetaL[i]
    #        local.Pcc           = self.input.design.Pcc[i]
    #        local.mDotox        = self.input.design.mDotox[i]
    #        local.OF            = self.input.design.OF[i]
            
    #        local.diameter      = self.input.design.diameter
    #        local.injCd         = self.input.design.injCd
            
    #        local.dt            = local.tBurn/(self.input.sim.numpt+1)
            
    #        self.batch_vars[i] = local
                    
    
    
    #'''------------------------------------------------------------------------------------------
    ##   METHOD: batch_sim
    ##   Perform a batch of simulations through all provided design
    ##   variable combinations
    ##   
    ##   INPUTS: NONE
    ##   OUTPUTS: NONE
    ##-------------------------------------------------------------------------------------------'''
    #def batch_sim(self):
        
    #    self.buildDesignVariables()
    #    self.batch_sim_results = cells(length(self.batch_vars), 2)
        
    #    for i in range(1,length(self.batch_vars)):
    #        self.setDesignVars(self.batch_vars[i])
            
    #        self.fly()
            
    #        self.batch_sim_results[i][1] = self.designVars
    #        self.batch_sim_results[i][2] = self.flight
        
    
    
    #'''-------------------------------------------------------------------------------------------
    ##   METHOD: fly
    ##   Perform complete simulation of the rocket's flight
    ##   
    ##   INPUTS: NONE
    ##   OUTPUTS: NONE
    ##-------------------------------------------------------------------------------------------'''
    #def fly(self):

    #    self.flight.t               = linspace(0, self.designVars.tBurn, self.numpt)
    
    #    self.rocket.propulsion.getBlowdown()
    #    self.rocket.propulsion.getCstar()
        
    #    altBO       = 1.5*self.flight.altBO
    #    combustion  = self.rocket.propulsion.combustion.get(self.designVars.OF, self.designVars.Pcc, [])                  

    #    convCrit    = self.input.sim.altConvCrit
        
    #    while (abs(self.flight.altBO - altBO) > convCrit):
        
    #        altBO   = self.flight.altBO + self.input.sim.relax * (altBO - self.flight.altBO)
    #        self.rocket.propulsion.nozzle.get(altBO, combustion.gamm)
    #        self.flight.get()
        
        
    #    self.rocket.propulsion.getCG()
    #    self.write_engine_file()
    
    
    #'''#-------------------------------------------------------------------------------------------
    ##   METHOD: write_engine_file
    ##   Write the engine file to interface with OpenRocket
    ##   
    ##   INPUTS: NONE
    ##   OUTPUTS: NONE
    ##-------------------------------------------------------------------------------------------'''
    #def write_engine_file(self):
        
    #    time        = linspace(0, self.designVars.tBurn, self.input.sim.numpt)
    #    initWt      = self.rocket.propulsion.m[1][1] * 1000
    #    propWt      = self.rocket.propulsion.performance.Mprop[1][1] * 1000
        
    #    d_e         = self.rocket.propulsion.nozzle.exit.d * 1000
    #    d_t         = self.rocket.propulsion.nozzle.throat.d * 1000
        
    #    a           = fullfile('Engine Files', self.input.engine.engfile)
    #    fid         = open(a, 'w')
        
    #    cg          = self.rocket.propulsion.cg
    #    thrust      = self.rocket.propulsion.performance.thrust
    #    m           = self.rocket.propulsion.m
        
    #    fid.write( '<engine-database>\n')
    #    fid.write( ' <engine-list>\n')
    #    fid.write( '  <engine  mfg="#s" code="#s" Type="Liquid" dia="#f" len="#f" initWt="#f" propWt="#f"\n', self.input.engine.Mfg, self.input.engine.name, self.designVars.diameter*1000,self.rocket.propulsion.l[1][1]*1000, initWt, propWt)
    #    fid.write( 'delays="0" auto-calc-mass="0" auto-calc-cg="1" avgrocket.thrust="#f"\n', mean(thrust))
    #    fid.write( 'peakrocket.thrust="#f" throatDia="#f" exitDia="#f" Itot="#f" burn-time="#f"\n', max(thrust), d_t, d_e, trapz(time, thrust), self.designVars.tBurn)
    #    fid.write( 'massFrac="0" engine.Isp_curve="#f" tDiv="10" tStep="-1." tFix="1" FDiv="10" FStep="-1." FFix="1"\n', mean(self.rocket.propulsion.performance.Isp[2]))
    #    fid.write( 'mDiv="10" mStep="-1." mFix="1" cgDiv="10" cgStep="-1." cgFix="1">\n')
    #    fid.write( '\n')
    #    fid.write( '\t<data>\n')
        
    #    for i in range(1,self.input.sim.numpt):
    #        fid.write( '\t <eng-data cg="#f" f="#f" m="#f" t="#f"/>\n', cg[i][1], thrust[i][1], m[i][1]*1000, time[i][1])
        
        
    #    fid.write( '\t</data>\n')
    #    fid.write( '  </engine>\n')
    #    fid.write( ' </engine-list>\n')
    #    fid.write( '</engine-database>')
        
    #    fid.close()
    

    ''' 
        TODO        
    def checkInputs(self)
        
    

        '''       

