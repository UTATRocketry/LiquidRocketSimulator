from rocketcea.cea_obj import CEA_Obj
from pylab import *

### Plots Cstar Values for LOX/LH2 for several values of chamber pressure and a range of mixture ratio

# range of chamber pressures [psia]
pcL = [ 2000., 500., 70.]

# create CEA object (oxidizer: liquid oxygen, fuel: liquid hydrogen)
ispObj = CEA_Obj(propName='', oxName='LOX', fuelName="LH2")

for Pc in pcL:
    # performance property ~ characteristic velocity
    cstarArr = []

    # transport properties ~ viscosity, conductivity, prandtl number
    visc_arr = []
    conductivity_arr = []
    prandtl_num_arr = []

    # mixture ratio
    MR = 2.0
    mrArr = []

    while MR < 8.0:
        transport_properties = ispObj.get_Chamber_Transport(Pc=Pc, MR=MR, eps=40.0, frozen=0)

        cstarArr.append(ispObj.get_Cstar(Pc=Pc, MR=MR))
        mrArr.append(MR)

        visc_arr.append(transport_properties[1])
        conductivity_arr.append(transport_properties[2])
        prandtl_num_arr.append(transport_properties[3])

        MR += 0.05
    plot(mrArr, cstarArr, label='Pc=%g psia'%Pc)

# additional plot features
legend(loc='best')
grid(True)
title( ispObj.desc )
xlabel( 'Mixture Ratio' )
ylabel( 'Cstar (ft/sec)' )
savefig('cea_cstar_plot.png', dpi=120)

show()