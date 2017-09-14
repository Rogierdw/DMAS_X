from mesa import Agent, Model
from mesa.time import RandomActivation
import random
from mesa.space import MultiGrid, SingleGrid
from mesa.datacollection import DataCollector

class FootballAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.aggression = 1

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,             # Moore includes diagonal neighbors. Von Neumann only up/down/left/right
            include_center=False)   # Center cell does or does not count as neighbor
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def give_aggression(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = random.choice(cellmates)
            other.aggression += 1
            self.aggression -= 1

    def step(self):
        self.move()
        if self.aggression > 0:
            self.give_aggression()

def compute_gini(model):
    agent_aggressions = [agent.aggression for agent in model.schedule.agents]
    x = sorted(agent_aggressions)
    N = model.num_agents
    B = sum( xi * (N-i) for i,xi in enumerate(x) ) / (N*sum(x))
    return (1 + (1/N) - 2*B)

class AggressionModel(Model):
    """A model simulating aggression and the onset of riots in crowd behavior."""
    def __init__(self, N, width, height):
        self.running = True # enables conditional shut off of the model (is now set True indefinitely)
        self.num_agents = N
        self.grid = MultiGrid(width, height, True) # Boolean is for wrap-around, SingleGrid would enforce one agent/cell
        self.schedule = RandomActivation(self) # Means agent activation ordering is random

        # Create agents
        for i in range(self.num_agents):
            a = FootballAgent(i, self)
            self.schedule.add(a)


            # Add the agent to a random grid cell
            x = random.randrange(self.grid.width)
            y = random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

            '''
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
            '''

        self.datacollector = DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Aggression": lambda a: a.aggression})

    def step(self):
        '''Advance the model by one step.'''
        self.datacollector.collect(self)
        self.schedule.step()

