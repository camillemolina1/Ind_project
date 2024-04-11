import random
import mesa
import policies as p
import variables as v
import helper_functions as h
from model import TradingMarket, Plant


# A basic Agent that always moves randomly. If it is next to an apple it will eat it
class BasicAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hunger = 0
        self.grid = model.grid
        self.has = v.NOTHING

    def move(self):
        new_position = p.random_policy(self)
        self.grid.move_agent(self, new_position)

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

    # take food from soil
    def take_food(self, plant):
        plant.take()
        self.has = v.BABY_PLANT
        self.hunger += 0.1

    # eat stored food
    def eat_stored(self):
        if self.has > v.NOTHING:
            self.has = v.NOTHING
            self.hunger -= 1

    # give food to an agent
    def give(self, agent):
        self.has -= 1
        agent.has += 1
        self.hunger += 0.1

    # trade food for seeds
    def trade(self):
        self.has = v.SEEDS
        self.hunger += 0.1

    # use seeds to plant more plants
    def plant(self, pos):
        contents = self.grid.get_cell_list_contents(pos)
        soil = contents[0]
        soil.plant()
        self.has = v.NOTHING
        self.hunger += 0.1

    # push agent away (from food)
    def push(self, agent):
        position = agent.pos
        new_position = p.random_policy(agent)
        self.grid.move_agent(agent, new_position)
        self.hunger += 0.5
        self.grid.move_agent(self, position)

    def wait(self):
        self.hunger += 0.1

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


# These agents act based on their social value orientation
class TradingAgent(BasicAgent):
    def __init__(self, unique_id, model, svo):
        super().__init__(unique_id, model)
        self.svo = svo
        if svo == v.ALTRUISTIC:
            self.hunger_limit = 3
        else:
            self.hunger_limit = 1.5
        self.hunger = 0
        self.has = v.SOIL

    def move(self):
        if self.svo == v.ALTRUISTIC:
            new_position = p.altruistic_policy(self)
        elif self.svo == v.COOPERATIVE:
            new_position = p.let_seeds_grow_policy(self)
        elif self.svo == v.SELFISH:
            new_position = p.simple_trading_policy(self)
        elif self.svo == v.COMPETITIVE:
            new_position = p.competitive_policy(self)
        else:
            new_position = p.sadistic_policy(self)
        self.grid.move_agent(self, new_position)

    def altruistic_step(self, plant, soil, market, agents):
        if self.has == v.PLANT and self.hunger > self.hunger_limit:
            self.eat_stored()
            return
        for a in agents:
            if self.has == v.PLANT and a.hunger > 2.5:
                if self.has > v.NOTHING and a.has == v.NOTHING:
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

    def cooperative_step(self, plant, soil, market):
        if self.has == v.PLANT and self.hunger > 3.5:
            self.eat_stored()
            return
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

    def selfish_step(self, plant, soil, market):
        if self.has == v.PLANT and self.hunger > 3:
            self.eat_stored()
            return
        if plant and v.SOIL < plant.size < v.SEEDS:
            if self.hunger > 3.5:
                self.eat(plant)
                return
            elif plant.size == v.BABY_PLANT or self.hunger < -1:
                self.wait()
                return
            elif plant.size > v.BABY_PLANT:
                if self.has == v.NOTHING:
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

    def competitive_step(self, plant, soil, market, agents):
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

    def sadistic_step(self, plant, agent):
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

    def step(self):
        plant = self.check_if_near(Plant, v.PLANT)
        soil = self.check_if_near(Plant, v.SOIL)
        market = self.check_if_near(TradingMarket, 0)
        agents = self.check_if_near_agents(TradingAgent)

        if self.svo == v.ALTRUISTIC:
            self.altruistic_step(plant, soil, market, agents)
        elif self.svo == v.COOPERATIVE:
            self.cooperative_step(plant, soil, market)
        elif self.svo == v.SELFISH:
            self.selfish_step(plant, soil, market)
        elif self.svo == v.COMPETITIVE:
            self.competitive_step(plant, soil, market, agents)
        else:
            self.sadistic_step(plant, agents)
