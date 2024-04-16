from model import Plant, TradingMarket
from Helpers import variables as v
from Agents import agents as ag


def list_contains(p, ls):
    for elem in ls:
        if p == elem:
            return True
    return False


def lists_contain(ps, ls):
    for elem in ls:
        for p in ps:
            if p == elem:
                return True
    return False


def distance_from(pos, other_pos):
    return abs(pos[0] - other_pos[0]) + abs(pos[1] - other_pos[1])


def check_if_valid_move(agent, move):
    neighbours = agent.model.grid.get_cell_list_contents(move)
    if len(neighbours) == 0:
        return True
    return False


def get_random_move(agent):
    valid_moves = find_all_valid_moves(agent)
    if len(valid_moves) == 0:
        return agent.pos
    return agent.random.choice(valid_moves)


def is_agent_in_the_way(a):
    if isinstance(a.check_if_near(Plant, v.PLANT), Plant):
        return True
    elif isinstance(a.check_if_near(TradingMarket, 0), TradingMarket):
        return True
    return False


def others_hunger(agents, agent):
    collective_hunger = 0
    for a in agents:
        if isinstance(a, ag.TradingAgent) and a.unique_id != agent.unique_id:
            collective_hunger += a.hunger
    return collective_hunger


def count(agent, obj):
    counter = 0
    for agent in agent.model.agents:
        if isinstance(agent, obj):
            if isinstance(agent, Plant):
                if v.SEEDS > agent.size > v.SOIL:
                    counter += agent.size
            else:
                counter += 1
    return counter


def find_all_valid_moves(agent):
    moves = []
    possible_moves = agent.model.grid.get_neighborhood(
        agent.pos, moore=False, include_center=False
    )
    for p in possible_moves:
        if check_if_valid_move(agent, p):
            moves.append(p)
    return moves


def find_all_valid_moves_given_position(agent, pos):
    moves = []
    possible_moves = agent.model.grid.get_neighborhood(
        pos, moore=False, include_center=False
    )
    for p in possible_moves:
        if check_if_valid_move(agent, p):
            moves.append(p)
    return moves


def find_thing(agent, item, size):
    items = []
    for a in agent.model.agents:
        if isinstance(a, item):
            if item == Plant:
                if size == v.PLANT and (a.size == v.BABY_PLANT or a.size == v.MEDIUM_PlANT or a.size == v.BIG_PlANT or a.size == v.HUGE_PlANT):
                    items.append(a.pos)
                elif size == v.SOIL and a.size == size:
                    items.append(a.pos)
            elif item == ag.TradingAgent and a.pos != agent.pos:
                items.append(a.pos)
            elif item == TradingMarket:
                items.append(a.pos)
    return items


def find_any_plant(agent):
    items = []
    for a in agent.model.agents:
        if isinstance(a, Plant) and v.SEEDS > a.size > v.SOIL:
            items.append(a.pos)
    return items


def find_biggest_plants(agent, size):
    plants = find_thing(agent, Plant, size)
    while len(plants) == 0 and size > v.SOIL:
        size -= 1
        plants = find_thing(agent, Plant, size)
    return plants


def find_hungriest_agent(agent):
    hungriest_agent = agent
    for a in agent.model.agents:
        if isinstance(a, ag.TradingAgent) and 4 > a.hunger > hungriest_agent.hunger:
            hungriest_agent = a
    return hungriest_agent


def find_best_move(agent, objs):
    valid_moves = find_all_valid_moves(agent)
    best_move = [agent.pos, 100]
    if len(objs) == 0:
        return best_move[0]
    for m in valid_moves:
        for o in objs:
            d = distance_from(m, o)
            if d < best_move[1]:
                best_move = [m, d]
    return best_move[0]


def find_best_move_given_path(agent, move, objs, path):
    valid_moves = find_all_valid_moves_given_position(agent, move)
    best_move = [agent.pos, 100]
    for m in valid_moves:
        for o in objs:
            d = distance_from(m, o)
            if d < best_move[1] and not list_contains(m, path):
                best_move = [m, d]
    return best_move[0]


def find_shortest_path_helper(agent, objs):
    paths = []
    moves_tried = []
    moves = find_all_valid_moves(agent)
    if len(moves) == 0:
        print("no moves available")
        return [agent.pos]

    random_move = agent.random.choice(moves)
    if len(objs) == 0:
        print("no places to go")
        return [agent.pos]

    for m in moves:
        paths.append([m])
        moves_tried.append(m)
        neighborhood = agent.model.grid.get_neighborhood(m, moore=False, include_center=False)
        if lists_contain(neighborhood, objs):
            return [m]

    while len(paths) != 0:
        new_paths = []
        for p in paths:
            moves = find_all_valid_moves_given_position(agent, p[len(p) - 1])
            for m in moves:
                if not list_contains(m, moves_tried):
                    new_paths.append(p + [m])
                    moves_tried.append(m)
            neighborhood = agent.model.grid.get_neighborhood(p[len(p) - 1], moore=False, include_center=False)
            if lists_contain(neighborhood, objs):
                return p
        paths = new_paths
    print("can't find a path")
    return []


def find_shortest_path(agent, objs):
    path = find_shortest_path_helper(agent, objs)
    if not path:
        return find_best_move(agent, objs)
    else:
        return path[0]

