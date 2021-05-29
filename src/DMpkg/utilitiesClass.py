import numpy as np
import DMpkg as rocket

class utilitiesClass:
    def __init__(self, input):
        self.g0          = 9.8056
        self.earthR      = 6371e3

        self.R           = 8314
        self.airR        = 287.05
        self.n2R         = 8314/28
        self.airM        = 0.0289644 #molar mass of air (kg/mol)
        self.airGamma    = 1.4

        self.cnv         = 6894.76

        self.coolProp_conversions = ('C2H5OH',  'Ethanol')

        self.input       = None
        self.zeroArray   = None
        self.noxProp     = None
        self.nitrogen    = None
        self.cp          = None
        self.coolprop_alias  = None



        self.zeroArray           = np.zeros((input.sim.numpt, 1))

        self.noxProp             = rocket.propertyClass()
        self.noxProp.rho_c       = 452
        self.noxProp.Tc          = 309.57
        self.noxProp.Pc          = 7.251e6

        self.noxProp.Coefs       = rocket.propertyClass()
        self.noxProp.Coefs.V1    = 96.512
        self.noxProp.Coefs.V2    = -4045
        self.noxProp.Coefs.V3    = -12.277
        self.noxProp.Coefs.V4    = 2.886e-5
        self.noxProp.Coefs.V5    = 2

        self.noxProp.Coefs.T1    = 2.3215e7
        self.noxProp.Coefs.T2    = 0.384
        self.noxProp.Coefs.T3    = 0
        self.noxProp.Coefs.T4    = 0

        self.noxProp.Coefs.Q1    = 2.781
        self.noxProp.Coefs.Q2    = 0.27244
        self.noxProp.Coefs.Q3    = 309.57
        self.noxProp.Coefs.Q4    = 0.2882

        self.noxProp.Coefs.D1    = 0.2934e5
        self.noxProp.Coefs.D2    = 0.3236e5
        self.noxProp.Coefs.D3    = 1.1238e3
        self.noxProp.Coefs.D4    = 0.2177e5
        self.noxProp.Coefs.D5    = 479.4

        self.noxProp.Coefs.E1    = 6.7556e4
        self.noxProp.Coefs.E2    = 5.4373e1
        self.noxProp.Coefs.E3    = 0
        self.noxProp.Coefs.E4    = 0
        self.noxProp.Coefs.E5    = 0

        self.noxProp.Coefs.b1    = 1.72328
        self.noxProp.Coefs.b2    = -0.8395
        self.noxProp.Coefs.b3    = 0.5106
        self.noxProp.Coefs.b4    = 0.10412

        self.noxProp.Coefs.q1    = -6.71893
        self.noxProp.Coefs.q2    = 1.35966
        self.noxProp.Coefs.q3    = 1.3779
        self.noxProp.Coefs.q4    = -4.051

        self.nitrogen            = rocket.propertyClass()
        self.nitrogen.Coefs      = rocket.propertyClass()
        self.nitrogen.Coefs.C1   = 0.28883e5
        self.nitrogen.Coefs.C2   = 0
        self.nitrogen.Coefs.C3   = 0
        self.nitrogen.Coefs.C4   = 0
        self.nitrogen.Coefs.C5   = 0

        self.nitrogen.h          = rocket.propertyClass()
        self.nitrogen.h.theta    = [0.90370032155133,\
                                      -3.99164830787538,\
                                       4.44554878990612,\
                                      -1.68387394930366,\
                                       1.84282855081908,\
                                      -2.71807522455834,\
                                       1.80658523674363,\
                                      -0.00026662830718,\
                                       0.16405364316350]

        self.nitrogen.h.alpha    = [1,               \
                                       0.45607085009281,\
                                       0.99224794564113,\
                                       1.58495789262624,\
                                       0.53133147588636,\
                                       1.29132167947510,\
                                       1.44008913900161,\
                                       2.74997487910292,\
                                       2.36611999082672]
                                   
        self.nitrogen.l          = rocket.propertyClass()

        self.nitrogen.l.theta    = [0.46742656471647,\
                                      -0.53799565472298,\
                                      -9.22454428760102,\
                                       9.15603503101003,\
                                       3.18808664459882,\
                                       0.30163700042055,\
                                      -0.27300234680706,\
                                      -1.00749719408221,\
                                      -1.49106816983329]

        self.nitrogen.l.alpha    = [1,               \
                                       1.41102397459172,\
                                       0.33562799290636,\
                                       0.79810083070486,\
                                       0.01008992455881,\
                                       2.53968667359886,\
                                       2.51281397715323,\
                                       1.20879498088509,\
                                       1.69572064361084]
                                   
        self.nitrogen.Tc         = 126.2
        self.nitrogen.Pc         = 492.314
            
        #py.importlib.import_module('CoolProp.CoolProp')
        #self.cp = load_cp.PropsSI
            
        #self.coolprop_alias = cells(1, 2)
        #self.coolprop_alias[1][1] = 'C2H5OH'
        #self.coolprop_alias[1] [2] = 'Ethanol'





    #def coolprop(needed, p1, p1val, p2, p2val, name):
    #    if name == 'C2H5OH':
    #        name = 'ethanol'
    #    output = py.CoolProp.CoolProp.PropsSI(needed, p1, p1val, p2, p2val, name)

    def stdAtmos(altitude):

            Ru  = obj.R / 1000 #universal gas constant (J/mol/K)
            Ra  = obj.airR

            if ( 0 <= altitude) and (altitude < 11000):
                Lb      = -0.0065 #Lapse rate (K/m)
                Tb      = 288.15 #Standard temperature (K)
                Pb      = 101325 #Static pressure (Pa)
                h0      = 0
                P       = Pb * (Tb/(Tb + Lb*(altitude - h0))) ^ (obj.g0*obj.airM/Ru/Lb)
                T       = Tb + Lb*(altitude - h0)

            elif ( 11000 <= altitude) and (altitude < 20000):
                Lb      = 0
                Tb      = 216.65
                Pb      = 22632.1
                h1      = 11000
                P       = Pb * exp(-obj.g0*obj.airM*(altitude - h1)/Ru/Tb)
                T       = Tb + Lb*(altitude - h1)

            elif ( 20000 <= altitude) and (altitude < 32000):
                Lb      = 0.001
                Tb      = 216.65
                Pb      = 5474.89
                h2      = 20000
                P       = Pb * (Tb/(Tb + Lb*(altitude - h2))) ^ (obj.g0*obj.airM/Ru/Lb)
                T       = Tb + Lb*(altitude - h2)

            elif (32000 <= altitude) and (altitude < 47000):
                Lb      = 0.0028
                Tb      = 228.65
                Pb      = 868.02
                h3      = 32000
                P       = Pb * (Tb/(Tb + Lb*(altitude - h3))) ^ (g*obj.airM/Ru/Lb)
                T       = Tb + Lb*(altitude - h3)

            elif(47000 <= altitude) and (altitude < 51000):
                Lb      = 0
                Tb      = 270.65
                Pb      = 110.91
                h4      = 47000
                P       = Pb * exp(-obj.g0*obj.airM*(altitude - h4)/Ru/Tb)
                T       = Tb + Lb*(altitude - h4)

            elif(51000 <= altitude) and (altitude < 71000):
                Lb      = -0.0028
                Tb      = 270.65
                Pb      = 66.94
                h5      = 51000
                P       = Pb * (Tb/(Tb + Lb*(altitude - h5))) ^ (obj.g0*obj.airM/Ru/Lb)
                T       = Tb + Lb*(altitude - h5)

            elif(71000 <= altitude) and (altitude < 86000):
                Lb      = -0.002
                Tb      = 214.65
                Pb      = 3.96
                h6      = 71000
                P       = Pb * (Tb/(Tb + Lb*(altitude - h6))) ^ (obj.g0*obj.airM/Ru/Lb)
                T       = Tb + Lb*(altitude - h6)

            else:
                P       = 0
            

            rho         = P / (Ra * T)
            a           = sqrt(1.4 * Ra * T)
            output.P    = P
            output.T    = T
            output.rho  = rho
            output.a    = a
            return output

def cellss(x,y):
    output = []
    for i in range(0,x):
        u  = []
        output.append(u)
        for j in range(0,y):
            t = []
            output[i].append(t)

    return output
    #setattr()
