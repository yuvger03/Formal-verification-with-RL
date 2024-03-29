import numpy as np
import random
from utils import runSmv, writeSmv, writePrism, runPrism
import parameters_run


class Q_Learning:

    def __init__(self, environment, probability=1.0, index=1, PR=None, **parameters):
        self.PR = PR
        self.env = environment
        self.index = index
        self.num_episodes = parameters.get('num_episodes', PR.size * 1000)
        self.max_steps_per_episode = parameters.get('max_steps_per_episode', PR.num_steps_in_episode)
        self.learning_rate = parameters.get('learning_rate', 0.1)
        self.discount_rate = parameters.get('discount_rate', 0.99)
        self.exploration_rate = parameters.get('exploration_rate', 0)
        self.max_exploration_rate = parameters.get('max_exploration_rate', 0)
        self.min_exploration_rate = parameters.get('min_exploration_rate', 0.0)
        self.exploration_decay_rate = parameters.get('exploration_decay_rate', 0.0001)
        self.bigChange = 0
        self.epsilon = 0.0000000000000000000000000001
        self.episodes = 0
        self.q_table = np.zeros((len(environment.get_state_space()), len(environment.get_action_space())))
        self.all_episode_rewards = []
        self.useNusmv = PR.get_useNusmv()
        self.probability = probability
        self.res_file_name = PR.get_file_name()
        self.probs = np.zeros((len(environment.get_state_space()), len(environment.get_action_space())))

    def update_probs(self, probability, row):
        """
        get the probability matrix according to the q_table
        :param probability:
        :param row:
        :return:
        """
        valid_actions = [action.value for action in self.env.valid_actions_of_state(row)]  # get the valid actions
        best_action = valid_actions[np.argmax(self.q_table[row, valid_actions])]  # get best valid action from q_table
        valid_actions.remove(best_action)  # remove the best action from the valid actions
        self.probs[row, :] = 0  # reset the row
        self.probs[row, best_action] = probability  # the best action gets our probability
        # the other actions get the rest of the probability (1-p)/(num_actions-1)
        self.probs[row, valid_actions] = ((1 - probability) / (len(valid_actions)) if len(valid_actions) > 0 else 0)

    def getQ(self):
        return self.q_table

    def setuseNusmv(self, value):
        self.useNusmv = value

    def run_algorithm(self, index=1):
        """
        run the q-learning algorithm
        :param index:
        :return:
        """
        # FLAG_win shows wheter smv found a solution or not and what solution
        FLAG_win = False
        # maxSteps shows which number of steps we need to take to win 
        maxSteps = self.PR.size * self.PR.size + 1

        finalAnswer = []

        for episode in range(self.num_episodes):
            rewards_for_current_episode = 0
            state = self.env.reset()

            old_q = self.q_table.copy()
            for step in range(self.max_steps_per_episode): # for each step in the episode
                rand = random.uniform(0, 1)
                if rand < self.exploration_rate or self.q_table[state, 0] == self.q_table[state, 1]:
                    action_index = self.env.get_random_action().value
                else:
                    action_index = np.argmax(self.q_table[state, :])

                # new_state, reward, done = self.env.step(action_index)
                new_state, reward, done, action_index = self.env.stochastic_step(action_index, self.probability)
                # get the new state, reward and done from the environment

                self.q_table[state][action_index] = self.q_table[state][action_index] * (1 - self.learning_rate) + \
                                                    self.learning_rate * (
                                                            reward + self.discount_rate * np.max(
                                                        self.q_table[new_state, :]))
                self.update_probs(self.probability, state)

                state = new_state
                rewards_for_current_episode += reward

                if done:
                    break

            self.exploration_rate = self.min_exploration_rate + \
                                    (self.max_exploration_rate - self.min_exploration_rate) * np.exp(
                -self.exploration_decay_rate * episode)

            self.all_episode_rewards.append(rewards_for_current_episode)

            if episode % 2000 == 0:
                print("we are in episode", episode)

            if (episode % 2000 == 0) and episode > 0 and self.useNusmv == 1:
                writeSmv(self.PR.size, maxSteps, self.q_table, self.env.get_holes(), index=index, PR=self.PR)
                answer = runSmv(index=index, PR=self.PR)

                if answer[1]: # if we found a solution
                    print("found something ", len(answer[0]))  # print the solution
                    FLAG_win = True
                    maxSteps = len(answer[0])

                    print(answer[0])
                    for i in range(len(answer[0]) - 1):
                        n_state = answer[0][i]
                        new_state = answer[0][i + 1]

                        # left
                        if int(new_state) - int(n_state) == int(-1):
                            action_index = 0
                        # right
                        elif int(new_state) - int(n_state) == int(1):
                            action_index = 1

                        self.q_table[int(n_state)][action_index] = self.q_table[int(n_state)][action_index] * (
                                1 - self.learning_rate) + \
                                                                   self.learning_rate * (
                                                                           reward + self.discount_rate * np.max(
                                                                       self.q_table[int(new_state),
                                                                       :])) + 10000000 * self.PR.size * self.PR.size
                        self.update_probs(self.probability, int(n_state))
                writePrism(self.PR.size, maxSteps, self.q_table, self.env.get_holes(), index, p=self.probability,
                           probs=self.probs, useNuxmv=self.useNusmv, PR=self.PR)
                runPrism(index, self.res_file_name, PR=self.PR)
                # lose

                if FLAG_win and answer[2] == 0 and answer[3] == 0: # if we found a solution and it is not a dead end
                    # print("dead")
                    print(finalAnswer)
                    print("length of answer ", len(finalAnswer))
                    # break
                if answer[1]:
                    maxSteps = len(answer[0]) - 1
                    FLAG_win = True
                    finalAnswer = answer[0]

            if episode % 100 == 0 and episode > 0 and self.useNusmv == 0:  # not using nusmv - just run prism
                writePrism(self.PR.size, maxSteps, self.q_table, self.env.get_holes(), index=index, p=self.probability,
                           probs=self.probs, useNuxmv=self.useNusmv, PR=self.PR)
                runPrism(index, self.res_file_name, PR=self.PR)
            # print(answer)
            # find convergence
            self.bigChange = np.ndarray.max(np.abs(np.subtract(old_q, self.q_table)))
            self.episodes = self.episodes + 1
            if self.bigChange <= self.epsilon:
                break

    def print_results(self):
        print('big Change')
        print('{:010.10f}'.format(self.bigChange))
        print('Episodes')
        print(self.episodes)
        writeSmv(self.PR.size, 10000, self.q_table, self.env.get_holes(), index=self.index, PR=self.PR)
        answer = runSmv(self.index, self.PR)
        writePrism(self.PR.size, 10000, self.q_table, self.env.get_holes(), index=self.index, p=self.probability,
                   probs=self.probs, useNuxmv=self.useNusmv, PR=self.PR)
        runPrism(self.index, self.res_file_name, PR=self.PR)

        if answer[1] == True:
            print("found something ", len(answer[0]))
            print(answer[0])

        print('Q-Table')
        print(self.q_table)
        print('-------------------------------------')

        # Calculate and print the average reward per thousand episodes
        avg_reward = sum(self.all_episode_rewards) / self.episodes

        print("Average reward:")
        print(avg_reward)
        print()

    def run_and_print_latest_iteration(self):
        """
        run the latest iteration of the q-learning algorithm
        :return:
        """
        state = self.env.reset()
        for step in range(100):
            # self.env.print_current_state()

            action_index = np.argmax(self.q_table[state, :])
            new_state, _, done, _ = self.env.stochastic_step(action_index, self.probability)
            # new_state, _, done = self.env.step(action_index)
            state = new_state

            if done:
                print('The agent has reached the goal!!!')
                return 1

        return 0
