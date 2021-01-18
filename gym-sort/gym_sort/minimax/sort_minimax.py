from gym_sort.game.sort import Sort
from copy import deepcopy


def minimax(sort, depth):
    if depth == 0 or not sort._check_win()[0]:
        return sort.final_score(), sort

    maxEval = float('-inf')
    best_move_result = None
    best_move = None
    for new_game, move in get_all_moves(sort):
        evaluation = minimax(new_game, depth-1)[0]
        maxEval = max(maxEval, evaluation)
        if maxEval == evaluation:
            best_move_result = new_game
            best_move = move
    return maxEval, best_move_result, best_move


def simulate_move(move, sort):
    origin, destiny = move
    sort.change_tube(origin, destiny)
    return sort


def get_all_moves(sort):
    moves = []
    for move in sort.get_valid_moves():
        temp_sort = deepcopy(sort)
        new_sort = simulate_move(move, temp_sort)
        moves.append([new_sort, move])
    return moves