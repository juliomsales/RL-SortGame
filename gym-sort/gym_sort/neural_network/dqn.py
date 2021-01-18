import numpy as np
import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam, Nadam
from rl.agents import DQNAgent, NAFAgent, DDPGAgent
from rl.policy import BoltzmannQPolicy, LinearAnnealedPolicy, EpsGreedyQPolicy
from rl.memory import SequentialMemory

from gym_sort.envs.sort_env import WaterSortEnv


def build_model(actions, states):
    model = Sequential()
    model.add(Flatten(input_shape=(1, states)))
    model.add(Dense(states, activation='relu'))
    model.add(Dense(states * 2, activation='relu'))
    model.add(Dense(states * 4, activation='relu'))
    model.add(Dense(states, activation='relu'))
    model.add(Dense(actions, activation='softmax'))
    return model


def build_agent(model, actions):
    policy = LinearAnnealedPolicy(EpsGreedyQPolicy(),
                                  attr='eps',
                                  value_max=10.,
                                  value_min=.01,
                                  value_test=.1,
                                  nb_steps=10000)
    memory = SequentialMemory(limit=100000, window_length=1)
    dqn = DQNAgent(model=model,
                   memory=memory,
                   policy=policy,
                   nb_actions=actions,
                   nb_steps_warmup=1000)
    return dqn

vis = False
env = WaterSortEnv(8, 0, vis)
states = env.state.shape[0]
actions = env.action_space.n

model = build_model(actions, states)
# model.summary()

dqn = build_agent(model, actions)
dqn.compile(Nadam(), metrics=['mae'])
dqn.fit(env, nb_steps=100000, visualize=vis, verbose=2)
