from model import *
import matplotlib.pyplot as plt
import numpy as np
from mesa.batchrunner import BatchRunner
from server import server

server.port = 8521 # The default
server.launch()

'''
N_fan = 500
N_hool = 100
N_pol = 60
N_riopol = 12
width = 100
height = 100
twogroup_switch = False
riot_police_grouped = True
size_riot_police_groups = 5

model = AggressionModel(N_fan, N_hool, N_pol, N_riopol, width, height, twogroup_switch, riot_police_grouped, size_riot_police_groups)
for i in range(100):
    model.step()
fights = model.datacollector.get_model_vars_dataframe()
fights.plot()
plt.show()
agent_aggression = model.datacollector.get_agent_vars_dataframe()
print(agent_aggression.head())


#Plot wealth at end of simulation (After Run 99)
end_aggression = agent_aggression.xs(99, level="Step")["Aggression"]
end_aggression.hist(bins=range(agent_aggression.Aggression.max()+1))
plt.show()

#Plot wealth of individual agent (14)
one_agent_aggression = agent_aggression.xs(14, level="AgentID")
one_agent_aggression.Aggression.plot()
plt.show()

#Batch run
params = {"width": 10,
          "height": 10,
          "N": range(10, 500, 10)}
batch_run = BatchRunner(AggressionModel,
                        parameter_values=params,
                        iterations=5,
                        max_steps=100,
                        model_reporters={"Gini": compute_gini})
batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
run_data.head()
plt.scatter(run_data.N, run_data.Gini)
plt.show()
'''
