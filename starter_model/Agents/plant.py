import mesa
from Helpers import variables as v


class Plant(mesa.Agent):
    def __init__(self, unique_id, pos, size, plant_params, model):
        super().__init__(unique_id, model)
        self.pos = pos
        self.size = size
        self.max_size = plant_params[0]
        self.growth_time = plant_params[1]
        self.time = 0
        # self.age = 0

    def step(self):
        if self.growth_time > 0:
            # if v.SOIL < self.size < v.SEEDS:
                # if self.age > 5:
                #     self.size = v.SOIL
                # else:
                #     self.age += 0.1
            if v.SOIL < self.size < self.max_size:
                if self.time > self.growth_time:
                    self.size += 1
                    self.time = 0
                else:
                    self.time += 1
            elif self.size == v.SEEDS:
                # self.age = 0
                if self.time > self.growth_time:
                    self.size = v.BABY_PLANT
                    self.time = 0
                else:
                    self.time += 1
        return

    def plant(self):
        if self.size == v.SOIL:
            if self.growth_time > 0:
                self.size = v.SEEDS
            else:
                self.size = self.max_size
        return

    def take(self):
        self.size -= 1
        self.time = 0


