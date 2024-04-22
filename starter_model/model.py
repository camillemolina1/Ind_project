from mesa import DataCollector
from mesa.space import SingleGrid

from Agents.plant import Plant
from Agents.market import TradingMarket
from Agents.agents import TradingAgent
from Helpers import variables as v
import mesa


class MyModel(mesa.Model):
    def __init__(self, altruistic_agents, cooperative_agents, selfish_agents, competitive_agents, sadistic_agents,
                 plants, width, height):
        super().__init__()
        self.num_agents = [altruistic_agents, cooperative_agents, selfish_agents, competitive_agents, sadistic_agents]
        self.amount_of_food = plants
        self.plant_params = [v.SIZE, v.GROWTH_TIME]
        self.soil = [(width - 3, height - 4), (height - 1, width - 1), (width - 3, height - 9), (height - 6, width - 1)]

        self.grid = SingleGrid(width, height, torus=False)
        self.schedule = mesa.time.RandomActivation(self)
        self._steps: int = 0
        self._time = 0  # the model's clock
        self.running = True
        self.moves = []

        tot_agents = self.num_agents[0] + self.num_agents[1] + self.num_agents[2] + self.num_agents[3] + self.num_agents[4]
        # place plants
        for j in range(tot_agents, tot_agents + self.amount_of_food):
            x, y = self.find_valid_plant_location()
            b = Plant(j, (x, y), self.plant_params[0], self.plant_params, self)
            self.schedule.add(b)
            self.grid.place_agent(b, (x, y))

        # create soil
        for h in range(2):
            for n in range(self.soil[h * 2][1], self.soil[h * 2 + 1][0]):
                for m in range(self.soil[h * 2][0], self.soil[h * 2 + 1][1]):
                    if len(self.grid.get_cell_list_contents((m, n))) == 0:
                        s = Plant(self.next_id(), (m, n), v.SOIL, self.plant_params, self)
                        self.grid.place_agent(s, (m, n))
                        self.schedule.add(s)

        # place trading markets
        g = TradingMarket(self.next_id(), (0, 1), self)
        self.grid.place_agent(g, (0, 1))
        self.schedule.add(g)
        g = TradingMarket(self.next_id(), (0, width - 2), self)
        self.grid.place_agent(g, (0, width - 2))
        self.schedule.add(g)

        # Create agents
        for i in range(self.num_agents[0]):
            ag = TradingAgent(i, self, v.ALTRUISTIC)
            self.add_agent(ag)
        t = self.num_agents[0]
        for i in range(self.num_agents[1]):
            ag = TradingAgent(t + i, self, v.COOPERATIVE)
            self.add_agent(ag)
        t += self.num_agents[1]
        for i in range(self.num_agents[2]):
            ag = TradingAgent(t + i, self, v.SELFISH)
            self.add_agent(ag)
        t += self.num_agents[2]
        for i in range(self.num_agents[3]):
            ag = TradingAgent(t + i, self, v.COMPETITIVE)
            self.add_agent(ag)
        t += self.num_agents[3]
        for i in range(self.num_agents[4]):
            ag = TradingAgent(t + i, self, v.SADISTIC)
            self.add_agent(ag)

        self.agent_count_chart = DataCollector(
            {
                "Agent_count": lambda l: self.count(TradingAgent),
            }
        )
        self.food_count_chart = DataCollector(
            {
                "Food_count": lambda l: self.count(Plant),
            }
        )
        self.datacollector = DataCollector(
            {
                "Agent 1": lambda l: self.get_hunger(0),
                "Agent 2": lambda l: self.get_hunger(1),
                "Agent 3": lambda l: self.get_hunger(2),
                "Agent 4": lambda l: self.get_hunger(3),
                "Agent 5": lambda l: self.get_hunger(4),
            }
        )
        self.agent_activity = DataCollector(
            {
                "Eat": lambda l: self.get_moves("eat"),
                "Eat Stored": lambda l: self.get_moves("eat_stored"),
                "Take": lambda l: self.get_moves("take"),
                "Trade": lambda l: self.get_moves("trade"),
                "Plant": lambda l: self.get_moves("plant"),
                "Give": lambda l: self.get_moves("give"),
                "Push": lambda l: self.get_moves("push"),
            }
        )
        self.agent_activity2 = DataCollector(
            {
                "Move": lambda l: self.get_moves("move"),
                "Wait": lambda l: self.get_moves("wait"),
             }
        )

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
        self.check_for_dead()
        self.agent_count_chart.collect(self)
        self.food_count_chart.collect(self)
        self.agent_activity.collect(self)
        self.agent_activity2.collect(self)

    def check_for_dead(self):
        for agent in self.schedule.agents:
            if isinstance(agent, TradingAgent) and agent.hunger > 4:
                self.schedule.remove(agent)
                self.grid.remove_agent(agent)
                self.agents.remove(agent)

    def add_agent(self, agent):
        self.schedule.add(agent)
        x, y = self.find_valid_agent_location()
        self.grid.place_agent(agent, (x, y))

    def count(self, obj):
        count = 0
        for agent in self.schedule.agents:
            if isinstance(agent, obj):
                if isinstance(agent, Plant):
                    if v.SEEDS > agent.size > v.SOIL:
                        count += agent.size
                else:
                    count += 1
        return count

    def get_hunger(self, agent_id):
        for agent in self.schedule.agents:
            if agent.unique_id == agent_id and isinstance(agent, TradingAgent):
                return agent.hunger

    def get_moves(self, move):
        for agent in self.schedule.agents:
            if isinstance(agent, TradingAgent) and agent.last_move == move:
                self.moves.append(move)
            if isinstance(agent, TradingAgent) and move == "move" and (agent.last_move == "move - market" or
                                                                       agent.last_move == "move - agents" or
                                                                       agent.last_move == "move - plants" or
                                                                       agent.last_move == "move - soil"):
                self.moves.append(move)
        return self.moves.count(move)

    def find_valid_agent_location(self):
        x = self.random.randrange(self.grid.width)
        y = self.random.randrange(self.grid.height)
        while len(self.grid.get_cell_list_contents((x, y))) != 0:
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
        return x, y

    def find_valid_plant_location(self):
        i = self.random.randrange(0, 2)
        x = self.random.randrange(self.soil[i*2][0], self.soil[i*2+1][1])
        y = self.random.randrange(self.soil[i*2][1], self.soil[i*2+1][0])
        while len(self.grid.get_cell_list_contents((x, y))) > 0:
            i = self.random.randrange(0, 2)
            x = self.random.randrange(self.soil[i*2][0], self.soil[i*2+1][1])
            y = self.random.randrange(self.soil[i*2][1], self.soil[i*2+1][0])
        return x, y



