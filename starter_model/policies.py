from model import Plant, TradingMarket
import variables as v
import helper_functions as h
import agents as a


# simply chooses a random move
def random_policy(agent):
    valid_moves = h.find_all_valid_moves(agent)
    if len(valid_moves) == 0:
        return agent.pos
    return agent.random.choice(valid_moves)


# can only see if in immediate proximity of apple
def stay_close_policy(agent):
    valid_moves = h.find_all_valid_moves(agent)
    for m in valid_moves:
        neighbourhood = agent.model.grid.get_neighborhood(
            m, moore=True, include_center=True
        )
        for n in neighbourhood:
            distant_neighbours = agent.model.grid.get_cell_list_contents(n)
            for distant_neighbour in distant_neighbours:
                if isinstance(distant_neighbour, Plant) and distant_neighbour.size > 0:
                    return m

    return agent.random.choice(valid_moves)


# knows where all apples are but not if they have a supply or not unless in immediate proximity
# will move closer to an apple it thinks has a supply
def omniscient_policy(agent):
    plant = h.find_thing(agent, Plant, v.PLANT)
    valid_moves = h.find_all_valid_moves(agent)
    best_move = [agent.pos, 100]
    if len(valid_moves) != 0 and len(plant) != 0:
        for m in valid_moves:
            for f in plant:
                d = h.distance_from(m, f)
                if d < best_move[1]:
                    best_move = [m, d]
    return best_move[0]


# this policy allows agent to trade plants for seeds
def simple_trading_policy(agent):
    # if agent has plant find a market
    if agent.has == v.PLANT:
        goals = h.find_thing(agent, TradingMarket, 0)
        return h.find_shortest_path(agent, goals)
    # if agent has seeds find soil
    elif agent.has == v.SEEDS:
        soil = h.find_thing(agent, Plant, v.SOIL)
        if len(soil) != 0:
            return h.find_shortest_path(agent, soil)
    # find a plant
    plant = h.find_any_plant(agent)
    if len(plant) == 0:
        plant = h.find_thing(agent, Plant, v.SEEDS)
    return h.find_shortest_path(agent, plant)


# building on previous policy this one tries to leave the smaller plants a chance to grow
def let_seeds_grow_policy(agent):
    if agent.has == v.PLANT:
        markets = h.find_thing(agent, TradingMarket, 0)
        return h.find_shortest_path(agent, markets)
    elif agent.has == v.SEEDS:
        soil = h.find_thing(agent, Plant, v.SOIL)
        if len(soil) != 0:
            return h.find_shortest_path(agent, soil)
    # find the biggest available plant
    plants = h.find_biggest_plants(agent, v.SIZE)
    if len(plants) == 0:
        plants = h.find_thing(agent, Plant, v.SEEDS)
    return  h.find_shortest_path(agent, plants)


# agents following this policy will move towards very hungry agents if they have food to give them
def altruistic_policy(agent):
    # if an agent is really hungry go feed him, else trade at the market
    if agent.has == v.PLANT:
        hungriest_agent = h.find_hungriest_agent(agent)
        if hungriest_agent.hunger > 2.5 and hungriest_agent.pos != agent.pos:
            return h.find_shortest_path(agent, hungriest_agent.pos)
        else:
            markets = h.find_thing(agent, TradingMarket, 0)
            return h.find_shortest_path(agent, markets)
    elif agent.has == v.SEEDS:
        soil = h.find_thing(agent, Plant, v.SOIL)
        if len(soil) != 0:
            return h.find_shortest_path(agent, soil)
    # find the biggest available plant
    plants = h.find_biggest_plants(agent, v.SIZE)
    if len(plants) == 0:
        plants = h.find_thing(agent, Plant, v.SEEDS)
    return h.find_shortest_path(agent, plants)


def competitive_policy(agent):
    # if agent has plant find a market
    if agent.has == v.PLANT:
        goals = h.find_thing(agent, TradingMarket, 0)
        return h.find_shortest_path(agent, goals)
    # if agent has seeds find soil
    elif agent.has == v.SEEDS:
        soil = h.find_thing(agent, Plant, v.SOIL)
        if len(soil) != 0:
            return h.find_shortest_path(agent, soil)
    # find a plant
    plant = h.find_any_plant(agent)
    if len(plant) == 0:
        other_agents = h.find_thing(agent, a.TradingAgent, 0)
        plants = h.find_thing(agent, Plant, v.PLANT)
        for p in plants:
            for o in other_agents:
                neighborhood = o.grid.get_neighborhood(o.pos, moore=False, include_center=False)
                for n in neighborhood:
                    if p == n:
                        return h.find_shortest_path(agent, [o.pos])
        plant = h.find_thing(agent, Plant, v.SEEDS)
    return h.find_shortest_path(agent, plant)


# agents following this policy will eat when hungry and otherwise will go towards agents (to disturb them)
def sadistic_policy(agent):
    thing = h.find_any_plant(agent)
    if len(thing) == 0:
        thing = h.find_thing(agent, a.TradingAgent, 0)
    move = h.find_shortest_path(agent, thing)
    if not move:
        move = agent.pos
    return move

