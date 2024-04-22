import mesa
from Helpers import variables as v, helper_functions as h
from model import TradingMarket, Plant


# A basic Agent that always moves randomly. If it is next to an apple it will eat it
class BasicAgent(mesa.Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.hunger = 0
        self.grid = model.grid
        self.has = v.NOTHING

    def move(self):
        new_position = h.get_random_move(self)
        self.grid.move_agent(self, new_position)

    def step(self):
        plant = self.check_if_near(Plant, Plant)
        if plant and plant.size > 0:
            if self.hunger > 0:
                self.eat(plant)
        else:
            self.move()
            self.hunger += 0.1

    def eat(self, plant):
        plant.take()
        self.hunger -= 1

    # take food from soil
    def take_food(self, plant):
        plant.take()
        self.has = v.BABY_PLANT
        self.hunger += 0.1

    # eat stored food
    def eat_stored(self):
        if self.has > v.NOTHING:
            self.has = v.NOTHING
            self.hunger -= 1

    # give food to an agent
    def give(self, agent):
        self.has -= 1
        agent.has += 1
        agent.eat_stored()
        self.hunger += 0.1

    # trade food for seeds
    def trade(self):
        self.has = v.SEEDS
        self.hunger += 0.1

    # use seeds to plant more plants
    def plant(self, soil):
        soil.plant()
        self.has = v.NOTHING
        self.hunger += 0.1

    # push agent away (from food)
    def push(self, agent):
        position = agent.pos
        new_position = h.get_random_move(agent)
        if new_position == position:
            self_pos = self.pos
            valid_moves = h.find_all_valid_moves(self)
            if valid_moves:
                new_pos = agent.random.choice(valid_moves)
                self.grid.move_agent(self, new_pos)
                self.grid.move_agent(agent, self_pos)
            else:
                return
        else:
            self.grid.move_agent(agent, new_position)
        self.hunger += 0.5
        self.grid.move_agent(self, position)

    def wait(self):
        self.hunger += 0.1

    def check_if_near(self, obj, size):
        # check if obj nearby
        neighborhood = self.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        neighbors = self.grid.get_cell_list_contents(neighborhood)
        for neighbour in neighbors:
            if isinstance(neighbour, obj):
                if obj == Plant:
                    if size == v.PLANT and (v.SOIL < neighbour.size < v.SEEDS):
                        return neighbour
                    if size == v.SOIL and neighbour.size == v.SOIL:
                        return neighbour
                else:
                    return neighbour

    def check_if_near_agents(self, obj):
        agents = []
        # check if agent nearby
        neighborhood = self.grid.get_neighborhood(self.pos, moore=False, include_center=False)
        neighbors = self.grid.get_cell_list_contents(neighborhood)
        for neighbour in neighbors:
            if isinstance(neighbour, obj):
                agents.append(neighbour)
        return agents

    def check_if_empty(self, pos):
        contents = self.grid.get_cell_list_contents(pos)
        if len(contents) == 0:
            return True
        else:
            if len(contents) == 1:
                c = contents[0]
                if isinstance(c, Plant) and c.size == v.SOIL:
                    return True
        return False


# These agents act based on their social value orientation
class TradingAgent(BasicAgent):
    def __init__(self, unique_id, model, svo, svo_changes, prison):
        super().__init__(unique_id, model)
        self.svo = svo
        self.model = model
        self.last_move = "nothing"
        self.hunger = 0
        self.has = v.NOTHING
        self.changing_svo = svo_changes
        self.prison = prison
        self.guesses = [-1, -1, -1, -1, -1]

    def move_towards(self, move):
        if move:
            # print("let's go towards ", move[0])
            pick = move[3]
        else:
            pick = h.get_random_move(self)
        self.grid.move_agent(self, pick)
        self.hunger += 0.1

    def calc_moves(self, next_to_plant, next_to_soil, next_to_market, next_to_agents):
        soil = h.find_thing(self, Plant, v.SOIL)
        plants = h.find_thing(self, Plant, v.PLANT)
        agents = h.find_thing(self, TradingAgent, 0)
        markets = h.find_thing(self, TradingMarket, 0)
        self_hunger = self.hunger / 5

        soil_path, plants_path, agents_path, market_path = (h.find_shortest_path_helper(self, soil),
                                                            h.find_shortest_path_helper(self, plants),
                                                            h.find_shortest_path_helper(self, agents),
                                                            h.find_shortest_path_helper(self, markets))
        moves = []
        if plants_path and plants_path[0] != self.pos and not next_to_plant:
            if self.has == v.PLANT:
                moves = [["move - plants", 1 - (len(plants_path) / 20) + self_hunger, -0.5, plants_path[0]]]
            else:
                moves = [["move - plants", 1 - (len(plants_path) / 20) + self_hunger, 0, plants_path[0]]]
        if self.has == v.PLANT:
            if market_path and market_path[0] != self.pos and not next_to_market:
                moves.append(
                    ["move - market", 1 - (len(market_path) / 20), 1 - (len(market_path) / 20), market_path[0]])
            if agents_path and agents_path[0] != self.pos and not next_to_agents:
                moves.append(["move - agents", - 1 - (len(agents_path) / 20), 1, agents_path[0]])
        else:
            if market_path and market_path[0] != self.pos and not next_to_market:
                moves.append(["move - market", 0 - (len(market_path) / 20), 0, market_path[0]])
            if agents_path and agents_path[0] != self.pos and not next_to_agents:
                moves.append(["move - agents", -0.3 - (len(agents_path) / 20), - 0.5, agents_path[0]])
        if soil_path and soil_path[0] != self.pos and not next_to_soil:
            if self.has == v.SEEDS:
                moves.append(["move - soil", 1 - (len(soil_path) / 20), 0.5 - (len(soil_path) / 20), soil_path[0]])
            else:
                moves.append(["move - soil", 0 - (len(soil_path) / 20), 0 - (len(soil_path) / 20), soil_path[0]])
        return moves

    def find_moves(self, plant, soil, market, agents):
        self_hunger = self.hunger / 5
        collective_hunger = h.others_hunger(self.model.agents, self)
        collective_hunger = (collective_hunger / h.count(self, TradingAgent)) / 5
        nb_of_food_left = h.count(self, Plant) / 5

        moves = self.calc_moves(plant, soil, market, agents)
        # print("self: ", self_hunger, " vs collective: ", collective_hunger)

        if plant:
            take = ["take", 1.5 + self_hunger + nb_of_food_left, nb_of_food_left]
            eat = ["eat", 1 + self_hunger + nb_of_food_left, - 1 - collective_hunger + nb_of_food_left]
            w = 0
            if agents:
                w = -0.5
            wait = ["wait", -0.1, w - collective_hunger]
            if plant.size < v.MEDIUM_PlANT:
                take = ["take", 0 + self_hunger, 0 - collective_hunger]
                eat = ["eat", 0 + self_hunger, -1.5 - collective_hunger]
                wait = ["wait", 1, w - collective_hunger]
            if self.has == v.NOTHING:
                moves.append(take)
            if self.hunger > -4:
                moves.append(eat)
            moves.append(wait)
        if soil and self.has == v.SEEDS:
            moves.append(["plant", 1.5, 0.5])
        if market and self.has == v.PLANT:
            moves.append(["trade", 2 - self_hunger, 0.5 + collective_hunger])
        if agents:
            if self.has == v.PLANT:
                moves.append(["give", -1, 1 + collective_hunger])
            for a in agents:
                if h.is_agent_in_the_way(a):
                    if self_hunger > 0:
                        if collective_hunger > 0:
                            moves.append(["push", -0.5 + (self_hunger * 3), -0.5 - collective_hunger])
                        else:
                            moves.append(["push", -0.5 + (self_hunger * 3), -0.5])
                    else:
                        if collective_hunger > 0:
                            moves.append(["push", -0.5, -0.5 - collective_hunger])
                        else:
                            moves.append(["push", -0.5, -0.5])
        if self.has == v.PLANT and self.hunger > -4:
            moves.append(["eat_stored", 1 + self_hunger, -1 - collective_hunger + nb_of_food_left])
        return moves

    def choose_move(self, moves):
        if self.svo == v.ALTRUISTIC:
            pick = moves[0]
            for move in moves:
                if move[2] > pick[2]:
                    pick = move
                elif move[2] == pick[2]:
                    if move[1] > pick[1]:
                        pick = move
        elif self.svo == v.COOPERATIVE:
            pick = moves[0]
            for move in moves:
                if move[1] + move[2] > pick[1] + pick[2]:
                    pick = move
                elif move[1] + move[2] == pick[1] + pick[2]:
                    if move[1] > pick[1]:
                        pick = move
        elif self.svo == v.SELFISH:
            pick = moves[0]
            for move in moves:
                if move[1] > pick[1]:
                    pick = move
        elif self.svo == v.COMPETITIVE:
            pick = moves[0]
            for move in moves:
                if move[1] - move[2] > pick[1] - pick[2]:
                    pick = move
                elif move[1] - move[2] == pick[1] - pick[2]:
                    if move[1] > pick[1]:
                        pick = move
        else:
            pick = moves[0]
            for move in moves:
                if move[2] < pick[2]:
                    pick = move
                elif move[2] < pick[2]:
                    if move[1] > pick[1]:
                        pick = move
        return pick

    def do_move(self, move, plant, soil, agent):
        self.last_move = move[0]
        if (move[0] == "move - agents" or move[0] == "move - market"
                or move[0] == "move - soil" or move[0] == "move - plants"):
            self.move_towards(move)
        elif move[0] == "eat_stored":
            self.eat_stored()
            # print("eating stored food")
        elif move[0] == "take":
            self.take_food(plant)
            # print("taking")
        elif move[0] == "eat":
            self.eat(plant)
            # print("eating")
        elif move[0] == "wait":
            self.wait()
            # print("waiting")
        elif move[0] == "push":
            self.push(agent[0])
            # print("pushing")
        elif move[0] == "plant":
            self.plant(soil)
            # print("planting")
        elif move[0] == "trade":
            self.trade()
            # print("trading")
        elif move[0] == "give":
            self.give(agent[0])
            # print("giving")

    def analyse_others_moves(self):
        if self.guesses == [-1, -1, -1, -1, -1]:
            for agent in self.model.agents:
                if isinstance(agent, TradingAgent):
                    if not agent.unique_id == self.unique_id:
                        self.guesses[agent.unique_id] = self.svo

        new_guesses = [-1, -1, -1, -1, -1]
        for agent in self.model.schedule.agents:
            if isinstance(agent, TradingAgent) and not agent.unique_id == self.unique_id:
                if agent.last_move == "trade" or agent.last_move == "plant":
                    if self.guesses[agent.unique_id] == v.SELFISH or self.guesses[agent.unique_id] == v.COOPERATIVE:
                        new_guesses[agent.unique_id] = v.COOPERATIVE
                    else:
                        new_guesses[agent.unique_id] = v.SELFISH
                elif agent.last_move == "push":
                    if self.guesses[agent.unique_id] == v.SELFISH or self.guesses[agent.unique_id] == v.COMPETITIVE:
                        new_guesses[agent.unique_id] = self.guesses[agent.unique_id] + 1
                    elif self.guesses[agent.unique_id] == v.SADISTIC:
                        new_guesses[agent.unique_id] = v.SADISTIC
                    else:
                        new_guesses[agent.unique_id] = v.COMPETITIVE
                elif agent.last_move == "give":
                    new_guesses[agent.unique_id] = v.ALTRUISTIC
                else:
                    new_guesses[agent.unique_id] = self.guesses[agent.unique_id]
        self.guesses = new_guesses

    def check_on_agents(self):
        for agent in self.model.schedule.agents:
            if isinstance(agent, TradingAgent) and not agent.unique_id == self.unique_id:
                # if agent is in "jail" and has become good, let him out
                if agent.pos[1] < 4 and self.guesses[agent.unique_id] < v.COMPETITIVE:
                    x = self.random.randrange(self.grid.width)
                    y = self.random.randrange(4, self.grid.height)
                    while len(self.grid.get_cell_list_contents((x, y))) != 0:
                        x = self.random.randrange(self.grid.width)
                        y = self.random.randrange(4, self.grid.height)
                    self.grid.move_agent(agent, (x, y))
                    # print((x, y))
        for agent in self.model.schedule.agents:
            if isinstance(agent, TradingAgent) and not agent.unique_id == self.unique_id:
                if agent.last_move == "push" and self.guesses[agent.unique_id] > v.COOPERATIVE:
                    # print(self.guesses[agent.unique_id])
                    x = self.random.randrange(self.grid.width)
                    y = self.random.randrange(0, 4)
                    while len(self.grid.get_cell_list_contents((x, y))) != 0:
                        x = self.random.randrange(self.grid.width)
                        y = self.random.randrange(0, 4)
                    self.grid.move_agent(agent, (x, y))
                    # print((x, y))

    def step(self):
        # print("")
        plant = self.check_if_near(Plant, v.PLANT)
        soil = self.check_if_near(Plant, v.SOIL)
        market = self.check_if_near(TradingMarket, 0)
        agents = self.check_if_near_agents(TradingAgent)

        if self.changing_svo:
            self.analyse_others_moves()
            # print(self.guesses)
            if not self.guesses.__contains__(v.COMPETITIVE) and not self.guesses.__contains__(v.SADISTIC):
                if self.svo == v.COMPETITIVE:
                    self.svo = v.SELFISH
            if not self.guesses.__contains__(v.COOPERATIVE) and not self.guesses.__contains__(v.ALTRUISTIC):
                if self.svo == v.COOPERATIVE:
                    self.svo = v.SELFISH
        if self.svo == v.COOPERATIVE or self.svo == v.SELFISH or self.svo == v.ALTRUISTIC:
            if self.prison:
                self.check_on_agents()

        moves = self.find_moves(plant, soil, market, agents)
        if moves:
            pick = self.choose_move(moves)
        else:
            pick = ["wait", 0, 0]
        # print(pick)
        self.do_move(pick, plant, soil, agents)
