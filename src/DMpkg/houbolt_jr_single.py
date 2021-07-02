import math
import yaml
import DMpkg as rocket
from DMpkg.utilitiesClass import cellss

def houbolt_jr_single(inp_path):

    with open(inp_path, "r") as f:
        inp_dic = yaml.load(f)

    # engine_dic = inp_dic.get("engine")
    # settings_dic = inp_dic.get("settings")
    # mass_dic = inp_dic.get("mass")
    # design_dic = inp_dic.get("design")
    # sim_dic = inp_dic.get("sim")
    # fPres_dic = inp_dic.get("fPres")
    # fuel_dic = inp_dic.get("fuel")
    # oxPres_dic = inp_dic.get("oxPres")
    # oxPres_dic = inp_dic.get("oxPres")

    # inp_dic["mass"]["data"] = get_mass_budget(inp_dic.get("mass").get("data"))

    """
    conversions and calculations that cannot be handled in the input.yaml file
    """
    
    inp_dic["fPres"]["Pinit"] = inp_dic["fPres"]["Pinit"] * inp_dic["settings"]["cnv"] # converting from psi to Pa
    inp_dic["fPres"]["mInit"] = inp_dic["fPres"]["vTank"] * inp_dic["fPres"]["Rhoinit"]

    inp_dic["fuel"]["Pinit"] = inp_dic["fuel"]["Pinit"] * inp_dic["settings"]["cnv"]
    inp_dic["fuel"]["vTank"] = inp_dic["fuel"]["mInit"] * (1 + inp_dic["fuel"]["ullage"]] / inp_dic["fuel"]["Rhoinit"] # converting from psi to Pa
    inp_dic["fuel"]["lTank"] = inp_dic["fuel"]["vTank"] / (math.pi*(0.5*inp_dic["design"]["diameter"] - inp_dic["fuel"]["tTank"]) ** 2)

    inp_dic["oxPres"]["Pinit"] = inp_dic["oxPres"]["Pinit"] * inp_dic["settings"]["cnv"] # converting from psi to Pa
    inp_dic["oxPres"]["mInit"] = inp_dic["oxPres"]["vTank"] * inp_dic["oxPres"]["Rhoinit"]

    inp_dic["ox"]["Pinit"] = inp_dic["ox"]["Pinit"] * inp_dic["settings"]["cnv"] # converting from psi to Pa
    inp_dic["ox"]["vTank"] = inp_dic["ox"]["mInit"] * (1 + inp_dic["ox"]["ullage"]] / inp_dic["ox"]["Rhoinit"]
    inp_dic["ox"]["lTank"] = inp_dic["ox"]["vTank"] / (math.pi*(0.5*inp_dic["design"]["diameter"] - inp_dic["ox"]["tTank"]) ** 2)

    inp_dic["props"] = cellss(4, 3) # cannot change to numpy array because of multiple data types
    inp_dic["props"][0][0] = 'Pressurant'
    inp_dic["props"][0][1] = inp_dic["fPres"]
    inp_dic["props"][0][2] = 0
    inp_dic["props"][1][0] = 'Fuel'
    inp_dic["props"][1][1] = inp_dic["fuel"]
    inp_dic["props"][1][2] = 1
    inp_dic["props"][2][0] = 'Pressurant'
    inp_dic["props"][2][1] = inp_dic["oxPres"]
    inp_dic["props"][2][2] = 
    inp_dic["props"][3][0] = 'Oxidizer'
    inp_dic["props"][3][1] = inp_dic["ox"]
    inp_dic["props"][3][2] = 3   

    """
    look into what to do with:
    input.fPres.Pinit
    input.fPres.mInit 
    input.fuel.lTank (read from mass budget)
    input.fuel.Pinit
    input.fuel.vTank
    input.fuel.lTank
    input.oxPres.Pinit
    input.oxPres.mInit
    input.ox.Pinit
    input.ox.vTank
    input.ox.lTank
    all of props

    completed except:
    input.fuel.lTank
    and input.mass.data
    """

    return inp_dic
