from agents import BasicAgent, StayCloseAgent, OmnicientAgent
from food import Food
from env import Environment
import mesa

EATEN_APPLE = 0
HALF_EATEN_APPLE = 10
APPLE = 20


class MyModel(mesa.Model):
    """A model with some number of agents."""
    def __init__(self, N, F, width, height):
        super().__init__()
        self.num_agents = N
        self.amount_of_food = F

        self.grid = Environment(width, height)
        self.schedule = mesa.time.RandomActivation(self)
        self._steps: int = 0
        self._time = 0  # the model's clock
        self.running = True

        food_locations = []
        for j in range(self.num_agents, self.amount_of_food + self.num_agents):
            x, y = self.find_valid_location()
            b = Food(j, (x, y), self)
            self.schedule.add(b)
            # Add the agent to a random grid cell
            self.grid.place_agent(b, (x, y))
            food_locations.append((x, y))
        print("food locations:", food_locations)

        # Create agents
        for i in range(self.num_agents):
            a = OmnicientAgent(i, food_locations, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x, y = self.find_valid_location()
            self.grid.place_agent(a, (x, y))

    def step(self):
        # self.datacollector.collect(self)
        self.schedule.step()
        self.check_for_dead()

    def check_for_dead(self):
        for agent in self.schedule.agents:
            if isinstance(agent, BasicAgent) and agent.hunger >= 40:
                self.schedule.remove(agent)

    def find_valid_location(self):
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        while len(self.grid.get_cell_list_contents((x, y))) != 0:
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
        return x, y

