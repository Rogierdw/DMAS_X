from model import *
import matplotlib.pyplot as plt
from mesa.batchrunner import BatchRunner
from server import server
import time

#server.port = 8521 # The default
#server.launch()

# Single run

start_time = time.time()
model = AggressionModel(N_fan = 300, N_hool = 200, N_pol = 0, N_riopol = 0, twogroup_switch = True)
for i in range(5400):
    model.step()
    print("step: " + str(i) + ' at time: ' + str(time.time()-start_time))

data = model.datacollector.get_model_vars_dataframe()
data.to_csv('two_party.csv')
data.plot()
plt.show()






#Batch run
# #params = {"N_fan": 328,
#          "N_hool": 110,
#          "N_pol": 46,
#          "N_riopol": 16,
#          "twogroup_switch": False,
#          "riot_police_grouped": False}
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
