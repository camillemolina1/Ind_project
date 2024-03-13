from agents import BasicAgent, StayCloseAgent, OmnicientAgent, IntelligentAgent
from food import Food
from env import Environment
from place import Goal, Soil
import mesa


class MyModel(mesa.Model):
    """A model with some number of agents."""
    def __init__(self, N, F, width, height):
        super().__init__()
        self.num_agents = N
        self.amount_of_food = F
        self.soil = [(width - 2, 0), (width, height)]

        self.grid = Environment(width, height)
        self.schedule = mesa.time.RandomActivation(self)
        self._steps: int = 0
        self._time = 0  # the model's clock
        self.running = True

        # place "goals"
        g = Goal(1000, (0, 1), self)
        self.grid.place_agent(g, (0, 1))
        self.schedule.add(g)
        g = Goal(1001, (0, width - 2), self)
        self.grid.place_agent(g, (0, width - 2))
        self.schedule.add(g)

        for n in range(self.soil[0][1], self.soil[1][0]):
            for m in range(self.soil[0][0], self.soil[1][1]):
                s = Soil(self.next_id(), (m, n), self)
                self.schedule.add(s)
                # Add the agent to a random grid cell
                self.grid.place_agent(s, (m, n))

        # place food
        for j in range(self.num_agents, self.amount_of_food + self.num_agents):
            x, y = self.find_valid_food_location()
            b = Food(j, (x, y), self)
            self.schedule.add(b)
            # Add the agent to a random grid cell
            self.grid.place_agent(b, (x, y))

        # Create agents
        for i in range(self.num_agents):
            a = IntelligentAgent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x, y = self.find_valid_agent_location()
            self.grid.place_agent(a, (x, y))

    def step(self):
        # self.datacollector.collect(self)
        self.schedule.step()
        self.check_for_dead()

    def check_for_dead(self):
        for agent in self.schedule.agents:
            if isinstance(agent, BasicAgent) and agent.hunger >= 4:
                self.schedule.remove(agent)
                self.grid.remove_agent(agent)
            if isinstance(agent, Food) and agent.supply == 0:
                self.schedule.remove(agent)
                self.grid.remove_agent(agent)

    def find_valid_agent_location(self):
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        while len(self.grid.get_cell_list_contents((x, y))) != 0:
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
        return x, y

    def find_valid_food_location(self):
        x = self.random.randrange(self.soil[0][0], self.soil[1][0])
        y = self.random.randrange(self.soil[0][1], self.soil[1][1])
        while len(self.grid.get_cell_list_contents((x, y))) > 1:
            x = self.random.randrange(self.soil[0][0], self.soil[1][0])
            y = self.random.randrange(self.soil[0][1], self.soil[1][1])
        return x, y

