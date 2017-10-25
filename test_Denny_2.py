from model import *

model = AggressionModel(N_fan = 180, N_hool = 120, N_pol = 180, N_riopol = 120, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('180-120-180-120-T.csv')

model = AggressionModel(N_fan = 180, N_hool = 120, N_pol = 150, N_riopol = 150, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('180-120-150-150-T.csv')

model = AggressionModel(N_fan = 180, N_hool = 120, N_pol = 240, N_riopol = 60, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('180-120-240-60-T.csv')

model = AggressionModel(N_fan = 150, N_hool = 150, N_pol = 180, N_riopol = 120, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('150-150-180-120-T.csv')

model = AggressionModel(N_fan = 150, N_hool = 150, N_pol = 150, N_riopol = 150, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('150-150-150-150-T.csv')

model = AggressionModel(N_fan = 150, N_hool = 150, N_pol = 240, N_riopol = 60, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('150-150-240-60-T.csv')

model = AggressionModel(N_fan = 240, N_hool = 60, N_pol = 180, N_riopol = 120, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('240-60-180-120-T.csv')

model = AggressionModel(N_fan = 240, N_hool = 60, N_pol = 150, N_riopol = 150, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('240-60-150-150-T.csv')

model = AggressionModel(N_fan = 240, N_hool = 60, N_pol = 240, N_riopol = 60, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('240-60-240-60-T.csv')