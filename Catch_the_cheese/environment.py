from numpy import random
from action import Action
import numpy as np
from copy import deepcopy
from numpy.random import seed
from numpy.random import randint
import random
from parameters_run import ParametersRun

# self.PR.size = ParametersRun.get_PR.size()
NUM_HOLES = 1


class Environment:

    def __init__(self, PR=None):
        self.PR = PR
        # write the map
        self.map = ['H']
        for i in range(1, self.PR.size - 1):
            self.map.append('F')
        self.map.append('C')

        self.index_hole = [0]

        self.action_space = np.array([Action.Left, Action.Right])
        self.state_space = [i for i in range(np.array(self.map).size)]

        self.current_state = 20
        self.score = 0

    def get_holes(self):
        return self.index_hole

    def get_action_space(self):
        return self.action_space

    def get_state_space(self):
        return self.state_space

    def get_random_action(self):
        return np.random.choice(self.action_space)

    def step(self, action_index):
        action = Action(action_index)

        if self.invalid_action(action):
            return self.current_state, -10 * self.PR.size * self.PR.size, False

        if action == Action.Left:
            self.current_state -= 1
        elif action == Action.Right:
            self.current_state += 1

        letter = self.map[self.current_state]

        if letter == 'F':
            return self.current_state, -self.PR.size, False
        if letter == 'C' and self.score < 5:
            self.score += 1
            return self.current_state, 100 * self.PR.size * self.PR.size, False
        if letter == 'C' and self.score >= self.PR.get_score():
            return self.current_state, 10010 * self.PR.size * self.PR.size, True
        else:
            return self.current_state, -10 * self.PR.size * self.PR.size, True

    def stocastic_step(self, action_index, probabiltyOfStep):
        step = self.probabiltyOfSteps(action_index, probabiltyOfStep)
        return self.step(step)

    def probabiltyOfSteps(self, action_index, probabiltyOfStep):  # returns the probability of the actions
        action = Action(action_index)
        validActions = self.get_valid_actions()
        if np.random.uniform(0, 1) < probabiltyOfStep or (len(validActions) == 1 and validActions[0] == action):
            return action
        return np.random.choice(validActions)

    def get_valid_actions(self):
        valid_actions = []
        if self.current_state != 0:
            valid_actions.append(Action.Left)
        if self.current_state != (self.PR.size - 1):
            valid_actions.append(Action.Right)
        return valid_actions

    def valid_actions_of_state(self, state):
        valid_actions = []
        for action in self.action_space:
            if not self.invalid_action_of_state(action, state):
                valid_actions.append(action)
        return valid_actions

    def invalid_action_of_state(self, action, state):
        if (action == Action.Left and state == 0) or \
                (action == Action.Right and state == (self.PR.size - 1)):
            return True

        return False

    def invalid_action(self, action):
        if (action == Action.Left and self.current_state == 0) or \
                (action == Action.Right and self.current_state == (self.PR.size - 1)):
            return True

        return False

    def reset(self):
        self.current_state = self.PR.get_start_point()
        self.score = 0
        return self.current_state

    def print_current_state(self):
        temp_map = deepcopy(self.map)
        for i in range(0, self.PR.size):
            if self.current_state != i:
                if (temp_map[i] == 'F'):
                    print('.', end=" ")
                if (temp_map[i] == 'H'):
                    print('O', end=" ")
                if (temp_map[i] == 'C'):
                    print('C', end=" ")
                if (temp_map[i] == 'S'):
                    print('S', end=" ")
            else:
                print('X', end=" ")

        print()
        print()
