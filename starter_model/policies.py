from food import Food
from place import Goal, Soil

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
                if isinstance(distant_neighbour, Food) and distant_neighbour.supply > 0:
                    return m

    return agent.random.choice(valid_moves)


# knows where all apples are but not if they have a supply or not unless in immediate proximity
# will move closer to an apple it thinks has a supply
def omnicient_policy(agent):
    food = find_food(agent)
    valid_moves = find_all_valid_moves(agent)
    best_move = [agent.pos, 100]
    for m in valid_moves:
        for f in food:
            d = distance_from(m, f)
            if d < best_move[1]:
                best_move = [m, d]
    return best_move[0]


def distance_from(pos, other_pos):
    return abs(pos[0] - other_pos[0]) + abs(pos[1] - other_pos[1])


def find_all_valid_moves(agent):
    moves = []
    possible_moves = agent.model.grid.get_neighborhood(
        agent.pos, moore=False, include_center=False
    )
    for p in possible_moves:
        if check_if_valid_move(agent, p):
            moves.append(p)
    return moves


def check_if_valid_move(agent, move):
    neighbours = agent.model.grid.get_cell_list_contents(move)
    if len(neighbours) == 0:
        return True
    return False


def find_food(agent):
    food = []
    for agent in agent.model.agents:
        if isinstance(agent, Food):
            if agent.supply > 0:
                food.append(agent.pos)
    return food


def find_place(agent, item):
    places = []
    for agent in agent.model.agents:
        if isinstance(agent, item):
            places.append(agent.pos)
    return places


def trading_policy(agent):
    if agent.has == APPLE:
        goals = find_place(agent, Goal)
        return find_best_move(agent, goals)
    elif agent.has == SEEDS:
        soil = find_place(agent, Soil)
        return find_best_move(agent, soil)
    else:
        return omnicient_policy(agent)


def find_best_move(agent, objs):
    valid_moves = find_all_valid_moves(agent)
    best_move = [agent.pos, 100]
    for m in valid_moves:
        for o in objs:
            d = distance_from(m, o)
            if d < best_move[1]:
                best_move = [m, d]
    return best_move[0]
