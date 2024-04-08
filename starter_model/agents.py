import random
import mesa
import policies as p
import variables as v
import helper_functions as h
from model import TradingMarket, Plant


# ---------------------------- Here are different agents based on functionality ----------------------------------- #


# A basic Agent that always moves randomly. If it is next to an apple it will eat it
class BasicAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hunger = 0
        self.grid = model.grid

    def step(self):
        plant = self.check_if_near(Plant, Plant)
        if plant and plant.size > 0:
            if self.hunger > 0:
                self.eat(plant)
        else:
            self.move()
            self.hunger += 0.1

    def eat(self, plant):
        plant.take()
        self.hunger -= 1

    def move(self):
        new_position = p.random_policy(self)
        self.grid.move_agent(self, new_position)

    def check_if_near(self, obj, size):
        # check if obj nearby
        neighborhood = self.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        neighbors = self.grid.get_cell_list_contents(neighborhood)
        for neighbour in neighbors:
            if isinstance(neighbour, obj):
                if isinstance(obj, Plant):
                    if obj.size == size:
                        return neighbour
                else:
                    return neighbour

    def check_if_near_agents(self, obj):
        agents = []
        # check if agent nearby
        neighborhood = self.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        neighbors = self.grid.get_cell_list_contents(neighborhood)
        for neighbour in neighbors:
            if isinstance(neighbour, obj):
                agents.append(neighbour)
        return agents

    def check_if_empty(self, pos):
        contents = self.grid.get_cell_list_contents(pos)
        if len(contents) == 0:
            return True
        else:
            if len(contents) == 1:
                c = contents[0]
                if isinstance(c, Plant) and c.size == v.SOIL:
                    return True
        return False


