from model import Plant, TradingMarket
import variables as v
import helper_functions as h


# simply chooses a random move
def random_policy(agent):
    valid_moves = h.find_all_valid_moves(agent)
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
    # check if previous path still works
    if len(agent.path) != 0:
        if h.check_if_valid_move(agent, agent.path[0]):
            return agent.path[0]
        else:
            agent.path = []
    # if agent has plant find a market
    if agent.has == v.PLANT:
        goals = h.find_thing(agent, TradingMarket, 0)
        agent.path = h.find_shortest_path(agent, goals)
        return agent.path[0]
    # if agent has seeds find soil
    elif agent.has == v.SEEDS:
        soil = h.find_thing(agent, Plant, v.SOIL)
        if len(soil) != 0:
            agent.path = h.find_shortest_path(agent, soil)
            return agent.path[0]
    # find a plant
    plant = h.find_any_plant(agent)
    if len(plant) == 0:
        plant = h.find_thing(agent, Plant, v.SEEDS)
    agent.path = h.find_shortest_path(agent, plant)
    return agent.path[0]


# building on previous policy this one tries to leave the smaller plants a chance to grow
def let_seeds_grow_policy(agent):
    # check if previous path still works
    if len(agent.path) != 0:
        if h.check_if_valid_move(agent, agent.path[0]):
            return agent.path[0]
        else:
            agent.path = []
    if agent.has == v.PLANT:
        markets = h.find_thing(agent, TradingMarket, 0)
        agent.path = h.find_shortest_path(agent, markets)
        return agent.path[0]
    elif agent.has == v.SEEDS:
        soil = h.find_thing(agent, Plant, v.SOIL)
        if len(soil) != 0:
            agent.path = h.find_shortest_path(agent, soil)
            return agent.path[0]
    # find the biggest available plant
    plants = h.find_biggest_plants(agent, agent.plant_size)
    if len(plants) == 0:
        plants = h.find_thing(agent, Plant, v.SEEDS)
    agent.path = h.find_shortest_path(agent, plants)
    return agent.path[0]


