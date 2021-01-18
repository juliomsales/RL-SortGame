from gym import Env
from gym.spaces import Discrete, Box, MultiDiscrete, Space
from gym_sort.game.sort import Sort
import numpy as np
import pygame
import time


class WaterSortEnv(Env):
    def __init__(self, n_tubes, random_seed, vis=False):
        self.vis = vis
        self.n_tubes, self.random_seed = n_tubes, random_seed
        self.x, self.y = 50, 50
        self.width, self.height = 60, 50
        self._init()
        self.action_space = Discrete(self.game.N_TUBES ** 2)
        self.observation_space = Box(low=np.float32(0), high=np.float32(self.game.N_TUBES), shape=self.shape)

    def step(self, action):
        progress = 0
        for i in range(self.game.N_TUBES):
            for j in range(self.game.N_TUBES):
                if action == progress:
                    self.origin, self.destiny = i, j
                progress += 1
        check_done, reward = self.game.change_tube(self.origin, self.destiny)
        self.state = np.array(self.game.aux_tubes).reshape(self.shape)
        if self.duration <= 0:
            reward -= 100
            done = True
        elif check_done == False:
            done = True
        else:
            done = False
        self.duration -= 1
        return np.copy(self.state), reward, done, {}

    def render(self, mode='human'):
        self._run()

    def reset(self):
        self._init()
        return np.copy(self.state)

    def _init(self):
        self.game = Sort(self.n_tubes, self.random_seed)
        self.shape = (self.game.N_TUBES * self.game.SIZE_TUBE,)
        self.state = np.array(self.game.aux_tubes).reshape(self.shape)
        self.duration = 100
        self.origin = -1

        if self.vis:
            pygame.init()
            self.fps = 10
            self.clock = pygame.time.Clock()
            self.running = True
            self._window()
            self._areas()

    def _window(self):
        if self.game.N_TUBES <= 6:
            len = self.game.N_TUBES * 100 + 60
            height = 300
        else:
            len = self.game.N_TUBES * 50 + 60
            height = 550
        self.win = pygame.display.set_mode((len, height))
        pygame.display.set_caption("Water Sort")
        self.win.fill((35, 35, 35))

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

    def _run(self):
        self.clock.tick(self.fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return False
        if self.origin != -1:
            self._click_in_tube(self.extremities[self.origin])
            time.sleep(0.5)
            self._click_in_tube(self.extremities[self.destiny])
            time.sleep(0.5)
        self._reset_view()

    def _reset_view(self):
        self.win.fill((35, 35, 35))
        self._draw_colors()
        self._draw_lines()
        pygame.display.update()

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

    def _click_in_tube(self, area):
        tube1 = self.extremities.index(area) + 1
        pygame.draw.lines(self.win, (255, 200, 0), False, area, 5)
        pygame.display.update()