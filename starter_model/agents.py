import mesa
from policies import stay_close_policy, omniscient_policy, random_policy, simple_trading_policy, let_seeds_grow_policy
from plant import Plant
from place import TradingMarket
import variables as v


# A basic Agent that always moves randomly. If it is next to an apple it will eat it
class BasicAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hunger = 0

    def step(self):
        plant = self.check_if_near(Plant, Plant)
        if plant and plant.size > 0:
            if self.hunger > 0:
                self.eat(plant)
        else:
            self.move()
            self.hunger += 0.1

    def check_if_near(self, obj, size):
        # check if food nearby
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        neighbors = self.model.grid.get_cell_list_contents(neighborhood)
        for neighbour in neighbors:
            if isinstance(neighbour, obj):
                if isinstance(obj, Plant):
                    if obj.size == size:
                        return neighbour
                else:
                    return neighbour

    def eat(self, plant):
        plant.size -= 1
        self.hunger -= 1

    def move(self):
        new_position = random_policy(self)
        self.model.grid.move_agent(self, new_position)


# This agent once it has found an apple will stay near if it still not fully eaten
class StayCloseAgent(BasicAgent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hunger = 0

    def move(self):
        new_position = stay_close_policy(self)
        self.model.grid.move_agent(self, new_position)


# This agent knows where the apples are and goes strait to them
class OmnicientAgent(BasicAgent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hunger = 0

    def move(self):
        new_position = omniscient_policy(self)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        plant = self.check_if_near(Plant, v.PLANT)
        if plant and plant.size > 0 and self.hunger > 0:
            self.eat(plant)
        self.move()
        self.hunger += 0.1


class IntelligentAgent(OmnicientAgent):
    def __init__(self, unique_id, plant_size, plant_params, model):
        super().__init__(unique_id, model)
        self.hunger = 0
        self.hunger_limit = 0
        self.has = v.SOIL
        self.plant_size = plant_size
        self.plant_params = plant_params

    def move(self):
        new_position = simple_trading_policy(self)
        self.model.grid.move_agent(self, new_position)

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

    def take_food(self, plant):
        plant.size -= 1
        self.has = v.BABY_PLANT

    def trade(self):
        self.has = v.SEEDS

    def plant(self, pos):
        contents = self.model.grid.get_cell_list_contents(pos)
        soil = contents[0]
        soil.plant()
        self.has = v.NOTHING

    def check_if_empty(self, pos):
        contents = self.model.grid.get_cell_list_contents(pos)
        if len(contents) == 0:
            return True
        else:
            if len(contents) == 1:
                c = contents[0]
                if isinstance(c, Plant) and c.size == v.SOIL:
                    return True
        return False


class IntelligentAgent2(IntelligentAgent):
    def __init__(self, unique_id, plant_size, plant_params, model):
        super().__init__(unique_id, plant_size, plant_params, model)
        self.hunger = 0
        self.has = v.SOIL
        self.plant_size = plant_size
        self.plant_params = plant_params
        self.hunger_limit = 1.5

    def move(self):
        new_position = let_seeds_grow_policy(self)
        self.model.grid.move_agent(self, new_position)

