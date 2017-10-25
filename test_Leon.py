from model import *

model = AggressionModel(N_fan = 188, N_hool = 62, N_pol = 150, N_riopol = 100, twogroup_switch = False)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('188-62-150-100-F.csv')

model = AggressionModel(N_fan = 188, N_hool = 62, N_pol = 125, N_riopol = 125, twogroup_switch = False)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('188-62-125-125-F.csv')

model = AggressionModel(N_fan = 188, N_hool = 62, N_pol = 200, N_riopol = 50, twogroup_switch = False)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('188-62-200-50-F.csv')

model = AggressionModel(N_fan = 125, N_hool = 125, N_pol = 150, N_riopol = 100, twogroup_switch = False)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('125-125-150-100-F.csv')

model = AggressionModel(N_fan = 125, N_hool = 125, N_pol = 125, N_riopol = 125, twogroup_switch = False)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('225-225-125-125-F.csv')

model = AggressionModel(N_fan = 125, N_hool = 125, N_pol = 200, N_riopol = 50, twogroup_switch = False)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('125-125-200-50-F.csv')

model = AggressionModel(N_fan = 219, N_hool = 31, N_pol = 150, N_riopol = 100, twogroup_switch = False)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('219-31-150-100-F.csv')

model = AggressionModel(N_fan = 219, N_hool = 31, N_pol = 125, N_riopol = 125, twogroup_switch = False)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('219-31-125-125-F.csv')

model = AggressionModel(N_fan = 219, N_hool = 31, N_pol = 200, N_riopol = 50, twogroup_switch = False)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('219-31-200-50-F.csv')