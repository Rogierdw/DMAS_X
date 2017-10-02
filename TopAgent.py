from mesa import Agent
import random

class TopAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)




     
    def scanArea(self,range):
        """ Returns number of agents within a certain range to scan the area """
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=range)
        #print(len(neighbors))

        return len(neighbors)
        


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

    def step(self):
        self.move()
        self.handle_aggression()
        self.scanArea(5)

    def handle_aggression(self):
        raise NotImplementedError("Should be handled by subclass")

class Fan(TopAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.aggression = 15
        self.role = 'Fan'
        self.model = model

    def handle_aggression(self):
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False
        )

        for other in neighbors:
            if other.role == 'Fan':
                pass

            elif other.role == 'Hooligan':
                if self.aggression < 50:
                    other.aggression -= 1
                    self.aggression += 1

            elif other.role == 'Police':
                if self.aggression > 50:
                    self.aggression += 1
                else:
                    self.aggression -= 2

            elif other.role == 'Riot Police':
                if self.aggression > 50:
                    self.aggression += 2
                else:
                    self.aggression += 1

        '''
        if len(neighbors)>0: ## HERE THE ACTUAL AGGRESSION RULES COME IN!
            other = random.choice(neighbors)
            if other.aggression > 0:
                other.aggression += 1
            if self.aggression > 0:
                self.aggression -= 1
        '''

class Hooligan(TopAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.aggression = 35
        self.role = 'Hooligan'
        self.model = model

    def handle_aggression(self):
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False
        )

        for other in neighbors:
            if other.role == 'Fan':
                if self.aggression > 50:
                    other.aggression += 2
                    self.aggression += 1
                else:
                    other.aggression += 1

            elif other.role == 'Hooligan':
                if self.aggression > 50:
                    other.aggression += 2
                else:
                    other.aggression += 1

            elif other.role == 'Police':
                if self.aggression > 50:
                    self.aggression -= 1
                else:
                    self.aggression -= 3

            elif other.role == 'Riot Police':
                if self.aggression > 50:
                    self.aggression += 2
                else:
                    self.aggression += 1

class Police(TopAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.aggression = 0
        self.role = 'Police'
        self.model = model

    def handle_aggression(self):
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False
        )

        for other in neighbors:
            if other.role == 'Fan':
                if other.aggression > 50:
                    other.aggression -= 1
                else:
                    other.aggression += 1

            elif other.role == 'Hooligan':
                if other.aggression > 50:
                    other.aggression -= 2
                else:
                    other.aggression -= 1

class Riot_Police(TopAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.aggression = 0
        self.role = 'Riot Police'
        self.model = model

    def handle_aggression(self):
        neighbors = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False
        )

        for other in neighbors:
            if other.role == 'Fan':
                if other.aggression > 50:
                    other.aggression -= 2
                else:
                    other.aggression -= 1

            elif other.role == 'Hooligan':
                if other.aggression > 50:
                    other.aggression -= 3
                else:
                    other.aggression -= 1