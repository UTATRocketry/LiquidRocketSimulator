from propertyClass import *
import math
from utilitiesClass import *

def houbolt_jr_single():

    with open(inp_path, "r") as f:
            inp_dic = json.load(f)

    # engine_dic = inp_dic.get("engine")
    # settings_dic = inp_dic.get("settings")
    # mass_dic = inp_dic.get("mass")
    # design_dic = inp_dic.get("design")
    # sim_dic = inp_dic.get("sim")
    # fPres_dic = inp_dic.get("fPres")
    # fuel_dic = inp_dic.get("fuel")
    # oxPres_dic = inp_dic.get("oxPres")
    # oxPres_dic = inp_dic.get("oxPres")

    """
    look into what to do with:
    input.fPres.Pinit
    input.fPres.mInit 
    input.fuel.lTank
    input.fuel.Pinit
    input.fuel.vTank
    input.fuel.lTank
    input.oxPres.Pinit
    input.oxPres.mInit
    input.ox.Pinit
    input.ox.vTank
    input.ox.lTank

    all of props
    """

    return inp_dic


