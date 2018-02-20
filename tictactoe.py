def play_game(p1, p2, env, draw=False):
	current_player = None
	while not env.game_over():
		#alternate players	
		if current_player == p1:
			current_player = p2
		else:
			current_player = p1
		
		#not sure what representation ill use
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

		#do the value function update	
		p1.update()
		p2.update()	


class Agent():

	def __init__(self, aid):
		self.aid = aid
		self.mean = 0
		self.count = 1
		self.learning_rate = 0.01
		self.statesTaken = []
		self.values = {}

	def take_action(self, env):
		"""take action based on egreedy method """
		self.count += 1
		maxValue = 0
		selectedAction = None
		possibleNextStates = env.possible_next_states(self.aid)
		
		if 1/self.count > np.random.rand():
			selectedAction, randState = np.random.choice(list(possibleNextStates.items()))
		else:	
			for action, nextState in possibleNextStates.items():
				value = self.values[nextState]
				if value > maxValue:
					maxValue = value
					selectedAction = action
		
		env.perform_action(self.aid, selectedAction)
		

	def find_final_state(self, state):
		"""detect a final state and the type of it """
		tempState = np.fromstring(state, np.int8) - 48
		tempState = np.reshape((3, 3))

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
		else:
			return 0	

	def update_state_history(self, state):
		""" add states taken to state history """
		self.statesTaken.append(state)
		findFinalState = self.find_final_state(state)

		if state not in self.values:
			if findFinalState == self.aid:
				self.values[state] = 1
			elif findFinalState != 0 and findFinalState != self.aid:
				self.values[state] = 0
			else:	
				self.values[state] = 0.5
			
	
	def update(self, env):
		"""update states backward """
				
		for state, nextState in zip(self.statesTaken[:-1][::-1], self.statesTaken[1:][::-1]):
			self.values[state] += learning_rate * (self.values[state] - self.values[nextState])



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
		tempState = np.reshape((3, 3))

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

	def possible_next_states(self, aid):
		"""gives information about the next states for the agent """
		tempState = list(self.actualState)
		tempState2 = tempState
		action = 0
		for pos, word in enum(tempState):
			if word == '0':
				tempState2[pos] = str(aid)
				self.possible_next_states[action] = ''.join(tempState2)
				tempState2 = tempState
				action += 1
		return self.possible_next_states		

		

	def perform_action(self, action):
		"""implement selected state """
		self.actualState = self.possible_next_states[action]
				




