from mesa import Agent
import random
import numpy as np

""" 
TODO in general:
 - Update aggression model based on multiple agent types. 
 - Think about how police and riot police handle aggression
  
TODO experiment:
 - Improve visual simulation and think of good ways to plot the data
 - Implement a certain degree of randomness within an agent class so not all agents of that type behave exactly equal.

TODO smaller details:
 - Change variable names for sake of clarity
 - Change class names to match with report (not fans and hooligans)
 - Comment functions so Bart understands what is happening 
 """

class TopAgent(Agent):
    """ Parameters that are true for all agent types at beginning of simulation."""
    def __init__(self, unique_id, model, team):
        super().__init__(unique_id, model)
        self.aggression = 0
        self.timesincescan = 0
        self.model = model
        self.timesincefight = 0
        self.attacks = 0
        self.attacked = 0
        self.scanrange = 5
        self.team = team
        self.fightThreshold = 25
        self.group_larger_threshold = 10
        self.police_interuptions = 0

    def scanArea(self, range):
        """ Returns number of agents within a certain range to scan the area """
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False, radius=range)
        return neighbors

    def numbers(self, neighbors):
        """" Returns array with the numbers of different agent types in the neighborhood (scanarea) of the agent"""
        numbers = np.zeros(3)
        for agent in neighbors:
            if type(agent) is Police or type(agent) is Riot_Police:
                numbers[2] += 1
            if agent.team is not None:
                if (agent.team is self.team):
                    numbers[0] += 1
                if (agent.team is not self.team):
                    numbers[1] += 1
        return numbers

    def get_agent(self, pos):
        """ Returns agent on pos if present"""
        if not self.model.grid.is_cell_empty(pos):
            agents = self.model.grid.get_neighbors(pos, moore=True, include_center=True, radius=0)
            return agents[0]
        else:
            return None

    def get_quadrant(self, i):
        """" returns quadrant for scanrange=5 """
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

    def standard_move(self):
        "Standard Function for moving to random empty cell next to agent, 95% chance"
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

    def check_quadrants(self):
        """Return nd-array with agent types per quadrant"""
        quadrants = np.zeros((4, 3))
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False, radius=5)
        i = 0
        for pos in neighborhood:
            x = self.get_quadrant(i)
            agent = self.get_agent(pos)
            if agent is not None:
                if type(agent) is Police or type(agent) is Riot_Police:
                    quadrants[x,2] += 1
                if agent.team is not None:
                    if agent.team is self.team:
                        quadrants[x,0] += 1
                    elif agent.team is not self.team:
                        quadrants[x,1] += 1
            i += 1
        return quadrants

    def move_quadrant(self, togo):
        """ Move to a certain quadrant (0-3) if space"""
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        if togo == 0:
            if self.model.grid.is_cell_empty(possible_steps[0]):
               self.model.grid.move_agent(self, possible_steps[0])
            elif self.model.grid.is_cell_empty(possible_steps[1]):
                self.model.grid.move_agent(self, possible_steps[1])
        elif togo == 1:
            if self.model.grid.is_cell_empty(possible_steps[2]):
                self.model.grid.move_agent(self, possible_steps[2])
            elif self.model.grid.is_cell_empty(possible_steps[4]):
                self.model.grid.move_agent(self, possible_steps[4])
        elif togo == 2:
            if self.model.grid.is_cell_empty(possible_steps[3]):
                self.model.grid.move_agent(self, possible_steps[3])
            elif self.model.grid.is_cell_empty(possible_steps[5]):
                self.model.grid.move_agent(self, possible_steps[5])
        elif togo == 3:
            if self.model.grid.is_cell_empty(possible_steps[6]):
                self.model.grid.move_agent(self, possible_steps[6])
            elif self.model.grid.is_cell_empty(possible_steps[7]):
                self.model.grid.move_agent(self, possible_steps[7])


    def step(self):
        """ Each time step this function is exectued for all agents"""
        if self.timesincefight == 0:
            if self.timesincescan >= self.scaninterval:
                neighbors = self.scanArea(range=self.scanrange)
                self.update_aggression(neighbors)
                self.move(neighbors)
                self.timesincescan = 0
            else:
                self.standard_move()
                self.timesincescan += 1
        else:
            self.timesincefight -= 1

