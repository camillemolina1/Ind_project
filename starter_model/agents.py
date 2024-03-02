import mesa
from policies import stay_close_policy, omnicient_policy
from food import Food

EATEN_APPLE = 0
HALF_EATEN_APPLE = 10
APPLE = 20


# A basic Agent that cannot move. It simply knows if it is next to an apple to go next to it and eat it
class BasicAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hunger = 0

    def step(self):
        apple = self.check_if_near_food()
        if apple and apple.supply > 0:
            if self.hunger > 0:
                self.eat(apple)
        else:
            self.move()
            self.hunger += 1

    def check_if_near_food(self):
        # check if food nearby
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        neighbors = self.model.grid.get_cell_list_contents(neighborhood)
        for neighbour in neighbors:
            if isinstance(neighbour, Food):
                return neighbour

    def eat(self, apple):
        apple.supply -= 10
        self.hunger -= 20

    def move(self):
        self.model.grid.move_agent(self, self.pos)


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
    def __init__(self, unique_id, food_locations, model):
        super().__init__(unique_id, model)
        self.hunger = 0
        self.food = []
        for loc_x, loc_y in food_locations:
            self.food.append([APPLE, loc_x, loc_y])

    def move(self):
        new_position = omnicient_policy(self)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        apple = self.check_if_near_food()
        if apple:
            self.update_food(apple)
            if apple.supply > 0 and self.hunger > 0:
                self.eat(apple)
                self.update_food(apple)
            else:
                self.move()
                self.hunger += 1
        else:
            self.move()
            self.hunger += 1

    def update_food(self, apple):
        for food in self.food:
            if food[1] == apple.pos[0] and food[2] == apple.pos[1]:
                food[0] = apple.supply
