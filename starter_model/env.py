from mesa.space import SingleGrid


class Environment(SingleGrid):
    def __init__(self, width, height):
        super().__init__(width, height, torus=False)





