from model import *

model = AggressionModel(N_fan = 338, N_hool = 112, N_pol = 30, N_riopol = 20, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('338-112-30-20-F.csv')

model = AggressionModel(N_fan = 338, N_hool = 112, N_pol = 25, N_riopol = 25, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('338-112-25-25-F.csv')

model = AggressionModel(N_fan = 338, N_hool = 112, N_pol = 40, N_riopol = 10, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('338-112-40-10-F.csv')

model = AggressionModel(N_fan = 225, N_hool = 225, N_pol = 30, N_riopol = 20, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('225-225-30-20-F.csv')

model = AggressionModel(N_fan = 225, N_hool = 225, N_pol = 25, N_riopol = 25, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('225-225-25-25-F.csv')

model = AggressionModel(N_fan = 225, N_hool = 225, N_pol = 40, N_riopol = 10, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('200-200-40-10-F.csv')

model = AggressionModel(N_fan = 394, N_hool = 56, N_pol = 30, N_riopol = 20, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('394-56-30-20-F.csv')

model = AggressionModel(N_fan = 394, N_hool = 56, N_pol = 25, N_riopol = 25, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('394-56-25-25-F.csv')

model = AggressionModel(N_fan = 394, N_hool = 56, N_pol = 40, N_riopol = 10, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('394-56-40-10-F.csv')