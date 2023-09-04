# from numpy import random, self.SIZE
from action import Action
import numpy as np
from copy import deepcopy
from numpy.random import seed
from numpy.random import randint
import random
import parameters_run


# self.SIZE=parameters_run.get_self.SIZE()
# NUM_HOLES=int(self.SIZE*self.SIZE/8)
# random.seed(0)
# self.SIZE=parameters_run.get_self.SIZE()
# NUM_HOLES=int(self.SIZE*self.SIZE/8)


class Environment:

    def __init__(self):  # initialize the environment
        self.SIZE = parameters_run.get_size()
        # self.SIZE=self.self.SIZE
        # write the map
        self.map = ['S']
        for i in range(1, self.SIZE * self.SIZE - 1):
            self.map.append('F')
        self.map.append('G')
        direction = 1
        self.index_hole = []

        # self.index_hole=random.sample(range((2),(self.SIZE*self.SIZE-3)), NUM_HOLES)
        # for i in self.index_hole:
        # self.map[i]='H'
        """
        for i in range(self.SIZE):
          if i%2==1:
           if direction==1:
             for j in range(self.SIZE-2):
              self.index_hole.append((i)*self.SIZE+j)
              self.map[(i)*self.SIZE+j]='H'
             direction=2
           else:
             for j in range(self.SIZE-2):
              self.index_hole.append((i)*self.SIZE+self.SIZE-j-1)
              self.map[(i)*self.SIZE+self.SIZE-j-1]='H'
             direction=1
          """
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                self.index_hole.append((i) * self.SIZE + j)
                self.map[(i) * self.SIZE + j] = 'H'

        for i in range(self.SIZE):
            self.map[i] = 'F'
            if i in self.index_hole:
                self.index_hole.remove(i)
        for i in range(self.SIZE):
            self.map[i * self.SIZE + self.SIZE - 1] = 'F'
            if i + self.SIZE - 1 in self.index_hole:
                self.index_hole.remove(i * self.SIZE + self.SIZE - 1)
        self.map[(self.SIZE) * self.SIZE - 1] = 'G'

        self.action_space = np.array([Action.Left, Action.Right, Action.Up, Action.Down])
        self.state_space = [i for i in range(np.array(self.map).size)]

        self.current_state = 0

    def get_holes(self):
        return self.index_hole

    def get_action_space(self):
        return self.action_space

    def get_state_space(self):
        return self.state_space

    def get_random_action(self):
        return np.random.choice(self.action_space)

    def step(self, action_index):  # take an action and return the next state, reward, and done
        action = Action(action_index)

        if self.invalid_action(action):  # if the action is invalid, return the current state, -10, and done
            return self.current_state, -10 * self.SIZE * self.SIZE, False

        if action == Action.Left:
            self.current_state -= 1
        elif action == Action.Right:
            self.current_state += 1
        elif action == Action.Up:
            self.current_state -= self.SIZE
        else:
            self.current_state += self.SIZE

        letter = self.map[self.current_state]

        if letter == 'S':  # if the next state is the start state, return the current state, -10, and done
            return self.current_state, -10 * self.SIZE * self.SIZE, False
        if letter == 'F':  # if the next state is a frozen state, return the current state, -1, and done
            return self.current_state, -self.SIZE, False
        elif letter == 'G':  # if the next state is the goal state, return the current state, 100, and done
            return self.current_state, 100 * self.SIZE * self.SIZE, True
        else:  # if the next state is a hole, return the current state, -10, and done
            return self.current_state, -10 * self.SIZE * self.SIZE, True

    def valid_actions_of_state(self, state=None):
        if not state:
            state = self.current_state
        valid_actions = []
        for action in self.action_space:
            if not self.invalid_action_of_state(action, state):
                valid_actions.append(action)
        return valid_actions

    def invalid_action_of_state(self, action, state):
        if (action == Action.Left and state % self.SIZE == 0) or \
                (action == Action.Right and state % (self.SIZE) == (self.SIZE - 1)) or \
                (action == Action.Up and state < self.SIZE) or \
                (action == Action.Down and (
                        self.SIZE * self.SIZE - self.SIZE) <= state <= self.SIZE * self.SIZE - 1):
            return True

        return False
    # def invalid_action(self, action):
    #     if (action == Action.Left and self.current_state % self.SIZE == 0) or \
    #             (action == Action.Right and self.current_state % (self.SIZE) == (self.SIZE - 1)) or \
    #             (action == Action.Up and self.current_state < self.SIZE) or \
    #             (action == Action.Down and (
    #                     self.SIZE * self.SIZE - self.SIZE) <= self.current_state and self.current_state <= self.SIZE * self.SIZE - 1):
    #         return True
    #
    #     return False
    # def valid_actions(self, state):
    #     valid_actions = []
    #     for action in self.action_space:
    #         if not self.invalid_action(action):
    #             valid_actions.append(action)
    #     return valid_actions

    def probabiltyOfNextState(self, action, probabilityOfStep):
        """
        take an action and return the next state, reward, and done
        :param action:
        :param probabilityOfStep:
        :return:
        """
        validActions = self.valid_actions_of_state()
        if np.random.uniform(0, 1) < probabilityOfStep or (len(validActions) == 1 and validActions[0] == action):
            return action
        if action in validActions:
            validActions.remove(action)
        return np.random.choice(validActions)

    def stochastic_step(self, action_index, probabilityOfStep):
        """
        take an action in a certein and return the next state, reward, and done
        :param action_index:
        :param probabilityOfStep:
        :return:
        """
        action = Action(action_index)
        action = self.probabiltyOfNextState(action, probabilityOfStep)
        state, reward, done = self.step(action.value)
        return state, reward, done, action.value

    def reset(self):
        self.current_state = 0
        return self.current_state

    def print_current_state(self):
        temp_map = deepcopy(self.map)
        for i in range(0, self.SIZE * self.SIZE):
            if self.current_state != i:
                if temp_map[i] == 'F':
                    print('.', end=" ")
                if temp_map[i] == 'H':
                    print('O', end=" ")
                if temp_map[i] == 'G':
                    print('G', end=" ")
                if temp_map[i] == 'S':
                    print('S', end=" ")
            else:
                print('X', end=" ")
            if i % self.SIZE == (self.SIZE - 1):
                print()
        print()
        print()
