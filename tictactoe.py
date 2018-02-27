import numpy as np
import random
def play_game(p1, p2, env, ep, draw=False):
	current_player = None 
	# random.choice((p1, p2))
	gameState = 0
	while not gameState:
		#alternate players	
		if current_player == p1:
			current_player = p2
		else:
			current_player = p1
		
		
		if draw:
			if draw == 1 and current_player == p1:
				env.draw_board()
			if draw == 2 and current_player == p2:
				env.draw_board()	

		#actual action		
		current_player.take_action(env)		
		#next state from that action
		state = env.get_state()
		#save states for episode
		p1.update_state_history(state)
		p2.update_state_history(state)
		
		#not sure about it yet 
		if draw:
			env.draw_board()

		#get final game state 
		gameState = env.game_over()
			
		#do the value function update	
		p1.update(gameState)
		p2.update(gameState)	

		

	print("----------------------------------------------------------")
	if gameState == 1:
		print("End of episode: " + str(ep) + ", player 1 wins")
	elif gameState == 2:
		print("End of episode: " + str(ep) + ", player 2 wins")
	else:
		print("End of episode: " + str(ep) + ", draw end")	  		
	print("----------------------------------------------------------")	

class Agent():

	def __init__(self, aid, train = True):
		self.aid = aid
		self.mean = 0
		self.eps = 0.1
		self.learning_rate = 0.5
		self.statesTaken = []
		self.values = {}
		self.train = train

	def take_action(self, env):
		"""take action based on egreedy method """
		#self.count += 1.0
		actionValue = []
		possibleNextStates = env.get_next_states(self.aid)
		
#		if 1.0/self.count > np.random.rand():
		#get better exploration
		if ((self.eps > np.random.rand()) and self.train):	
			selectedAction, randState = random.choice(list(possibleNextStates.items()))
		else:	
			for action, nextState in possibleNextStates.items():
				findFinalState = self.find_final_state(nextState)
				self.is_state_in_values(findFinalState, nextState)
				value = self.values[nextState]
				actionValue.append((value, action))
			selectedAction = max(actionValue)[1]	
		
		env.perform_action(selectedAction)
		

	def find_final_state(self, state):
		"""detect a final state and the type of it """
		tempState = np.fromstring(state, np.int8) - 48
		tempState = tempState.reshape((3, 3))

		if ((tempState == 1).all(0).any() or 
			(tempState == 1).all(1).any() or 
			(tempState == 1).diagonal().all() or 
			np.rot90((tempState == 1)).diagonal().all()):
			return 1
		elif ((tempState == 2).all(0).any() or 
			(tempState == 2).all(1).any() or 
			(tempState == 2).diagonal().all() or 
			np.rot90((tempState == 2)).diagonal().all()):	
			return 2
		elif tempState.all():
			return 3	
		else:
			return 0	

	def update_state_history(self, state):
		""" add states taken to state history """
		self.statesTaken.append(state)
		findFinalState = self.find_final_state(state)
		self.is_state_in_values(findFinalState, state)

	def is_state_in_values(self, findFinalState, state):	
		if state not in self.values:
			if findFinalState == self.aid:
				self.values[state] = 1
			elif (findFinalState != 0 and 
				findFinalState != self.aid and 
				findFinalState != 3):
				self.values[state] = -1
			elif findFinalState == 3:
				self.values[state] = 0
			else:	
				self.values[state] = 0.5
			
	
	def update(self, gameState):
		"""update states backward just and the end of an episode """
		if gameState:		
			for state, nextState in zip(self.statesTaken[:-1][::-1], self.statesTaken[1:][::-1]):
				self.values[state] += self.learning_rate * (self.values[state] - self.values[nextState])



class Eviroment():
	"""game class """
	def __init__(self):
		self.actualState = "000000000"
		self.possible_next_states = {}

	def game_over(self):
		"""define the end of the game, also reset the next possible states
		every turn to get the new possible states """
		self.possible_next_states = {}
		tempState = np.fromstring(self.actualState, np.int8) - 48
		tempState = tempState.reshape((3, 3))
		

		if ((tempState == 1).all(0).any() or 
			(tempState == 1).all(1).any() or 
			(tempState == 1).diagonal().all() or 
			np.rot90((tempState == 1)).diagonal().all()):
			self.actualState = "000000000"
			return 1
		elif ((tempState == 2).all(0).any() or 
			(tempState == 2).all(1).any() or 
			(tempState == 2).diagonal().all() or 
			np.rot90((tempState == 2)).diagonal().all()):	
			self.actualState = "000000000"
			return 2
		elif tempState.all():
			self.actualState = "000000000"
			return 3	
		
		else:
			return 0

	def get_next_states(self, aid):
		"""gives information about the next states for the agent """
		tempState = list(self.actualState)
		tempState2 = list(tempState)
		action = 0
		for pos, word in enumerate(self.actualState):
			if word == '0':
				tempState2[pos] = str(aid)
				self.possible_next_states[action] = ''.join(tempState2)
				tempState2 = list(tempState)
				action += 1
		
		return self.possible_next_states		

		
	def perform_action(self, action):
		"""implement selected state """
		nextState = self.possible_next_states[action]
		print(nextState)
		self.actualState = nextState

	def perform_human_action(self, nextState):
		print(nextState)
		self.actualState = nextState	

	def get_state(self):
		return self.actualState 

	def draw_board(self):
		"""not implemented yet """		
				
#make human agent
class Human():
	"""human agent to play against the trained AI """
	def __init__(self, aid = 2):
		self.aid = aid

	def make_move(self, env, posX, posY):
		state = list(env.get_state())
		state[posX * 3 + posY] = str(self.aid)
		state = ''.join(state)	
		env.perform_human_action(state)

if __name__ == "__main__":

	env = Eviroment()
	player1 = Agent(1)
	player2 = Agent(2)

	for i in range(100000):

		play_game(player1, player2, env, i)




			