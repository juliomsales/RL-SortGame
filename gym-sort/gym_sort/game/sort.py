from random import Random
from copy import deepcopy


class Sort:
    def __init__(self, n_tubes, random_seed):
        self.random_seed = random_seed
        self.N_TUBES = n_tubes
        self.SIZE_TUBE = 4
        self.colors = []

        self.win = 0
        self.rewards = 0
        self.join_colors = 0
        self.valid_moves = 0
        self.invalid_moves = 0
        self.repetitive_moves = 0
        self.n_moves = 0
        self.lose = 0
        self.useless = 0
        self.penalties = 0
        self.cur_balance = {}

        self.last_move = (0, 0)
        self.COLORS_RGB = {
            1: (255, 0, 0),
            2: (0, 255, 0),
            3: (0, 0, 255),
            4: (255, 255, 0),
            5: (0, 255, 255),
            6: (255, 0, 255),
            7: (128, 128, 128),
            8: (128, 0, 0),
            9: (128, 128, 0),
            10: (0, 128, 0),
            11: (128, 0, 128),
            12: (0, 128, 128),
            13: (0, 0, 128)
        }
        self._generate_tubes()

    def _generate_tubes(self):
        for i in range(1, self.N_TUBES - 1):
            for _ in range(self.SIZE_TUBE):
                self.colors.append(i)

        Random(self.random_seed).shuffle(self.colors)

        self.tubes = [self.colors[i:i + self.SIZE_TUBE] for i in range(0, len(self.colors), self.SIZE_TUBE)]
        self.tubes.append([])
        self.tubes.append([])
        self.aux_tubes = deepcopy(self.tubes)
        for tube in self.aux_tubes:
            while len(tube) != 4:
                tube.append(0)
        self.original_tube = deepcopy(self.tubes)

    def change_tube(self, origin, destiny):
        old = deepcopy(self.final_score())
        self.move()
        if origin == destiny:
            self.invalid_move()
        elif (len(self.tubes[destiny]) == self.SIZE_TUBE) or (len(self.tubes[origin]) == 0):
            self.invalid_move()
        elif len(self.tubes[destiny]) == 0 or self.tubes[origin][-1] == self.tubes[destiny][-1]:
            self.useless += 1 if len(self.tubes[destiny]) == 0 and len(set(self.tubes[origin])) == 1 else 0
            if (destiny, origin) == self.last_move:
                self.repetitive_move()
            self.last_move = (origin, destiny)
            self.valid_move()
            original_last = self.tubes[origin][-1]
            while original_last == self.tubes[origin][-1]:
                self.tubes[destiny].append(self.tubes[origin][-1])
                self.tubes[origin].pop()
                if len(self.tubes[origin]) == 0 or len(self.tubes[destiny]) == self.SIZE_TUBE:
                    break
        else:
            self.invalid_move()

        done, state = self._check_win()

        self.join_color()
        self.score()
        self.penalty()

        self.aux_tubes = deepcopy(self.tubes)
        for tube in self.aux_tubes:
            while len(tube) != 4:
                tube.append(0)

        new = self.final_score()
        this_move_reward = new - old

        return done, this_move_reward

    def _check_win(self):
        list_win = []
        for tube in self.tubes:
            if len(tube) == 0 or len(tube) == 4:
                if len(set(tube)) == 1 or len(tube) == 0:
                    list_win.append('ok')
                else:
                    list_win.append('nok')
            else:
                list_win.append('nok')
                pass
        if len(set(list_win)) == 1 and list_win[0] == 'ok':
            self.win += 100
            self.score()
            self.penalty()
            return False, 'win'
        else:
            if len(self.get_valid_moves()) == 0:
                self.lose += 100
                self.score()
                self.penalty()
                return False, 'lose'
            else:
                return True, 'continue'

    def reset_game(self):
        self.tubes = deepcopy(self.original_tube)
        self.valid_moves = 0
        self.join_colors = 0
        self.invalid_moves = 0
        self.repetitive_moves = 0
        self.n_moves = 0
        self.rewards = 0

    def get_valid_moves(self):
        valid_moves = []
        for origin in range(len(self.tubes)):
            for destiny in range(len(self.tubes)):
                if origin == destiny:
                    pass
                elif (len(self.tubes[destiny]) == self.SIZE_TUBE) or (len(self.tubes[origin]) == 0):
                    pass
                elif len(self.tubes[destiny]) == 0 and len(set(self.tubes[origin])) == 1:
                    pass
                elif (len(self.tubes[destiny]) == 0) or (self.tubes[origin][-1] == self.tubes[destiny][-1]):
                    if self.tubes[origin].count(self.tubes[origin][-1]) != self.SIZE_TUBE:
                        valid_moves.append((origin, destiny))
                else:
                    pass
        return valid_moves

    def get_valid_moves_aux(self):
        moves = self.get_valid_moves()
        while len(moves) < 24:
            moves.append((0, 0))
        return moves

    # REWARDS AND PENALTIES
    def score(self):  # Reward
        self.rewards = self.join_colors + self.valid_moves + self.win

    def valid_move(self):  # Reward
        self.valid_moves += 1

    def join_color(self):  # Reward
        self.join_colors = 0
        for tube in self.tubes:
            if len(tube) != 0 and tube.count(tube[-1]) > 1:
                top_color = tube[-1]
                i = 2
                while tube[-i] == top_color:
                    self.join_colors += 2
                    i += 1
                    if i > len(tube):
                        break
                if i >= 3:
                    self.join_colors += 2

    def invalid_move(self):  # Penalty
        self.invalid_moves += 1

    def repetitive_move(self):  # Penalty
        self.repetitive_moves += 1

    def move(self):  # Penalty
        self.n_moves += 1

    def penalty(self):
        self.penalties = self.repetitive_moves + self.invalid_moves + self.lose + self.n_moves + self.useless

    def balance(self):
        self.cur_balance['Valid_moves']      = self.valid_moves
        self.cur_balance['Joined_colors']    = self.join_colors
        self.cur_balance['Invalid_moves']    = self.invalid_moves
        self.cur_balance['Repetitive_moves'] = self.repetitive_moves
        self.cur_balance['Useless_moves']    = self.useless
        self.cur_balance['Total_moves']      = self.n_moves
        self.cur_balance['Rewards']          = self.rewards
        self.cur_balance['Penalties']        = self.penalties
        self.cur_balance['Final_Score']      = self.final_score()
        return self.cur_balance

    def final_score(self):
        return self.rewards - self.penalties
