from gym_sort.game.sort import Sort
from gym_sort.game.sort_vis import WaterSort

a = Sort(8, 0)
minimax = True
depth = 5
b = WaterSort(a, (minimax, depth))
b.start_game()