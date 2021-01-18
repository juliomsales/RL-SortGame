from gym_sort.envs.sort_env import WaterSortEnv

visualization = True
episodes = 10
env = WaterSortEnv(14, 0, visualization)
for episode in range(1, episodes + 1):
    state = env.reset()
    done = False
    score = 0
    while not done:
        if visualization:
            env.render()
        action = env.action_space.sample()
        n_state, reward, done, info = env.step(action)
        score += reward
    print(f'Episode:{episode} Score:{score}')
