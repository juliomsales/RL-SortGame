from gym_sort.game.sort import Sort
from gym_sort.game.sort_vis import WaterSort

a = Sort(14, 0)
b = WaterSort(a)
b.start_game()