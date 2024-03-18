import mesa
import variables as v


class Plant(mesa.Agent):
    def __init__(self, unique_id, pos, size, max_size, growth, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.size = size
        self.max_size = max_size
        self.growth = growth
        self.time = 0

    def step(self):
        if self.growth:
            if v.SOIL < self.size < self.max_size:
                if self.time > 2:
                    self.size += 1
                    self.time = 0
                else:
                    self.time += 1
            elif self.size == v.SEEDS:
                if self.time > 2:
                    self.size = v.BABY_PLANT
                    self.time = 0
                else:
                    self.time += 1
        return

    def plant(self):
        if self.size == v.SOIL:
            self.size = v.SEEDS
        return



