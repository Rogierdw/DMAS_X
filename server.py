from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import AggressionModel
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from TopAgent import *

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "r": 0.5}

    if type(agent) is Fan:
        portrayal['Color'] = 'green'

    if type(agent) is Hooligan:
        portrayal['Color'] = 'red'

    if type(agent) is Police:
        portrayal['Color'] = 'blue'

    if type(agent) is Riot_Police:
        portrayal['Color'] = 'purple'

    if agent.walkable != 0:
        portrayal['Color'] = 'black'
        portrayal['r'] = 1.0

    return portrayal

grid = CanvasGrid(agent_portrayal, 100, 100, 500, 500)

n_slider_fan = UserSettableParameter('slider', "Number of Fans", 170, 2, 400, 1)
n_slider_hool = UserSettableParameter('slider', "Number of Hooligans", 30, 2, 400, 1)
n_slider_pol = UserSettableParameter('slider', "Number of Police", 170, 2, 400, 1)
n_slider_riopol = UserSettableParameter('slider', "Number of Riot police", 30, 2, 400, 1)




chart = ChartModule([{"Label": "Riot",
                      "Color": "Black"}],
                    data_collector_name='datacollector')

server = ModularServer(AggressionModel, # Which model
                       [grid, chart], # Add what to page
                       "Aggression Model", # Title
                       {"N_fan": n_slider_fan, # Actual parameters for __init__ of model
                        "N_hool": n_slider_hool,
                        "N_pol": n_slider_pol,
                        "N_riopol": n_slider_riopol,
                        "width": 100, "height": 100})



