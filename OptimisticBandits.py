import numpy as np
from operator import itemgetter

class Bandit():
	
	def __init__(self, initVal = 0, trueM = 0, bid = 0):
		self.mean = initVal
		self.trueM = trueM
		self.id = bid
		self.count = 0
		self.actionCount = 0.001

	def pull(self):
		self.actionCount = self.actionCount + 1
		return np.random.randn() + self.trueM	
		
	def update(self, reward):
		self.count = self.count + 1
		self.mean = (1.0 - 1.0/self.count)*self.mean + 1.0/self.count*reward

	def UCB1bound(self, iteration):
		ucb1Bound = self.mean + np.sqrt(2*np.log(iteration)/self.actionCount)
		return ucb1Bound
		
def optimisticBandit():
	bandits = [Bandit(10, i ,i) for i in range(1, 5)]
	totalReward = 0
	for i in range(1, 1000000):
		means = [(bandit.mean, bandit.id) for bandit in bandits]
		means.sort(key=itemgetter(0), reverse = True)
		for bandit in bandits:
			if bandit.id == means[0][1]:
				reward = bandit.pull()
				totalReward = totalReward + reward
				bandit.update(reward)
	for bandit in bandits:
		print(bandit.mean)	
	print(totalReward)			

def UCB1Bandit():
	bandits = [Bandit(10, i ,i) for i in range(1, 5)]
	totalReward = 0
	for i in range(1, 1000000):
		ucb1Bounds = [(bandit.UCB1bound(i), bandit.id) for bandit in bandits]
		ucb1Bounds.sort(key=itemgetter(0), reverse = True)
		for bandit in bandits:
			if bandit.id == ucb1Bounds[0][1]:
				reward = bandit.pull()
				totalReward = totalReward + reward
				bandit.update(reward)
	for bandit in bandits:
		print(bandit.mean)	
	print(totalReward)		

def eGreedyBandit():
	bandits = [Bandit(0, i ,i) for i in range(1, 5)]
	totalReward = 0
	
	for i in range(1, 1000000):
		epsilon = 1.0/(i+1)
		if epsilon > np.random.rand():
			randBandit = np.random.choice(bandits)
			reward = randBandit.pull()
			randBandit.update(reward)
		else:       
			means = [(bandit.mean, bandit.id) for bandit in bandits]
			means.sort(key=itemgetter(0), reverse = True)
			for bandit in bandits:
				if bandit.id == means[0][1]:
					reward = bandit.pull()
					bandit.update(reward)
		totalReward = totalReward + reward
		
	for bandit in bandits:
		print(bandit.mean)	
	print(totalReward)			
	

if __name__ == "__main__":
	print("optimistic bandits: ")
	optimisticBandit()
	print("ucb1 bandits: ")
	UCB1Bandit()
	print("e greedy bandits: ")
	eGreedyBandit()