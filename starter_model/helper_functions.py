from model import Plant, TradingMarket
import variables as v


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


def is_agent_in_the_way(a):
    if isinstance(a.check_if_near(Plant, v.PLANT), Plant):
        return True
    elif isinstance(a.check_if_near(TradingMarket, 0), TradingMarket):
        return True
    return False


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
                if size == a.size:
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
        if a.hunger > hungriest_agent.hunger:
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


def find_shortest_path(agent, objs):
    paths = []
    moves_tried = []
    moves = find_all_valid_moves(agent)
    if len(moves) == 0:
        return [agent.pos]

    random_move = agent.random.choice(moves)
    if len(objs) == 0:
        return [random_move]

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
    return []

