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
    def __init__(self, unique_id, model, svo):
        super().__init__(unique_id, model)
        self.svo = svo
        self.last_move = "nothing"
        if svo == v.ALTRUISTIC:
            self.hunger_limit = 3
        else:
            self.hunger_limit = 1.5
        self.hunger = 0
        self.has = v.NOTHING

    def move(self):
        moves = self.calc_moves()
        if moves:
            pick = self.choose_move(moves)
            print("let's go towards ", pick[0])
            pick = pick[3]
        else:
            pick = h.get_random_move(self)
        self.grid.move_agent(self, pick)
        self.hunger += 0.1

    def calc_moves(self):
        soil = h.find_thing(self, Plant, v.SOIL)
        plants = h.find_thing(self, Plant, v.PLANT)
        agents = h.find_thing(self, TradingAgent, 0)
        markets = h.find_thing(self, TradingMarket, 0)

        paths = [h.find_shortest_path_helper(self, soil), h.find_shortest_path_helper(self, plants),
                 h.find_shortest_path_helper(self, agents), h.find_shortest_path_helper(self, markets)]

        moves = []
        if paths[1] and paths[1][0] != self.pos:
            if self.has == v.PLANT:
                moves = [["plant", 1 - (len(paths[1]) / 100), 0, paths[1][0]]]
            else:
                moves = [["plant", 1 - (len(paths[1]) / 100) + self.hunger, 0, paths[1][0]]]
        if self.has == v.PLANT:
            if paths[3] and paths[3][0] != self.pos:
                moves.append(["market", 1 - (len(paths[3]) / 100), 0.5 - (len(paths[3]) / 100), paths[3][0]])
            if paths[2] and paths[2][0] != self.pos:
                moves.append(["agent", - 1 - (len(paths[2]) / 100), 1 - (len(paths[2]) / 100), paths[2][0]])
        else:
            if paths[3] and paths[3][0] != self.pos:
                moves.append(["market", 0 - (len(paths[3]) / 100), 0 - (len(paths[3]) / 100), paths[3][0]])
            if paths[2] and paths[2][0] != self.pos:
                moves.append(["agent", 0.5 - (len(paths[2]) / 100), - 0.5 - (len(paths[2]) / 100), paths[2][0]])
        if paths[0] and paths[0][0] != self.pos:
            if self.has == v.SEEDS:
                moves.append(["soil", 1 - (len(paths[0]) / 100), 0.5 - (len(paths[0]) / 100), paths[0][0]])
            else:
                moves.append(["soil", 0 - (len(paths[0]) / 100), 0 - (len(paths[0]) / 100), paths[0][0]])
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
        if move[0] == "move":
            self.move()
        elif move[0] == "eat_stored":
            self.eat_stored()
            print("eating stored food")
        elif move[0] == "take":
            self.take_food(plant)
            print("taking")
        elif move[0] == "eat":
            self.eat(plant)
            print("eating")
        elif move[0] == "wait":
            self.wait()
            print("waiting")
        elif move[0] == "push":
            self.push(agent[0])
            print("pushing")
        elif move[0] == "plant":
            self.plant(soil)
            print("planting")
        elif move[0] == "trade":
            self.trade()
            print("trading")
        elif move[0] == "give":
            self.give(agent[0])
            print("giving")

    def find_moves(self, plant, soil, market, agents):
        self_hunger = self.hunger / 10
        collective_hunger = h.others_hunger(self.model.agents, self)
        collective_hunger = (collective_hunger / h.count(self, TradingAgent)) / 10

        moves = [["move", 0, 0]]
        print("self: ", self_hunger, " vs collective: ", collective_hunger)

        if plant:
            take = ["take", 0.5 + self_hunger, 0]
            eat = ["eat", 1 + self_hunger, - 1 - collective_hunger]
            wait = ["wait", -0.1, -0.5 - collective_hunger]
            if plant.size < v.MEDIUM_PlANT:
                take = ["take", 0.5, 0 - collective_hunger]
                eat = ["eat", 0.1 + self_hunger, -1.5 - collective_hunger]
                wait = ["wait", 1, -0.5 - collective_hunger]
            if self.has == v.NOTHING:
                moves.append(take)
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
                            moves.append(["push", -0.5 + self_hunger, -0.5 - collective_hunger])
                        else:
                            moves.append(["push", -0.5 + self_hunger, -0.5])
                    else:
                        if collective_hunger > 0:
                            moves.append(["push", -0.5, -0.5 - collective_hunger])
                        else:
                            moves.append(["push", -0.5, -0.5])
        if self.has == v.PLANT:
            moves.append(["eat_stored", 1 + (self_hunger * 1.5), -1.5 - collective_hunger])
        return moves

    def step(self):
        print("")
        plant = self.check_if_near(Plant, v.PLANT)
        soil = self.check_if_near(Plant, v.SOIL)
        market = self.check_if_near(TradingMarket, 0)
        agents = self.check_if_near_agents(TradingAgent)

        moves = self.find_moves(plant, soil, market, agents)
        print(self.unique_id, moves)
        pick = self.choose_move(moves)
        self.do_move(pick, plant, soil, agents)

