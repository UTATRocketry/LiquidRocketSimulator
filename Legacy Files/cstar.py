from rocketcea.cea_obj_w_units import CEA_Obj
from pylab import *

pcL = [100., 200., 350., 500., 600.]

ispObj = CEA_Obj(propName='', oxName='N2O', fuelName="Ethanol", cstar_units="m/s")

for Pc in pcL:
    cstarArr = []
    MR = 1.1
    mrArr = []
    while MR < 6.0:
        cstarArr.append( ispObj.get_Cstar( Pc=Pc, MR=MR))
        mrArr.append(MR)
        MR += 0.05
    plot(mrArr, cstarArr, label='Pc=%g psia'%Pc)

legend(loc='best')
grid(True)
title( ispObj.desc )
xlabel( 'Mixture Ratio' )
ylabel( 'Cstar (m/s)' )
savefig('cea_cstar_plot.png', dpi=120)

show()