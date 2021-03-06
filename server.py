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

    if two_groups:
        if agent.team:
            portrayal["Color"] = 'green'
        else:
            portrayal["Color"] = "red"

    if type(agent) is Fan:
        portrayal['r'] = '0.3'
    if type(agent) is Hooligan:
        portrayal['r'] = '0.6'

    if type(agent) is Police:
        portrayal['Color'] = 'blue'
        portrayal['r'] = '0.3'

    if type(agent) is Riot_Police:
        portrayal['Color'] = 'blue'
        portrayal['r'] = '0.6'

    if agent.timesincefight != 0:
        portrayal['Color'] = 'black'
        portrayal['r'] = 1.0

    return portrayal

grid = CanvasGrid(agent_portrayal, 100, 100, 1000, 1000)

two_groups = UserSettableParameter('checkbox', 'Two groups', value=True)
group_a_proportion = UserSettableParameter('slider', "Group A proportion", 0.25, 0, 0.50, 0.05)
riot_police_grouped = UserSettableParameter('checkbox', 'Grouped Riot Police', value = False)

n_slider_fan = UserSettableParameter('slider', "Number of Fans", 300, 0, 800, 1)
n_slider_hool = UserSettableParameter('slider', "Number of Hooligans", 200, 0, 200, 1)
n_slider_pol = UserSettableParameter('slider', "Number of Police", 0, 0, 200, 1)
n_slider_riopol = UserSettableParameter('slider', "Number of Riot police", 0, 0, 50, 1)

#size_riot_police_groups = UserSettableParameter("slider", "initial group size of Riot Police", 5, 1, 5, 1)

chart = ChartModule([{"Label": "Aggression",
                      "Color": "Red"}],
                    data_collector_name='datacollector')

chart2 = ChartModule([{"Label": "Attacks",
                      "Color": "Black"}],
                    data_collector_name='datacollector')


chart4 = ChartModule([{"Label": "Police interuptions",
                      "Color": "Blue"}],
                    data_collector_name='datacollector')


server = ModularServer(AggressionModel, # Which model
                       [grid, chart, chart2, chart4], # Add what to page
                       "Aggression Model", # Title
                       {"N_fan": n_slider_fan, # Actual parameters for __init__ of model
                        "N_hool": n_slider_hool,
                        "N_pol": n_slider_pol,
                        "N_riopol": n_slider_riopol,
                        "width": 100, "height": 100,
                        "twogroup_switch": two_groups,
                        "group_a_proportion": group_a_proportion,
                        "riot_police_grouped": riot_police_grouped})



