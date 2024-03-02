import mesa
from policies import stay_close_policy
from food import Food


# A basic Agent that cannot move. It simply knows if it is next to an apple to go next to it and eat it
class BasicAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hunger = 0

    def step(self):
        apple = self.check_if_near_food()
        if apple and self.hunger > 0:
            apple.supply -= 10
            self.hunger -= 20
        else:
            self.move()
            self.hunger += 1

    def check_if_near_food(self):
        # check if food nearby
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        neighbors = self.model.grid.get_cell_list_contents(neighborhood)
        for neighbour in neighbors:
            if isinstance(neighbour, Food) and neighbour.supply > 0:
                return neighbour

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
