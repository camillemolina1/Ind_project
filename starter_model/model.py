from mesa import DataCollector

from agents import BasicAgent, StayCloseAgent, OmnicientAgent, IntelligentAgent
from plant import Plant
from env import Environment
from place import TradingMarket, Soil
import mesa


class MyModel(mesa.Model):
    """A model with some number of agents."""
    def __init__(self, N, F, S, width, height):
        super().__init__()
        self.num_agents = N
        self.amount_of_food = F
        self.food_supply = S
        self.soil = [(width - 3, height - 4), (height - 1, width - 1), (width - 3, height - 9), (height - 6, width - 1)]

        self.grid = Environment(width, height)
        self.schedule = mesa.time.RandomActivation(self)
        self._steps: int = 0
        self._time = 0  # the model's clock
        self.running = True

        self.count_chart = DataCollector(
            {
                "Agent_count": lambda l: self.count(BasicAgent),
                "Food_count": lambda l: self.count(Plant),
            }
        )
        self.hunger_levels = DataCollector(
            {
                "Agent 1": lambda l: self.get_hunger(0),
                "Agent 2": lambda l: self.get_hunger(1),
                "Agent 3": lambda l: self.get_hunger(2),
                "Agent 4": lambda l: self.get_hunger(3),
                "Agent 5": lambda l: self.get_hunger(4),
            }
        )

        # create soil
        for h in range(2):
            for n in range(self.soil[h*2][1], self.soil[h*2+1][0]):
                for m in range(self.soil[h*2][0], self.soil[h*2+1][1]):
                    s = Soil(self.next_id(), (m, n), 0, self)
                    # Add the agent to a random grid cell
                    self.grid.place_agent(s, (m, n))
                    self.schedule.add(s)

        # place food
        for j in range(self.num_agents, self.amount_of_food + self.num_agents):
            x, y = self.find_valid_food_location()
            b = Plant(j, (x, y), self.food_supply, self)
            self.schedule.add(b)
            # Add the agent to a random grid cell
            self.grid.place_agent(b, (x, y))

        # Create agents
        for i in range(self.num_agents):
            a = IntelligentAgent(i, self.food_supply, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x, y = self.find_valid_agent_location()
            self.grid.place_agent(a, (x, y))

        # place trading markets
        g = TradingMarket(1000, (0, 1), self)
        self.grid.place_agent(g, (0, 1))
        g = TradingMarket(1001, (0, width - 2), self)
        self.grid.place_agent(g, (0, width - 2))
        self.schedule.add(g)

    def step(self):
        self.hunger_levels.collect(self)
        self.count_chart.collect(self)
        self.schedule.step()
        self.check_for_dead()

    def check_for_dead(self):
        for agent in self.schedule.agents:
            if isinstance(agent, BasicAgent) and agent.hunger >= 4:
                self.schedule.remove(agent)
                self.grid.remove_agent(agent)
            if isinstance(agent, Plant) and agent.supply == 0:
                self.schedule.remove(agent)
                self.grid.remove_agent(agent)

    def count(self, obj):
        count = 0
        for agent in self.schedule.agents:
            if isinstance(agent, obj):
                if isinstance(agent, Plant):
                    count += agent.supply
                else:
                    count += 1
        return count

    def find_valid_agent_location(self):
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        while len(self.grid.get_cell_list_contents((x, y))) != 0:
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
        return x, y

    def find_valid_food_location(self):
        i = self.random.randrange(0, 2)
        x = self.random.randrange(self.soil[i*2][0], self.soil[i*2+1][1])
        y = self.random.randrange(self.soil[i*2][1], self.soil[i*2+1][0])
        while len(self.grid.get_cell_list_contents((x, y))) > 1:
            i = self.random.randrange(0, 2)
            x = self.random.randrange(self.soil[i*2][0], self.soil[i*2+1][1])
            y = self.random.randrange(self.soil[i*2][1], self.soil[i*2+1][0])
        return x, y

    def get_hunger(self, agent_id):
        for agent in self.schedule.agents:
            if agent.unique_id == agent_id and isinstance(agent, BasicAgent):
                return agent.hunger



