import src as rocket
import numpy as np

class rocketClass:
    
    def __init__(self, input = None, utilities = None, propulsion = None, airframe = None) -> None:
        if input == None:
            raise Exception('ERROR: rocketClass constructor executed without input arguments')
        
        else:
            self.input                  = input
            #self.propulsion             = propulsionClass(input)
            self.airframe               = rocket.propertyClass()
            self.utilities              = rocket.utilitiesClass(input)

            self.airframe.drag_file     = 'src\Drag_Data_Houbolt_Jr.csv'
            self.drag_model()
            
    def drag_model(self):
        drag_data = np.genfromtxt(self.airframe.drag_file, delimiter = ',')
        self.airframe.cd = np.polynomial.Polynomial.fit(drag_data[:,0], drag_data[:,1], deg=3)