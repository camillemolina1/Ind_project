import mesa


class Food(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.food = 20


class HungryAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
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
            if isinstance(c, Food) and c.food > 0:
                c.food -= 10
                if c.food < -40:
                    self.model.grid.remove_agent(c)
                    self.model.schedule.remove(c)
                self.food += 10

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=True
        )
        new_position = self.random.choice(possible_steps)
        neighbour = self.model.grid.get_cell_list_contents(new_position)
        while len(neighbour) != 0:
            new_position = self.random.choice(possible_steps)
            neighbour = self.model.grid.get_cell_list_contents(new_position)
        print(new_position, neighbour, len(neighbour))
        self.model.grid.move_agent(self, new_position)
