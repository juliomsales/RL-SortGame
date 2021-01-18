import pygame
import time
from copy import deepcopy
from gym_sort.minimax.sort_minimax import minimax


class WaterSort:

    def __init__(self, game_backend, ia=(False, 0)):
        self.ia_minimax = ia[0]
        self.minimax_depth = ia[1]
        self.game = game_backend
        pygame.init()
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Arial', 30)
        self.x, self.y = 50, 50
        self.width, self.height = 60, 50
        self.fps = 0
        self.clock = pygame.time.Clock()

    def start_game(self):
        self._window()
        self._areas()
        self._reset_view()
        self._run()
        pygame.quit()

    def _reset_game(self):
        self.game.reset_game()

    def _window(self):
        if self.game.N_TUBES <= 6:
            len = self.game.N_TUBES * 100 + 60
            height = 300
        else:
            len = self.game.N_TUBES * 50 + 60
            height = 550
        self.win = pygame.display.set_mode((len, height))
        pygame.display.set_caption("Water Sort")
        self.win.fill((25, 25, 25))

    def _areas(self):
        self.extremities = []
        y1, j = self.y, 0
        for i in range(self.game.N_TUBES):
            if i == round(self.game.N_TUBES / 2) and self.game.N_TUBES > 6:
                y1 += 250
                j = self.game.N_TUBES / 2
            x1 = self.x + 100 * (i - j)
            point1 = (x1, y1)
            point2 = (x1, y1 + 200)
            point3 = (x1 + 60, y1 + 200)
            point4 = (x1 + 60, y1)
            self.extremities.append([point1, point2, point3, point4])

    def _draw_lines(self):
        for points in self.extremities:
            pygame.draw.lines(self.win, (255, 255, 255), False, points, 3)
        pygame.display.update()

    def _draw_colors(self):
        for i in range(len(self.game.tubes)):
            x1, y1 = self.extremities[i][1]
            y1 -= 50
            for color in self.game.tubes[i]:
                pygame.draw.rect(self.win, self.game.COLORS_RGB.get(color), (x1, y1, self.width, self.height))
                y1 -= 50
        pygame.display.update()

    def _reset_view(self):
        self.win.fill((25, 25, 25))
        self._draw_colors()
        self._draw_lines()
        pygame.display.update()

    def _click_mouse(self):
        pos = pygame.mouse.get_pos()
        in_tube = False
        for area in self.extremities:
            x1, y1 = area[0]
            x2, y2 = area[2]
            if x1 < pos[0] < x2 and y1 < pos[1] < y2:
                self._click_in_tube(area)
                in_tube = True
        if not in_tube:
            self._reset_view()
            self.sequence_click = []

    def _click_in_tube(self, area):
        tube1 = self.extremities.index(area) + 1
        pygame.draw.lines(self.win, (255, 200, 0), False, area, 5)
        pygame.display.update()
        self.sequence_click.append(tube1 - 1)

    def _run(self):
        self.run1 = True
        self.sequence_click = []
        while self.run1:
            if self.ia_minimax == True:
                best_move = minimax(self.game, self.minimax_depth)[2]
                origin, destiny = best_move
                self._click_in_tube(self.extremities[origin])
                time.sleep(0.5)
                self._click_in_tube(self.extremities[destiny])
                time.sleep(0.5)
                self.run1, _ = self.game.change_tube(origin, destiny)
                print(self.game.final_score())
                self._reset_view()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run1 = False

                    if event.type == pygame.MOUSEBUTTONUP:
                        self._click_mouse()
                        if len(self.sequence_click) == 2:
                            self.run1, _ = self.game.change_tube(self.sequence_click[0], self.sequence_click[1])
                            self.sequence_click = []
                            time.sleep(0.2)
                            self._reset_view()
                            print(self.game.balance())
                        elif len(self.sequence_click) == 0:
                            self._reset_view()

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_r:
                            self._reset_game()
                            self._reset_view()

    def get_balance(self):
        return self.game.balance()

    def get_valid_moves(self):
        return self.game.get_valid_moves()
