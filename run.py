from model import *
import matplotlib.pyplot as plt
from mesa.batchrunner import BatchRunner
from server import server
import time

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
'''



'''
# Single run
params = {"N_fan": 328,
          "N_hool": 110,
          "N_pol": 46,
          "N_riopol": 16,
          "twogroup_switch": False,
          "riot_police_grouped": False}

start_time = time.time()
model = AggressionModel(N_fan = 328, N_hool = 110, N_pol = 46, N_riopol = 16, width = 100, height = 100, twogroup_switch = False, riot_police_grouped = False, size_riot_police_groups = 5)
for i in range(5400):
    model.step()
    print("step: " + str(i) + ' at time: ' + str(time.time()-start_time))

data = model.datacollector.get_model_vars_dataframe()
data.plot()
plt.show()



#Batch run
#batch_run = BatchRunner(AggressionModel,
#                        parameter_values=params,
#                        iterations=1,
#                        max_steps=5400,
#                        model_reporters={"Attacks": compute_attacks,
#                             "Attacked": compute_attacked,
#                             "Police Interuptions": police_interutions})
#batch_run.run_all()

#run_data = batch_run.get_model_vars_dataframe()
#run_data.to_csv('basecase.csv')

#plt.scatter(run_data.N_riopol, run_data.Attacks)
#plt.show()
'''