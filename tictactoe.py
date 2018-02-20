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
		self.count = 0
		self.statesTaken = []
		self.values = {}

	def take_action(self, env):
		"""take action based on egreedy method """
		maxValue = 0
		selectedAction = None
		possibleNextStates = np.random.shuffle(env.possible_next_states())
		
		if 1/self.count > np.random.rand():
			selectedAction, randState = possibleNextStates
		else:	
			for action, nextState in possibleNextStates:
				value = self.values[nextState]
				if value > maxValue:
					maxValue = value
					selectedAction = action
		
		env.perform_action(selectedAction)
		

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
		self.count += 1.0
		
		for state, nextState in zip(self.statesTaken[:-1][::-1], self.statesTaken[1:][::-1]):
			self.values[state] += 1/self.count * (self.values[state] - self.values[nextState])



class Eviroment():
	"""game class """
	def __init__(self):
		self.actualState = None


	def game_over(self):
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

	def possible_next_states(self):
		

	def perform_action(self, action):
				




