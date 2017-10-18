from model import *
import matplotlib.pyplot as plt
from mesa.batchrunner import BatchRunner
from server import server

#server.port = 8521 # The default
#server.launch()

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

#Batch run
params = {"N_fan": 255,
          "N_hool": 45,
          "N_pol": 85,
          "twogroup_switch": False,
          "riot_police_grouped": False,
          "N_riopol": range(5,100, 5)}

batch_run = BatchRunner(AggressionModel,
                        parameter_values=params,
                        iterations=1,
                        max_steps=5400,
                        model_reporters={"Attacks": compute_attacks,
                             "Attacked": compute_attacked,
                             "Police Interuptions": police_interutions})
batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
run_data.to_csv('test1.csv')

#plt.scatter(run_data.N_riopol, run_data.Attacks)
#plt.show()