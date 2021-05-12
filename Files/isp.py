from rocketcea.cea_obj import CEA_Obj
from pylab import *

Pc = 350.

ispIRFNA = CEA_Obj(propName='', oxName='N2O', fuelName="Ethanol")

for e in [2., 5., 10., 20., 50.]:
    ispArr = []
    MR = 1.1
    mrArr = []
    while MR < 6.:
        ispArr.append( ispIRFNA(Pc, MR, e ))
        mrArr.append(MR)
        MR += 0.05
    plot(mrArr, ispArr, label='AreaRatio %g'%e)

legend(loc='best')
grid(True)
title( ispIRFNA.desc )
xlabel( 'Mixture Ratio' )
ylabel( 'Isp ODE (sec)' )
savefig('isp_plot.png', dpi=120)

show()