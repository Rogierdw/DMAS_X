from mesa import Agent
import random
import numpy as np

""" 
TODO in general:
 - Update aggression model based on multiple agent types. 
 - Hooligans only fight normal fans now. We should fix this, so either two parties or none. Stop confusing the parties 
 from the paper of Jager et al with our different agent classes. 
 - Declare all parameters globally so we can easily tune them during testing
 - Think about how police and riot police handle aggression
 - Fix the quadrant functions
  
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
        self.fights = 0
        self.scanrange = 5
        self.team = team
        self.agg_thres = 10

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
        if not self.model.grid.is_cell_empty(pos):
            agents = self.model.grid.get_neighbors(pos, moore=True, include_center=True, radius=0)
            return agents[0]
        else:
            return None

    def get_quadrant(self, i):
        """" TODO: Make this less static so we can still tune the scan range of the agents. """
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
        quadrants = np.zeros((4, 3))
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False, radius=5)
        i = 0
        for pos in neighborhood:
            x = self.get_quadrant(i)
            agent = self.get_agent(pos)
            if agent is not None:
                if type(agent) is Police or type(agent) is Riot_Police:
                    quadrants[x,2] += 1
                if agent.team is self.team:
                    quadrants[x,0] += 1
                elif agent.team is not self.team:
                    quadrants[x,1] += 1
            i += 1
        return quadrants

        """
        quadrants = np.zeros((4, 4))
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False, radius=5)
        i = 0
        for pos in neighborhood:
            x = self.get_quadrant(i)
            agent = self.get_agent(pos)
            if agent is not None:
                if type(agent) is Fan:
                    quadrants[x, 0] += 1
                elif type(agent) is Hooligan:
                    quadrants[x, 1] += 1
                elif type(agent) is Police:
                    quadrants[x, 2] += 1
                elif type(agent) is Riot_Police:
                    quadrants[x, 3] += 1
            i += 1
        return quadrants
        """

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
        self.timesincefight = 25
        other.timesincefight = 25

    def step(self):
        if self.timesincefight == 0:
            if self.timesincescan >= self.scanfreq:
                neighbors = self.scanArea(range=self.scanrange)
                self.timesincescan == 0

                self.update_aggression(neighbors)
                self.move(neighbors)
            else:
                self.standard_move()
                self.timesincescan += 1
        else:
            self.timesincefight -= 1



class Fan(TopAgent):
    def __init__(self, unique_id, model, team):
        super().__init__(unique_id, model, team)
        self.scanfreq = 20

    def update_aggression(self, neighbors):
        numbers = self.numbers(neighbors)
        if (numbers[0] -  numbers[1]) >= self.agg_thres:
            self.aggression += 1
        elif (numbers[1] - numbers[0]) <= -self.agg_thres:
            self.aggression -= 1

    def move(self, neighbors):
        numbers = self.numbers(neighbors)
        if self.aggression > 15:
            fight = self.check_fight()
            if not fight:
                # check presence of other groups
                others = np.delete(self.check_quadrants(), 0, 1)
                others = others.astype('float')
                others[others==0] = np.nan
                x = np.where(others==np.nanmin(others))
                try:
                    pos = x[0][0],x[0][1]# IF there are any nonzero-values of neighbours, move to the first lowest one
                    self.move_quadrant(pos)
                except IndexError:
                    self.standard_move()# If there are no other-group members around, move randomly

                #togo = np.argmin(self.check_quadrants(), axis=0)[0]
        else:
            if np.argmax(numbers) != 0: # Own group not largest
                # Check quadrant to go to (own group)
                togo = np.argmax(self.check_quadrants(), axis=0)[0]
                self.move_quadrant(togo)
            else:
                self.standard_move()

class Hooligan(TopAgent):
    def __init__(self, unique_id, model, team):
        super().__init__(unique_id, model, team)
        self.scanfreq = 3

    def update_aggression(self, neighbors):
        numbers = self.numbers(neighbors)
        if (numbers[0] -  numbers[1]) >= self.agg_thres:
            self.aggression += 1
        elif (numbers[1] - numbers[0]) <= -self.agg_thres:
            self.aggression -= 1

    def move(self, neighbors = None):
        numbers = self.numbers(neighbors)
        if self.aggression > 15:
            fight = self.check_fight()
            if not fight:
                # check presence of other groups
                others = np.delete(self.check_quadrants(), 1, 1)
                others = others.astype('float')
                others[others == 0] = np.nan
                x = np.where(others == np.nanmin(others))
                try:
                    pos = x[0][0],x[0][1]# IF there are any nonzero-values of other groups in scanarea, move to the first lowest one
                    self.move_quadrant(pos)
                except IndexError:
                    self.standard_move()# If there are no other-group members around, move randomly
        else:
            if np.argmax(numbers) != 0: # Own group not largest
                # Check quadrant to go to
                togo = np.argmax(self.check_quadrants(), axis=0)[1]
                self.move_quadrant(togo)
            else:
                self.standard_move()


class Police(TopAgent):
    def __init__(self, unique_id, model, team):
        super().__init__(unique_id, model, team)
        self.scanfreq = 20

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
    def __init__(self, unique_id, model, team):
        super().__init__(unique_id, model, team)
        self.scanfreq = 3


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