class Non_Police(TopAgent):
    def __init__(self, unique_id, model, team):
        super().__init__(unique_id, model, team)

    def update_aggression(self, neighbors):
        """ Updates aggression according to number of own and other team"""
        numbers = self.numbers(neighbors)
        if (numbers[0] -  numbers[1]) >= self.group_larger_threshold:
            self.aggression += 1
        elif (numbers[0] - numbers[1]) <= -self.group_larger_threshold:
            if self.aggression > 0:
                self.aggression -= 1

    def move(self, neighbors):
        """ Fight or move according to aggression level"""
        if self.aggression > 15:
            fight = self.check_fight()
            if not fight:
                togo = np.argmax(self.check_quadrants(), axis=0)[1]
                self.move_quadrant(togo)
        else:
            togo = np.argmax(self.check_quadrants(), axis=0)[0]
            self.move_quadrant(togo)

    def check_fight(self):
        """ Check if willing to fight and neighbor is other team"""
        if self.aggression > self.fightThreshold:
            fight = True
            direct_neighbors = self.scanArea(range=1)
            if len(direct_neighbors) > 0:
                for contact in direct_neighbors:
                    if contact.team is not None:
                        if contact.team is not self.team:
                            #print(str(type(contact)) + " AND " + str(type(self)))
                            self.fight(contact)
        else:
            fight = False
        return fight

    def fight(self, other):
        """ Fight """
        self.attacks += 1
        other.attacked += 1
        self.aggression = 0
        other.aggression = 0
        self.timesincefight = 25
        other.timesincefight = 25

class Fan(Non_Police):
    def __init__(self, unique_id, model, team):
        super().__init__(unique_id, model, team)
        self.scaninterval = 8

class Hooligan(Non_Police):
    def __init__(self, unique_id, model, team):
        super().__init__(unique_id, model, team)
        self.scaninterval = 4

class Yes_Police(TopAgent):
    def __init__(self, unique_id, model, team):
        super().__init__(unique_id, model, team)
        self.police_aggression = 2

    def update_aggression(self, neighbors):
        """ Own aggression always 0, breaks up fights"""
        self.aggresssion = 0
        direct_neighbors = self.scanArea(range=1)
        if len(direct_neighbors) > 0:
            for contact in direct_neighbors:
                if contact.timesincefight != 0:
                    contact.timesincefight = 0
                    contact.aggression = 10
                    neighbors = self.scanArea(self.scanrange)
                    for neighbor in neighbors:
                        neighbor.aggression += self.police_aggression
                    self.police_interuptions += 1


    def move(self, neighbors):
        """ Will move to fight if one is seen, otherwise will group or move randomly"""
        fight = self.see_fight(neighbors)
        if fight:
            self.move_to_most_fights()
        else:
            numbers = self.numbers(neighbors)
            if np.argmax(numbers) != 2: # Police group not largest
                # Check quadrant to go to
                togo = np.argmax(self.check_quadrants(), axis=0)[2]
                self.move_quadrant(togo)
            else:
                self.standard_move()

    def see_fight(self, neighbors):
        """ Checks surroundings for fights"""
        for contact in neighbors:
            if contact.timesincefight != 0:
                return True
        return False

    def move_to_most_fights(self):
        """ Move to quadrant with most fights """
        quadrants = np.zeros(4)
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False, radius=5)
        i = 0
        for pos in neighborhood:
            x = self.get_quadrant(i)
            agent = self.get_agent(pos)
            if agent is not None:
                if agent.timesincefight != 0:
                    quadrants[x] += 1
            i += 1
        togo = np.argmax(quadrants)
        self.move_quadrant(togo)

class Police(Yes_Police):
    def __init__(self, unique_id, model, team):
        super().__init__(unique_id, model, team)
        self.scaninterval = 4

class Riot_Police(Yes_Police):
    def __init__(self, unique_id, model, team):
        super().__init__(unique_id, model, team)
        self.scaninterval = 2


