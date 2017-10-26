from model import *
import matplotlib.pyplot as plt

# Single run

model = AggressionModel(N_fan = 225, N_hool = 225, N_pol = 40, N_riopol = 10, twogroup_switch = False, group_a_proportion=0.25, riot_police_grouped=False, size_riot_police_groups=5, width=100, height=100)
for i in range(5400):
    model.step()

data = model.datacollector.get_model_vars_dataframe()
data.to_csv('test.csv')
data.plot()
plt.show()