from mesa import Agent
import random
import numpy as np


class TopAgent(Agent):
    """ An agent with fixed initial wealth."""
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.aggression = 0
        self.lastscan = 0
        self.model = model
        self.walkable = 0
        self.fights = 0

    def scanArea(self, range=5):
        """ Returns number of agents within a certain range to scan the area """
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=range)
        return neighbors

    def numbers(self, neighbors):
        numbers = np.zeros(4)
        for agent in neighbors:
            if (type(agent) is Fan):
                numbers[0] += 1
            if (type(agent) is Hooligan):
                numbers[1] += 1
            if (type(agent) is Police):
                numbers[2] += 1
            if (type(agent) is Riot_Police):
                numbers[3] += 1
        return numbers

    def get_agent(self, pos):
        if not self.model.grid.is_cell_empty(pos):
            agents = self.model.grid.get_neighbors(pos, moore=True, include_center=True, radius=0)
            return agents[0]
        else:
            return None

    def get_quadrant(self, i):
        zero = [0,1,2,3,4,8,9,10,11,12,17,18,19,20,21,26,27,27,28,29,30]
        one = [5,6,7,13,14,15,16,22,23,24,25,31,32,33,34,40,41,42,43,44]
        two = [35,36,37,38,39,45,46,47,48,54,55,56,57,63,64,65,66,72,73,74]
        three = [49,50,51,52,53,58,59,60,61,62,67,68,69,70,71,75,76,77,78,79]
        if i in zero:
            return 0
        elif i in one:
            return 1
        elif i in two:
            return 2
        elif i in three:
            return 3

    def check_quadrants(self):
        quadrants = np.zeros((4, 4))
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False, radius=5)
        i = 0
        for pos in neighborhood:
            x = self.get_quadrant(i)
            agent = self.get_agent(pos)
            if agent is not None:
                if type(agent) is Fan:
                    quadrants[x,0] += 1
                elif type(agent) is Hooligan:
                    quadrants[x,1] += 1
                elif type(agent) is Police:
                    quadrants[x,2] += 1
                elif type(agent) is Riot_Police:
                    quadrants[x,3] += 1
            i += 1
        return quadrants

    def standard_move(self):
        "Standard Function for moving to empty cell next to agent"
        if random.random() < 0.95:  # 95% chance to randomly move
            moved = False
            tries = 0
            tried = []

            possible_steps = self.model.grid.get_neighborhood(
                self.pos,
                moore=True,  # Moore includes diagonal neighbors. Von Neumann only up/down/left/right
                include_center=False)  # Center cell does or does not count as neighbor

            while not moved and tries <= 8:
                new_position = random.choice(possible_steps)
                if new_position not in tried:
                    tried += new_position
                    if self.model.grid.is_cell_empty(new_position):
                        moved = True
                        self.model.grid.move_agent(self, new_position)
                    else:
                        tries += 1
        else:  # 5% chance to stand still
            pass

    def move_quadrant(self, togo):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        if togo is 0:
            if self.model.grid.is_cell_empty(possible_steps[0]):
                self.model.grid.move_agent(possible_steps[0])
            elif self.model.grid.is_cell_empty(possible_steps[1]):
                self.model.grid.move_agent(possible_steps[1])
        elif togo is 1:
            if self.model.grid.is_cell_empty(possible_steps[2]):
                self.model.grid.move_agent(possible_steps[2])
            elif self.model.grid.is_cell_empty(possible_steps[4]):
                self.model.grid.move_agent(possible_steps[4])
        elif togo is 2:
            if self.model.grid.is_cell_empty(possible_steps[3]):
                self.model.grid.move_agent(possible_steps[3])
            elif self.model.grid.is_cell_empty(possible_steps[5]):
                self.model.grid.move_agent(possible_steps[5])
        elif togo is 3:
            if self.model.grid.is_cell_empty(possible_steps[6]):
                self.model.grid.move_agent(possible_steps[6])
            elif self.model.grid.is_cell_empty(possible_steps[7]):
                self.model.grid.move_agent(possible_steps[7])

    def check_fight(self):
        if self.aggression > 25:
            fight = True
            direct_neighbors = self.scanArea(range=1)
            if len(direct_neighbors) > 0:
                for contact in direct_neighbors:
                    if type(contact) is not type(self):
                        #print(str(type(contact)) + " AND " + str(type(self)))
                        self.fight(contact)
        else:
            fight = False
        return fight

    def fight(self, other):
        self.fights += .5
        other.fights += .5
        self.aggression = 0
        other.aggression = 0
        self.walkable = 25
        other.walkable = 25

    def step(self):
        if self.walkable == 0:
            if self.lastscan >= self.scanfreq:
                neighbors = self.scanArea()
                self.lastscan == 0

                self.update_aggression(neighbors)
                self.move(neighbors)
            else:
                self.standard_move()
                self.lastscan += 1
        else:
            self.walkable -= 1

    def update_aggression(self, neighbors):
        raise NotImplementedError("Should be handled by subclass")


