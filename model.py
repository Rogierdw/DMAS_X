from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from TopAgent import *

def compute_aggression(model):
    agent_aggression = [agent.aggression for agent in model.schedule.agents]
    total_aggression = sum(agent_aggression)
    return total_aggression

def compute_fights(model):
    agent_fights = [agent.fights for agent in model.schedule.agents]
    total_fights = sum(agent_fights)
    return total_fights

class AggressionModel(Model):
    """A model simulating aggression and the onset of riots in crowd behavior."""
    def __init__(self, N_fan, N_hool, N_pol, N_riopol, width, height, twogroup_switch):
        self.running = True # enables conditional shut off of the model (is now set True indefinitely)
        self.num_agents = N_fan + N_hool + N_pol + N_riopol
        self.grid = SingleGrid(width, height, True) # Boolean is for wrap-around, SingleGrid enforces one agent/cell
        self.schedule = RandomActivation(self) # Means agent activation ordering is random

        if twogroup_switch:
            # Create agents
            half_fan = N_fan / 2
            half_hool = N_hool / 2
            for i in range(self.num_agents):
                if i < half_fan:
                    a = Fan(i, self, True) # True and False are the party
                elif i < (2*half_fan):
                    a = Fan(i, self, False)
                elif i < (2*half_fan) + half_hool:
                    a = Hooligan(i, self, True)
                elif i < (2 * half_fan) + (2 * half_hool):
                    a = Hooligan(i, self, False)
                elif i < N_fan + N_hool + N_pol:
                    a = Police(i, self, None)
                else:
                    a = Riot_Police(i, self, None)
                self.schedule.add(a)

                x = 1
                y = 1
                placed = False
                while not placed:
                    if (x, y) in self.grid.empties:
                        self.grid.place_agent(a, (x, y))
                        placed = True
                    else:
                        x = random.randrange(self.grid.width)
                        y = random.randrange(self.grid.height)
        else:
            for i in range(self.num_agents):
                if i < N_fan:
                    a = Fan(i, self, True)
                elif i < N_fan+N_hool:
                    a = Hooligan(i, self, True)
                elif i < N_fan+N_hool+N_pol:
                    a = Police(i, self, False)
                else:
                    a = Riot_Police(i, self, False)
                self.schedule.add(a)

                x = 1
                y = 1
                placed = False
                while not placed:
                    if (x,y) in self.grid.empties:
                        self.grid.place_agent(a, (x, y))
                        placed = True
                    else:
                        x = random.randrange(self.grid.width)
                        y = random.randrange(self.grid.height)


        self.datacollector = DataCollector(
            model_reporters={"Riot": compute_aggression},
            agent_reporters={"Aggression": lambda a: a.aggression})

    def step(self):
        '''Advance the model by one step.'''
        self.datacollector.collect(self)
        self.schedule.step()

