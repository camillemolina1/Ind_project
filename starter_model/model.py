from agent import HungryAgent, Food
from env import Environment
import mesa


class MyModel(mesa.Model):
    """A model with some number of agents."""
    def __init__(self, N, F, width, height):
        self.num_agents = N
        self.amount_of_food = F

        self.grid = Environment(width, height)
        self.schedule = mesa.time.RandomActivation(self)
        self._steps: int = 0
        self._time = 0  # the model's clock
        self.running = True

        # Create agents
        for i in range(self.num_agents):
            a = HungryAgent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        for j in range(self.num_agents, self.amount_of_food + self.num_agents):
            b = Food(j, self)
            # self.schedule.add(b)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(b, (x, y))

    def step(self):
        # self.datacollector.collect(self)
        self.schedule.step()

    # def reset(self):
    #     # self.datacollector.collect(self)
    #     self.state = self.start
