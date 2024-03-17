import mesa
from policies import stay_close_policy, omniscient_policy, random_policy, trading_policy
from food import Food
from place import Goal, Soil

NOTHING = 0
APPLE = 1
SEEDS = 2


# A basic Agent that always moves randomly. If it is next to an apple it will eat it
class BasicAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hunger = 0

    def step(self):
        apple = self.check_if_near(Food)
        if apple and apple.supply > 0:
            if self.hunger > 0:
                self.eat(apple)
        else:
            self.move()
            self.hunger += 0.1

    def check_if_near(self, obj):
        # check if food nearby
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        neighbors = self.model.grid.get_cell_list_contents(neighborhood)
        for neighbour in neighbors:
            if isinstance(neighbour, obj):
                return neighbour

    def eat(self, apple):
        apple.supply -= 1
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
        apple = self.check_if_near(Food)
        if apple and apple.supply > 0 and self.hunger > 0:
            self.eat(apple)
        self.move()
        self.hunger += 0.1


class IntelligentAgent(OmnicientAgent):
    def __init__(self, unique_id, supply, model):
        super().__init__(unique_id, model)
        self.hunger = 0
        self.has = NOTHING
        self.food_supply = supply

    def move(self):
        new_position = trading_policy(self)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        apple = self.check_if_near(Food)
        if apple and apple.supply > 0:
            if self.hunger > 0:
                self.eat(apple)
                return
            elif self.has == NOTHING:
                self.take_apple(apple)
                return
        soil = self.check_if_near(Soil)
        if soil and self.has == SEEDS:
            if self.check_if_empty(soil.pos):
                self.plant(soil.pos)
                return
        goal = self.check_if_near(Goal)
        # agent trades apple for seeds
        if goal and self.has == APPLE:
            self.trade()
            return
        self.move()
        self.hunger += 0.1

    def take_apple(self, apple):
        apple.supply -= 1
        self.has = APPLE

    def trade(self):
        self.has = SEEDS

    def plant(self, pos):
        b = Food(self.model.next_id(), pos, self.food_supply, self.model)
        self.model.schedule.add(b)
        # Add the agent to a random grid cell
        self.model.grid.place_agent(b, pos)
        self.has = NOTHING

    def check_if_empty(self, pos):
        contents = self.model.grid.get_cell_list_contents(pos)
        if len(contents) == 0:
            return True
        else:
            if len(contents) == 1 and isinstance(contents[0], Soil):
                return True
        return False
