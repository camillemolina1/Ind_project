import mesa


FOOD = 0
AGENT = 1


class Food(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = FOOD


class MoneyAgent(mesa.Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.type = AGENT
        self.wealth = 1

    def step(self):
        self.move()
        if self.wealth > 0:
            self.give_money()

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other_agent = self.random.choice(cellmates)
            other_agent.wealth += 1
            self.wealth -= 1

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
