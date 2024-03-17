import mesa


class Plant(mesa.Agent):
    def __init__(self, unique_id, pos, supply, model):
        super().__init__(unique_id, model)
        self.supply = supply
        self.pos = pos

    def step(self):
        return



