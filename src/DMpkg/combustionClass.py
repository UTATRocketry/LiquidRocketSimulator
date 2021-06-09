from src.DMpkg.houbolt_jr_single import houbolt_jr_single
import DMpkg as rocket
import numpy as np

class combustionClass:
    def __init__(self, input) -> None:
        self.input = houbolt_jr_single()
        self.util = utilitiesClass(self.input)

    def getPropellantTags(self):
        self.fuelTag = self.input.get("fuel")
        self.oxidizerTag = self.input.get("ox")

    



