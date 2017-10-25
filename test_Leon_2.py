from model import *

model = AggressionModel(N_fan = 330, N_hool = 220, N_pol = 30, N_riopol = 20, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('330-220-30-20-T.csv')

model = AggressionModel(N_fan = 330, N_hool = 220, N_pol = 25, N_riopol = 25, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('330-220-25-25-T.csv')

model = AggressionModel(N_fan = 330, N_hool = 220, N_pol = 40, N_riopol = 10, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('330-220-40-10-T.csv')

model = AggressionModel(N_fan = 275, N_hool = 275, N_pol = 30, N_riopol = 20, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('275-275-30-20-T.csv')

model = AggressionModel(N_fan = 275, N_hool = 275, N_pol = 25, N_riopol = 25, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('225-225-25-25-T.csv')

model = AggressionModel(N_fan = 275, N_hool = 275, N_pol = 40, N_riopol = 10, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('275-275-40-10-T.csv')

model = AggressionModel(N_fan = 440, N_hool = 110, N_pol = 30, N_riopol = 20, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('440-110-30-20-T.csv')

model = AggressionModel(N_fan = 440, N_hool = 110, N_pol = 25, N_riopol = 25, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('440-110-25-25-T.csv')

model = AggressionModel(N_fan = 440, N_hool = 110, N_pol = 40, N_riopol = 10, twogroup_switch = True)
for i in range(5400):
    model.step()
data = model.datacollector.get_model_vars_dataframe()
data.to_csv('440-110-40-10-T.csv')