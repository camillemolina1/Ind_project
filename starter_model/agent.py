import mesa

FOOD = 0
AGENT = 1


class Food(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = FOOD
        self.food = 20


class HungryAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = AGENT
        self.food = 0

    def step(self):
        if self.food < 0:
            self.get_food()
        if self.food > -40:
            self.move()
            self.food -= 1

    def get_food(self):
        # check if food nearby & take it
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)
        cellmates = self.model.grid.get_cell_list_contents(neighborhood)
        for c in cellmates:
            if c.type == FOOD and c.food > 0:
                c.food -= 10
                self.food += 10

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=True
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
