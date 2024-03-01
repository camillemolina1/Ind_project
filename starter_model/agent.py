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
        new_position = self.choose_good_move()
        self.model.grid.move_agent(self, new_position)

    def choose_good_move(self):
        valid_moves = self.find_all_valid_moves()
        for m in valid_moves:
            neighbourhood = self.model.grid.get_neighborhood(
                m, moore=True, include_center=True
            )
            for n in neighbourhood:
                distant_neighbours = self.model.grid.get_cell_list_contents(n)
                for distant_neighbour in distant_neighbours:
                    if isinstance(distant_neighbour, Food) and distant_neighbour.supply > 0:
                        return m

        return self.random.choice(valid_moves)

    def find_all_valid_moves(self):
        moves = []
        possible_moves = self.model.grid.get_neighborhood(
            self.pos, moore=False, include_center=True
        )
        for p in possible_moves:
            if self.check_if_valid_move(p):
                moves.append(p)
        return moves

    def check_if_valid_move(self, move):
        neighbours = self.model.grid.get_cell_list_contents(move)
        if len(neighbours) != 0:
            return False
        else:
            return True

