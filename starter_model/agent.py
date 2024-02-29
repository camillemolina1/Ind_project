import mesa


class Food(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.supply = 20


class HungryAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hunger = 0

    def step(self):
        if self.hunger > 0:
            self.eat()
        if self.hunger < 40:
            self.move()
            self.hunger += 1

    def eat(self):
        # check if food nearby & take it
        neighborhood = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)
        neighbor = self.model.grid.get_cell_list_contents(neighborhood)
        for n in neighbor:
            if isinstance(n, Food) and n.supply > 0:
                n.supply -= 10
                self.hunger -= 20

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=True
        )
        new_position = self.choose_move(possible_steps)
        neighbour = self.model.grid.get_cell_list_contents(new_position)
        while len(neighbour) != 0:
            new_position = self.random.choice(possible_steps)
            neighbour = self.model.grid.get_cell_list_contents(new_position)
        self.model.grid.move_agent(self, new_position)

    def choose_move(self, possible_steps):
        # Find viable random step
        best_move = self.random.choice(possible_steps)
        neighbour = self.model.grid.get_cell_list_contents(best_move)
        while len(neighbour) != 0:
            best_move = self.random.choice(possible_steps)
            neighbour = self.model.grid.get_cell_list_contents(best_move)

        # If close to apple to towards it
        for p in possible_steps:
            neighbour = self.model.grid.get_cell_list_contents(p)
            if len(neighbour) == 0:
                neighbourhood = self.model.grid.get_neighborhood(p, moore=True, include_center=True)
                for n in self.model.grid.get_cell_list_contents(neighbourhood):
                    if isinstance(n, Food) and n.supply > 0:
                        best_move = p
        return best_move


