import mesa


class TradingMarket(mesa.Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos


class Wall(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)