# This agent once it has found an apple will stay near if it still not fully eaten
class StayCloseAgent(BasicAgent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        new_position = p.stay_close_policy(self)
        self.grid.move_agent(self, new_position)


# This agent knows where the apples are and goes strait to them
class OmniscientAgent(BasicAgent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        new_position = p.omniscient_policy(self)
        self.grid.move_agent(self, new_position)

    def step(self):
        plant = self.check_if_near(Plant, v.PLANT)
        if plant and plant.size > 0 and self.hunger > 0:
            self.eat(plant)
        self.move()
        self.hunger += 0.1


# this agent can collect food, give it away, trade it for seeds to grow more plants and push agents
class TradingAgent(OmniscientAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hunger = 0
        self.hunger_limit = 0
        self.has = v.SOIL
        self.path = []

    def move(self):
        new_position = p.simple_trading_policy(self)
        self.grid.move_agent(self, new_position)
        self.path = self.path.remove(new_position)

    # take food from soil
    def take_food(self, plant):
        plant.take()
        self.has = v.BABY_PLANT

    # eat stored food
    def eat_stored(self):
        if self.has > v.NOTHING:
            self.has = v.NOTHING
            self.hunger -= 1

    # give food to an agent
    def give(self, agent):
        if self.has > v.NOTHING and agent.has == v.NOTHING:
            self.has -= 1
            agent.has += 1

    # trade food for seeds
    def trade(self):
        self.has = v.SEEDS

    # use seeds to plant more plants
    def plant(self, pos):
        contents = self.grid.get_cell_list_contents(pos)
        soil = contents[0]
        soil.plant()
        self.has = v.NOTHING

    # push agent away (from food)
    def push(self, agent):
        position = agent.pos
        new_position = p.random_policy(agent)
        self.grid.move_agent(agent, new_position)
        self.hunger -= 0.5
        self.grid.move_agent(self, position)

    def step(self):
        plant = self.check_if_near(Plant, v.PLANT)
        soil = self.check_if_near(Plant, v.SOIL)
        market = self.check_if_near(TradingMarket, 0)

        if plant and v.SOIL < plant.size < v.SEEDS:
            if self.hunger > self.hunger_limit:
                self.eat(plant)
                return
            elif self.has == v.SOIL:
                self.take_food(plant)
                return
        if soil and self.has == v.SEEDS:
            if self.check_if_empty(soil.pos):
                self.plant(soil.pos)
                soil.contains = v.PLANT
                return
        # agent trades apple for seeds
        if market and self.has == v.PLANT:
            self.trade()
            return
        self.move()
        self.hunger += 0.1


# ------------------------------------ Here are our 5 types of agents ------------------------------------------ #
# -------------------------------------- based on social orientation ------------------------------------------- #

# Agent prioritises helping others (for now everyone but later on greenbeards or kin) so will bring the hungriest food
class AltruisticAgent(TradingAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hunger_limit = 3

    def move(self):
        new_position = p.simple_trading_policy(self)
        self.grid.move_agent(self, new_position)

    def step(self):
        plant = self.check_if_near(Plant, v.PLANT)
        soil = self.check_if_near(Plant, v.SOIL)
        market = self.check_if_near(TradingMarket, 0)
        agents = self.check_if_near_agents(TradingAgent)

        if self.has == v.PLANT and self.hunger > self.hunger_limit:
            self.eat_stored()
            return
        for a in agents:
            if self.has == v.PLANT and a.hunger > self.hunger:
                self.give(a)
                return
        if plant and v.SOIL < plant.size < v.SEEDS:
            if self.has == v.NOTHING:
                self.take_food(plant)
                return
        if soil and self.has == v.SEEDS:
            if self.check_if_empty(soil.pos):
                self.plant(soil.pos)
                soil.contains = v.PLANT
                return
        # agent trades apple for seeds
        if market and self.has == v.PLANT:
            self.trade()
            return
        self.move()
        self.hunger += 0.1


# Agent will prioritise itself, so it will eat when hungry, but it will also help others when it is full
class CooperativeAgent(TradingAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hunger_limit = 1.5

    def move(self):
        new_position = p.simple_trading_policy(self)
        self.grid.move_agent(self, new_position)

    def step(self):
        plant = self.check_if_near(Plant, v.PLANT)
        soil = self.check_if_near(Plant, v.SOIL)
        market = self.check_if_near(TradingMarket, 0)

        if plant and v.SOIL < plant.size < v.SEEDS:
            if self.has == v.NOTHING:
                self.take_food(plant)
                return
            elif self.hunger > self.hunger_limit:
                self.eat(plant)
                return
        # agent plants seeds
        if soil and self.has == v.SEEDS:
            if self.check_if_empty(soil.pos):
                self.plant(soil.pos)
                soil.contains = v.PLANT
                return
        # agent trades apple for seeds
        if market and self.has == v.PLANT:
            self.trade()
            return
        self.move()
        self.hunger += 0.1


# Agent will prioritise itself, so it will eat all the food while still making sure it has a food source by planting
class SelfishAgent(TradingAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        new_position = p.simple_trading_policy(self)
        self.grid.move_agent(self, new_position)

    def step(self):
        plant = self.check_if_near(Plant, v.PLANT)
        soil = self.check_if_near(Plant, v.SOIL)
        market = self.check_if_near(TradingMarket, 0)

        if self.has == v.PLANT and self.hunger > 3.5:
            self.eat_stored()
            return
        if plant and v.SOIL < plant.size < v.SEEDS:
            if self.hunger > 3.5:
                self.eat(plant)
                return
            else:
                if self.has == v.NOTHING:
                    self.take_food(plant)
                    return
                elif self.hunger > -1:
                    self.eat(plant)
                    return
        # agent plants seeds
        if soil and self.has == v.SEEDS:
            if self.check_if_empty(soil.pos):
                self.plant(soil.pos)
                soil.contains = v.PLANT
                return
        # agent trades apple for seeds
        if market and self.has == v.PLANT:
            self.trade()
            return
        self.move()
        self.hunger += 0.1


# Agent will prioritise itself, so it eats all the food but still leaves some to trade for seeds and can push agents.
class SpitefulAgent(TradingAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        new_position = p.simple_trading_policy(self)
        self.grid.move_agent(self, new_position)

    def step(self):
        plant = self.check_if_near(Plant, v.PLANT)
        soil = self.check_if_near(Plant, v.SOIL)
        market = self.check_if_near(TradingMarket, 0)
        agents = self.check_if_near_agents(TradingAgent)

        if self.has == v.PLANT and self.hunger > 3.5:
            self.eat_stored()
            return
        if plant and v.SOIL < plant.size < v.SEEDS:
            if self.hunger > 3.5:
                self.eat(plant)
                return
            else:
                if self.has == v.NOTHING:
                    self.take_food(plant)
                    return
                elif self.hunger > -1:
                    self.eat(plant)
                    return
        # agent plants seeds
        if soil and self.has == v.SEEDS:
            if self.check_if_empty(soil.pos):
                self.plant(soil.pos)
                soil.contains = v.PLANT
                return
        # agent trades apple for seeds
        if market and self.has == v.PLANT:
            self.trade()
            return
        # is an agent is in the way this agent will push it away
        if agents and self.hunger < 3.5:
            for a in agents:
                if h.is_agent_in_the_way(a):
                    self.push(a)
                    return
        self.move()
        self.hunger += 0.1


# Agent will prioritise hurting the others so will eat all the food and block people from getting any
class SadisticAgent(TradingAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def move(self):
        new_position = p.simple_trading_policy(self)
        self.grid.move_agent(self, new_position)

    def step(self):
        plant = self.check_if_near(Plant, v.PLANT)
        agent = self.check_if_near(TradingAgent, 0)

        if self.has == v.PLANT and self.hunger > 3.5:
            self.eat_stored()
            return
        if plant and v.SOIL < plant.size < v.SEEDS:
            if self.hunger > 3.5:
                self.eat(plant)
                return
            else:
                if self.has == v.NOTHING:
                    self.take_food(plant)
                    return
                elif self.hunger > -1:
                    self.eat(plant)
                    return
        # is an agent is in the way this agent will push it away
        if agent:
            self.push(agent)
            return
        self.move()
        self.hunger += 0.1