class Fan(TopAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.aggression = 0
        self.lastscan = 0
        self.model = model
        self.scanfreq = 20

    def update_aggression(self, neighbors):
        numbers = self.numbers(neighbors)
        if np.argmax(numbers)==0:
            self.aggression += 1
        else:
            if self.aggression > 0:
                self.aggression -= 1

    def move(self, neighbors):
        numbers = self.numbers(neighbors)
        if self.aggression > 15:
            fight = self.check_fight()
            if not fight:
                # move to other group. which one? So move to place where least of own group are
                togo = np.argmin(self.check_quadrants(), axis=0)[0]
                self.move_quadrant(togo)
        else:
            if np.argmax(numbers) != 0: # Own group not largest
                # Check quadrant to go to (own group)
                togo = np.argmax(self.check_quadrants(), axis=0)[0]
                self.move_quadrant(togo)
            else:
                self.standard_move()


class Hooligan(TopAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.aggression = 0
        self.model = model
        self.scanfreq = 3
        self.lastscan = 0

    def update_aggression(self, neighbors = None):
        if neighbors is None:
            self.move()
        numbers = self.numbers(neighbors)
        if np.argmax(numbers)==1:
            self.aggression += 1
        else:
            if self.aggression > 0:
                self.aggression -= 1

    def move(self, neighbors = None):
        numbers = self.numbers(neighbors)
        if self.aggression > 15:
            fight = self.check_fight()
            if not fight:
                # move to other group. which one? So move to place where least of own group are
                togo = np.argmin(self.check_quadrants(), axis=0)[1]
                self.move_quadrant(togo)
        else:
            if np.argmax(numbers) != 0: # Own group not largest
                # Check quadrant to go to
                togo = np.argmax(self.check_quadrants(), axis=0)[1]
                self.move_quadrant(togo)
            else:
                self.standard_move()


class Police(TopAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.aggression = 0
        self.model = model
        self.scanfreq = 20
        self.lastscan = 0

    def update_aggression(self, neighbors):
        pass

    def move(self, neighbors = None):
        numbers = self.numbers(neighbors)
        if np.argmax(numbers) != 0: # Own group not largest
            # Check quadrant to go to
            togo = np.argmax(self.check_quadrants(), axis=0)[2]
            self.move_quadrant(togo)
        else:
            self.standard_move()


class Riot_Police(TopAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.aggression = 0
        self.model = model
        self.scanfreq = 3
        self.lastscan = 0


    def update_aggression(self, neighbors):
        pass

    def move(self, neighbors = None):
        numbers = self.numbers(neighbors)
        if np.argmax(numbers) != 0: # Own group not largest
            # Check quadrant to go to
            togo = np.argmax(self.check_quadrants(), axis=0)[3]
            self.move_quadrant(togo)
        else:
            self.standard_move()
