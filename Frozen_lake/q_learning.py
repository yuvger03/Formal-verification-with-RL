

import numpy as np
import random
import time
from utils import runSmv, writeSmv, writePrism, runPrism
import parameters_run

#self.SIZE=parameters_run.get_self.SIZE()
#from environment import self.SIZE
# probability = 0.99
class Q_Learning:

    def __init__(self, environment,learning_rate,discount_rate,probability, **parameters):
        self.SIZE=parameters_run.get_size()
        self.env = environment

        self.num_episodes = parameters.get('num_episodes', self.SIZE*1000)
        self.max_steps_per_episode = parameters.get('max_steps_per_episode', self.SIZE*self.SIZE)
        self.learning_rate = parameters.get('learning_rate', learning_rate)
        self.discount_rate = parameters.get('discount_rate', discount_rate)
        self.exploration_rate = parameters.get('exploration_rate', 1)
        self.max_exploration_rate = parameters.get('max_exploration_rate', 1)
        self.min_exploration_rate = parameters.get('min_exploration_rate', 0.01)
        self.exploration_decay_rate = parameters.get('exploration_decay_rate', 0.0001)

        self.bigChange=0
        self.epsilon=10e-30
        self.episodes=0

        self.q_table = np.zeros((len(environment.get_state_space()), len(environment.get_action_space())))
        self.all_episode_rewards = []
        self.useNusmv=parameters_run.get_useNusmv()

        self.probability = probability
        self.probs = np.zeros((len(environment.get_state_space()), len(environment.get_action_space())))

    def getQ(self):
        return self.q_table

    def update_probs(self, probability, row):  # get the probability matrix according to the q_table
        valid_actions = [action.value for action in self.env.valid_actions_of_state(row)]  # get the valid actions
        best_action = valid_actions[np.argmax(self.q_table[row, valid_actions])]  # get best valid action from q_table
        valid_actions.remove(best_action)  # remove the best action from the valid actions
        self.probs[row, :] = 0  # reset the row
        self.probs[row, best_action] = probability  # the best action gets our probability
        # the other actions get the rest of the probability (1-p)/(num_actions-1)
        self.probs[row, valid_actions] = (1 - probability) / (len(valid_actions))

    def setuseNusmv(self,value):
         self.useNusmv=value
    def run_algorithm(self,probability,index):
        #FLAG_win shows wheter smv found a solution or not and what solution
        FLAG_win=False
        #maxSteps shows which number of steps we need to take to win
        maxSteps=self.SIZE*self.SIZE+1

        finalanswer=[]
        run_prism_index = 0

        for episode in range(self.num_episodes):
            rewards_for_current_episode = 0
            state = self.env.reset()

            old_q=self.q_table.copy()
            for step in range(self.max_steps_per_episode):
                rand = random.uniform(0, 1)
                if rand < self.exploration_rate:
                    action_index = self.env.get_random_action().value
                else:
                    action_index = np.argmax(self.q_table[state, :])

                new_state, reward, done = self.env.step(action_index)
                # new_state, reward, done = self.env.stocastic_step(action_index, probability)

                # update the q_table and prob matrix accordingly
                self.q_table[state][action_index] = self.q_table[state][action_index] * (1 - self.learning_rate) + \
                                                    self.learning_rate * \
                                                    (reward + self.discount_rate * np.max(self.q_table[new_state, :]))

                self.update_probs(probability, state)

                state = new_state
                rewards_for_current_episode += reward              

                if done:
                    break

            self.exploration_rate = self.min_exploration_rate + \
                                    (self.max_exploration_rate - self.min_exploration_rate) * np.exp(
                -self.exploration_decay_rate * episode)

            self.all_episode_rewards.append(rewards_for_current_episode)
            
            if episode%2000==0:
                print("we are in episode", episode)


            if episode%100==0 and episode>0 and self.useNusmv==1:
                writeSmv(self.SIZE, maxSteps ,self.q_table, self.env.get_holes(),index= index)
                answer=runSmv(index)

                if not answer[1]:
                    self.q_table[answer[2]][answer[3]]= self.q_table[answer[2]][answer[3]]-1000
                    self.update_probs(probability, answer[2])
                    print(answer[0])
                    print(answer[1])
                    print(answer[2])
                    print(answer[3])

                if answer[1]:
                    print("found something ", len(answer[0]))
                    FLAG_win=True
                    maxSteps=len(answer[0])

                    #print(answer[0])
                    for i in range(len(answer[0])-1):
                        n_state=answer[0][i]
                        new_state=answer[0][i+1]

                        #left
                        if int(new_state)-int(n_state)==int(-1):
                            action_index=0
                        #right
                        elif int(new_state)-int(n_state)==int(1):
                            action_index=1
                        #up
                        elif int(new_state)-int(n_state)==-self.SIZE:
                            action_index=2
                        #down
                        elif int(new_state)-int(n_state)==self.SIZE:
                            action_index=3

                        self.q_table[int(n_state)][action_index] = self.q_table[int(n_state)][action_index] * (1 - self.learning_rate) + \
                                                            self.learning_rate * (
                                                                    reward + self.discount_rate * np.max(
                                                                self.q_table[int(new_state), :]))+10*self.SIZE*self.SIZE

                        self.update_probs(probability, int(n_state))
                        writePrism(self.SIZE, maxSteps, self.q_table, self.env.get_holes(), index=index, probs=self.probs)
                        runPrism(index, f'tests/nuxmv_prism_results_{index}.csv')
                #lose

                if FLAG_win and answer[2]==0 and answer[3]==0:
                    #print("dead")
                    print(finalanswer)
                    print("length of answer ", len(finalanswer))
                    #break
                if answer[1]:
                    maxSteps=len(answer[0])-1
                    FLAG_win=True
                    finalanswer=answer[0]

            if episode % 100 == 0 and episode > 0 and self.useNusmv==0:  # not using nusmv - just run prism
                writePrism(self.SIZE, maxSteps, self.q_table, self.env.get_holes(), index=index, probs=self.probs)
                runPrism(index, f'tests/no_nuxmv_prism_results_{index}.csv')


            #print(answer)
            #find convergence
            self.bigChange = np.ndarray.max(np.abs(np.subtract(old_q, self.q_table)))
            self.episodes = self.episodes + 1
            if self.bigChange <= self.epsilon:
                break

    def print_results(self,index):
        print('big Change')
        print('{:010.10f}'.format(self.bigChange))
        print('Episodes')
        print(self.episodes)
        writeSmv(self.SIZE, 10000 ,self.q_table, self.env.get_holes(),index= index)
        answer=runSmv(index)

        if answer[1]:
         print("found something ", len(answer[0]))
         print(answer[0])


        print('Q-Table')
        self.x = print(self.q_table)
        print('-------------------------------------')

        # Calculate and print the average reward per thousand episodes
        avg_reward=sum(self.all_episode_rewards) / self.episodes

        print("Average reward:")
        print(avg_reward)
        print()

    def run_and_print_latest_iteration(self,probability):
        state = self.env.reset()

        for step in range(self.max_steps_per_episode):
            #self.env.print_current_state()
            #time.sleep(1)
            action_index = np.argmax(self.q_table[state, :])
            # new_state, _, done = self.env.step(action_index)
            new_state, _, done = self.env.stocastic_step(action_index,probability)
            state = new_state

            if done and state==self.SIZE*self.SIZE-1:
                print('The agent has reached the goal!!!')
                return 1,self.episodes
            if done:
              break
        return 0,self.episodes