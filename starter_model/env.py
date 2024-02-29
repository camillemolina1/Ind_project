from mesa.space import SingleGrid


class Environment(SingleGrid):
    def __init__(self, width, height):
        super().__init__(width, height, torus=False)
    #     self.actions = {
    #         0: self.move_south,
    #         1: self.move_north,
    #         2: self.move_east,
    #         3: self.move_west,
    #         4: self.eat,
    #     }
    #
    # def get_obs(self):
    #     return [0, 0, 0]
    #
    # def get_actions(self):
    #     return self.actions
    #
    # def step(self, action):
    #     return 0

    def remove_agent(self, agent):
        super().remove_agent(agent)

