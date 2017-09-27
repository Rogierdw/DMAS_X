from mesa import Agent
import random


class FootballAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.aggression = 1

    def move(self):
        "Function for moving to empty cell next to agent"

        moved = False
        tries = 0
        tried = []

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,             # Moore includes diagonal neighbors. Von Neumann only up/down/left/right
            include_center=False)   # Center cell does or does not count as neighbor

        while not moved and tries <= 8:
            new_position = random.choice(possible_steps)
            if new_position not in tried:
                tried += new_position
                if self.model.grid.is_cell_empty(new_position):
                    moved = True
                    self.model.grid.move_agent(self, new_position)
                else:
                    tries += 1

        #new_position = random.choice(possible_steps)
        #self.model.grid.move_agent(self, new_position)

    def give_aggression(self):

        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False
        )

        if len(neighbors)>0:
            other = random.choice(neighbors)
            other.aggression += 1
            self.aggression -= 1

        '''
        neighborhood = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,  # Moore includes diagonal neighbors. Von Neumann only up/down/left/right
            include_center=False)  # Center cell does or does not count as neighbor
        
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = random.choice(cellmates)
            other.aggression += 1
            self.aggression -= 1
        '''

    def step(self):
        self.move()
        if self.aggression > 0:
            self.give_aggression()