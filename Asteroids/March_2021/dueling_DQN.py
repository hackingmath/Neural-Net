"""From Reinforcement Learning with Pytorch Udemy course
Feb 28, 2021"""

import torch
import torch.nn as nn
import torch.optim as optim
from game_move import Game
#from game import Game
#from game_no_graphics import Game
import random
import math
import time
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np
from torch.autograd import Variable

#if gpu is to be used
use_cuda = torch.cuda.is_available()
device = torch.device("cuda:0" if use_cuda else "cpu")
Tensor = torch.Tensor
LongTensor = torch.LongTensor

env = Game() #gym.make("CartPole-v0")
seed_value = 23
#env.seed(seed_value)
torch.manual_seed(seed_value)
random.seed(seed_value)

#####PARAMS#######
learning_rate = 0.03
NUM_EPISODES = 200
gamma = 0.9999
replay_memory_size = 50000
batch_size = 32

update_target_frequency = 50
double_dqn = True

hidden_layer1 = 64
#hidden_layer2 = 32
egreedy = 0.9
egreedy_final = 0.01
egreedy_decay = 200

score_to_solve=1000
clip_error = False
##################

number_of_inputs = 8#env.observation_space.shape[0]
number_of_outputs = 4#env.action_space.n

def calculate_epsilon(steps_done):
    epsilon = egreedy_final + (egreedy - egreedy_final) * \
        math.exp(-1. * steps_done / egreedy_decay)
    return epsilon

class ExperienceReplay(object):
    def __init__(self,capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0 #track entries pushed into memory

    def push(self,state,action,new_state,reward,done):
        transition = (state,action,new_state,reward,done)
        if self.position >= len(self.memory):
            self.memory.append(transition)
        else:
            self.memory[self.position] = transition
        self.position = ( self.position + 1) % self.capacity

    def sample(self,batch_size):
        """Puts all states together, all actions together..."""
        return zip(*random.sample(self.memory,batch_size))

    def __len__(self):
        return len(self.memory)

class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork,self).__init__()
        self.linear1 = nn.Linear(number_of_inputs,hidden_layer1)
        self.advantage = nn.Linear(hidden_layer1,number_of_outputs)
        self.value = nn.Linear(hidden_layer1, 1)
        #self.linear3 = nn.Linear(hidden_layer2,number_of_outputs)
        self.activation = nn.Tanh()
        #self.activation = nn.ReLU()

    def forward(self,x):
        output1 = self.linear1(x)
        output1 = self.activation(output1)
        output_advantage = self.advantage(output1)
        output_value = self.value(output1)
        #output2 = self.activation(output2)
        #output3 = self.linear3(output2)
        output_final = output_value + output_advantage - output_advantage.mean()
        return output_final

class QNet_Agent(object):
    def __init__(self):
        self.nn = NeuralNetwork().to(device)
        self.target_nn = NeuralNetwork().to(device)
        self.loss_func = nn.MSELoss()
        self.optimizer = optim.Adam(params=self.nn.parameters(),lr=learning_rate)
        self.update_target_counter = 0

    def select_action(self,state,epsilon):

        if torch.rand(1)[0] > epsilon:
            with torch.no_grad():
                state = torch.tensor(state,dtype=torch.float32).to(device)
                action_from_nn = self.nn(state)
                action = torch.max(action_from_nn,0)[1]
                action = action.item()
        else:
            action = random.choice(list(range(number_of_outputs)))#env.action_space.sample()
        return action

    def optimize(self):
        if len(memory) < batch_size:
            return
        state, action, new_state, reward, done = memory.sample(batch_size)
        #print("state:",len(state),type(state),state)
        #print("action:", len(action), action)
        state= torch.tensor(state,dtype=torch.float32)#Tensor(state).to(device)#
        new_state = Tensor(new_state).to(device)
        action = LongTensor(action).to(device)
        done = Tensor(done).to(device)
        reward = Tensor(reward).to(device)

        if double_dqn:
            new_state_indexes = self.nn(new_state).detach()
            max_new_state_indexes = torch.max(new_state_indexes, 1)[1]

            new_state_values = self.target_nn(new_state).detach()
            max_new_state_values = new_state_values.gather(1,max_new_state_indexes.unsqueeze(1)).squeeze(1)

        else:
            new_state_values = self.target_nn(new_state).detach()
            max_new_state_values = torch.max(new_state_values,1)[0]
        #if 1 in done: target value is just reward
        target_value = reward + (1-done) * gamma * max_new_state_values

        predicted_value = self.nn(state).gather(1,action.unsqueeze(1)).squeeze(1) #calculate gradient
        loss = self.loss_func(predicted_value,target_value)
        self.optimizer.zero_grad()
        loss.backward()
        if clip_error:
            for param in self.nn.parameters():
                param.grad.data.clamp(-1,1)
        self.optimizer.step()

        if self.update_target_counter % update_target_frequency == 0:
            self.target_nn.load_state_dict(self.nn.state_dict())

        self.update_target_counter += 1

        #Q[state,action] = reward+gamma*torch.max(Q[new_state])

memory = ExperienceReplay(replay_memory_size)
qnet_agent = QNet_Agent()
report_interval = 10
steps_total = []
frames_total = 0
high_score = 0
scores = []
mean_100s = list()
num_scores = 0
solved_after = 0
solved = False
start_time = time.time()

for i_episode in range(1,NUM_EPISODES+1):
    state = env.reset()
    step = 0
    while True:
        step += 1
        frames_total += 1
        epsilon = calculate_epsilon(step)
        action = qnet_agent.select_action(state,epsilon)
        #print("epsilon:",epsilon)
        new_state,reward,done, score=env.play_frame(action)
        #print(new_state,reward,done,score)
        if score > high_score:
            high_score = score

        #scores.append(score)
        #num_scores += 1
        memory.push(state,action,new_state,reward,done)
        #print(f"frame{frames_total}")
        qnet_agent.optimize()
        state = new_state
        if done:
            scores.append(score)
            steps_total.append(step)
            mean_reward_100 = sum(scores[-100:])/100
            mean_100s.append(mean_reward_100)
            if mean_reward_100 > score_to_solve and not solved:
                print(f"SOLVED! After {i_episode} episodes.")
                solved_after = i_episode
                solved = True

            if i_episode % report_interval == 0:
                print("\n***Episode %i *** \
\                      \nAv.scores: [last %i]: %.2f,[last 100]: %.2f, [all]: %.2f \
                        \nepsilon: %.2f, frames_total: %i, last score: %i, high score: %i"
                      %
                      (i_episode,
                       report_interval,
                       sum(scores[-report_interval:])/report_interval,
                       mean_reward_100,
                       sum(scores)/len(scores),
                       epsilon,
                       frames_total,
                       score,high_score)
                      )
                elapsed_time = time.time() - start_time
                print("Elapsed time:",time.strftime("%H:%M:%S",time.gmtime(elapsed_time)))
            break

print("Average Steps: {0}".format(sum(steps_total)/NUM_EPISODES))
print("Average Steps (last 100 episodes): {0}".format(sum(steps_total[-100:])/100))

if solved:
    print(f"Solved after {solved_after} episodes")
plt.figure(figsize=(12,5))
plt.title("Scores")
plt.bar(torch.arange(i_episode),mean_100s,alpha=0.6,color='green', width=5)
plt.show()


"""
March 24:
***Episode 380 *** \                      
Av.scores: [last 10]: 5136.00,[last 100]: 5103.60, [all]: 2972.48                         
epsilon: 0.01, frames_total: 320998, last score: 5240, high score: 11520
Elapsed time: 01:43:23


"""