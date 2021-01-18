from gym.envs.registration import register

register(
    id='sort-v0',
    entry_point='gym_sort.envs:SortEnv',
)
register(
    id='sort-extrahard-v0',
    entry_point='gym_sort.envsSortExtraHardEnv',
)