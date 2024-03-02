from food import Food


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
    valid_moves = find_all_valid_moves(agent)
    best_move = [agent.pos, 100]
    for m in valid_moves:
        for food in agent.food:
            if food[0] > 0:
                d = distance_from_food(m, (food[1], food[2]))
                if d < best_move[1]:
                    best_move = [m, d]
    return best_move[0]


def distance_from_food(pos, food_pos):
    return abs(pos[0] - food_pos[0]) + abs(pos[1] - food_pos[1])


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
    if len(neighbours) != 0:
        return False
    else:
        return True

