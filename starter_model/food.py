import mesa


class Food(mesa.Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.supply = 20
        self.pos = pos

    def step(self):
        return


