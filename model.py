from mesa import Agent, Model
from mesa.time import RandomActivation
import random
from mesa.space import MultiGrid, SingleGrid
from mesa.datacollection import DataCollector
#from FootballAgent import FootballAgent
from TopAgent import *

def compute_aggression(model):
    agent_aggression = [agent.agent_aggression for agent in model.schedule.agents]
    total_aggression = sum(agent_aggression)
    return total_aggression

def compute_fights(model):
    agent_fights = [agent.fights for agent in model.schedule.agents]
    total_fights = sum(agent_fights)
    return total_fights

class AggressionModel(Model):
    """A model simulating aggression and the onset of riots in crowd behavior."""
    def __init__(self, N_fan, N_hool, N_pol, N_riopol, width, height):
        self.running = True # enables conditional shut off of the model (is now set True indefinitely)
        self.num_agents = N_fan + N_hool + N_pol + N_riopol
        self.grid = SingleGrid(width, height, False) # Boolean is for wrap-around, SingleGrid would enforce one agent/cell
        self.schedule = RandomActivation(self) # Means agent activation ordering is random

        # Create agents
        for i in range(self.num_agents):
            if i < N_fan:
                a = Fan(i, self)
            elif i < N_fan+N_hool:
                a = Hooligan(i, self)
            elif i < N_fan+N_hool+N_pol:
                a = Police(i, self)
            else:
                a = Riot_Police(i, self)
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

