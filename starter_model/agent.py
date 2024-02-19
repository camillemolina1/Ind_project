import mesa


FOOD = 0
AGENT = 1


class Food(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = FOOD
        self.food = 2


class MoneyAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = AGENT
        self.food = 0

    def step(self):
        self.move()
        if self.food == 0:
            self.take_food()

    def take_food(self):
        neighborhood = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        cellmates = self.model.grid.get_cell_list_contents(neighborhood)
        for c in cellmates:
            if c.food > 0:
                c.food -= 1
                self.food += 1

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
