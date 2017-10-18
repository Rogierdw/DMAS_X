from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from TopAgent import *

def mean_aggression(model):
    agent_aggression = [agent.aggression for agent in model.schedule.agents]
    mean_aggression = sum(agent_aggression)/len(model.schedule.agents)
    return mean_aggression

def compute_fights(model):
    agent_fights = [agent.attacked for agent in model.schedule.agents]
    total_fights = sum(agent_fights)
    return total_fights

class AggressionModel(Model):
    """A model simulating aggression and the onset of riots in crowd behavior."""
    def __init__(self, N_fan, N_hool, N_pol, N_riopol, width, height, twogroup_switch):
        self.running = True # enables conditional shut off of the model (is now set True indefinitely)
        self.num_agents = N_fan + N_hool + N_pol + N_riopol
        self.grid = SingleGrid(width, height, True) # Boolean is for wrap-around, SingleGrid enforces one agent/cell
        self.schedule = RandomActivation(self) # Means agent activation ordering is random
        self.size_riot_groups = 5  # Initial size of riot police groups

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
                self.place_agent(a)
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
                self.place_agent(a)

        self.datacollector = DataCollector(
            model_reporters={"Riot": mean_aggression ,
                             "Fights": compute_fights},
            agent_reporters={"Aggression": lambda a: a.aggression})

    def step(self):
        '''Advance the model by one step.'''
        self.datacollector.collect(self)
        self.schedule.step()

    def place_agent(self,a):
        x = 1
        y = 1
        placed = False

        # For riot police, place different
        if(type(a)==Riot_Police):
            x,y = self.place_grouped(a)
            self.grid.place_agent(a,(x,y))
        else:
            # if not riot, place random
            while not placed:
                if (x,y) in self.grid.empties:
                    self.grid.place_agent(a, (x, y))
                    placed = True
                else:
                    x = random.randrange(self.grid.width)
                    y = random.randrange(self.grid.height)

    def findagents(self):
        # Finds agents (length of array) with corresponding position and return this
        locations=[]
        for row in range(self.grid.width):
            for col in range(self.grid.height):
                if self.grid[row][col] is not None:
                   locations.append((row,col,type(self.grid[row][col])))
        return locations

    def place_grouped(self,a):
        # Places the agent in a group with other agents, if none are available or no spots available place on a random spot, so random distribution of group size as model property
        temp_placed=False
        x=1
        y=1

        # The random position if an agent cant find an ungrouped riot police agent, possibilities to place better distributed
        while not temp_placed:
            if(x,y) in self.grid.empties:
                temp_placed = True
                finalpos = (x,y)
            else:
                x = random.randrange(self.grid.width)
                y = random.randrange(self.grid.height)

        # If there is an agent of Riot police with less than size members in his range, then return empty x,y in neighborhood-space. Else pick random x,y
        foundgroup = False
        agents = self.findagents()
        for agent in agents:   # all the agents in the grid
            if(agent[2]==Riot_Police):      # 3rd position represents type
                if(foundgroup):
                    break
                pos = (agent[0],agent[1])  # Row/Col combined
                neighbors = self.grid.get_neighbors(pos,moore=True,include_center=False,radius=1)
                count = 0

                for neighbor in neighbors:
                    if(type(neighbor) is Riot_Police):
                        count += 1
                    
                if(count<self.size_riot_groups):
                    # BETTER DEFINITION OF A GROUP
                    # Found riot_police agent which is not fully 'grouped', now find empty pos around the found agent
                    empty=False
                    area = self.grid.get_neighborhood(pos,moore=True,include_center=False,radius=1)
                        
                    for position in area:
                        if(self.grid.is_cell_empty(position)):   # else the agent keeps the random position (unlikely with radius=2)
                            finalpos=position
                            found = True
                            break
        # pos of new agent
        return finalpos


