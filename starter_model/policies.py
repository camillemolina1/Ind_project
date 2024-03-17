from plant import Plant
from place import TradingMarket, Soil

NOTHING = 0
APPLE = 1
SEEDS = 2


# simply chooses a random move
def random_policy(agent):
    valid_moves = find_all_valid_moves(agent)
    return agent.random.choice(valid_moves)


# can only see if in immediate proximity of apple
def stay_close_policy(agent):
    valid_moves = find_all_valid_moves(agent)
    for m in valid_moves:
        neighbourhood = agent.model.grid.get_neighborhood(
            m, moore=True, include_center=True
        )
        for n in neighbourhood:
            distant_neighbours = agent.model.grid.get_cell_list_contents(n)
            for distant_neighbour in distant_neighbours:
                if isinstance(distant_neighbour, Plant) and distant_neighbour.supply > 0:
                    return m

    return agent.random.choice(valid_moves)


# knows where all apples are but not if they have a supply or not unless in immediate proximity
# will move closer to an apple it thinks has a supply
def omniscient_policy(agent):
    food = find_thing(agent, Plant)
    valid_moves = find_all_valid_moves(agent)
    best_move = [agent.pos, 100]
    if len(valid_moves) != 0 and len(food) != 0:
        for m in valid_moves:
            for f in food:
                d = distance_from(m, f)
                if d < best_move[1]:
                    best_move = [m, d]
    return best_move[0]


def trading_policy(agent):
    if agent.has == APPLE:
        print("finding trading station")
        goals = find_thing(agent, TradingMarket)
        return find_shortest_path(agent, goals)
    elif agent.has == SEEDS:
        print("finding soil")
        soil = find_thing(agent, Soil)
        return find_shortest_path(agent, soil)
    else:
        print("finding apple")
        food = find_thing(agent, Plant)
        return find_shortest_path(agent, food)


def distance_from(pos, other_pos):
    return abs(pos[0] - other_pos[0]) + abs(pos[1] - other_pos[1])


def check_if_valid_move(agent, move):
    neighbours = agent.model.grid.get_cell_list_contents(move)
    if len(neighbours) == 0:
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


def find_thing(agent, item):
    items = []
    for a in agent.model.agents:
        if isinstance(a, item):
            if item == Plant and a.supply > 0:
                items.append(a.pos)
            elif item == Soil and a.contains != APPLE:
                items.append(a.pos)
            elif item == TradingMarket:
                items.append(a.pos)
    return items


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
    random_move = agent.random.choice(moves)

    if len(objs) == 0:
        return random_move

    for m in moves:
        paths.append([m])
        moves_tried.append(m)
        neighborhood = agent.model.grid.get_neighborhood(m, moore=False, include_center=False)
        if lists_contain(neighborhood, objs):
            return m

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
                print(p[0])
                return p[0]
        paths = new_paths
    return find_best_move(agent, objs)


def list_contains(p, ls):
    for l in ls:
        if p == l:
            return True
    return False


def lists_contain(ps, ls):
    for l in ls:
        for p in ps:
            if p == l:
                return True
    return False
