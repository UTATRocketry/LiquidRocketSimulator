from rocketcea.cea_obj import CEA_Obj
from pylab import *

Pc = 350.

tempsOBJ = CEA_Obj(propName='', oxName='N2O', fuelName="Ethanol")

e = 5
tempsArr = []
MR = 1.1
mrArr = []
while MR < 6.:
    tempsArr.append((tempsOBJ.get_Temperatures( Pc=Pc, MR=MR, eps=e))[0])
    mrArr.append(MR)
    MR += 0.05
plot(mrArr, tempsArr, label='AreaRatio %g'%e)

legend(loc='best')
grid(True)
title(tempsOBJ.desc)
xlabel( 'Mixture Ratio' )
ylabel( 'Temperature, K' )
savefig('tempmr_plot.png', dpi=120)

show()