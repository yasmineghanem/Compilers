from graphviz import Digraph

# Each state has a list of transitions and epsilon transitions
# We have 2 types of states accepting and non accepting
class State:
    # id = 0 # Smarter than using index in NFA
    def __init__(self, name, start=False, accepting=True, transitions=[], parents=[]):
        # self.id = State.id
        # State.id += 1
        self.name = name
        self.transitions = []
        self.parents = []
        self.accepting = accepting
        self.start = start

    def add_transition(self, transition, state):
        self.transitions.append((transition, state))
        state.parents.append(self)
        self.accepting = False

    def get_transitions(self):
        return self.transitions.copy()

    def get_parents(self):
        return self.parents.copy()


# NFA class
	# Consists of
		# 1. States ( eaach has its transitions and epsilon transitions)
		# 2. Start State
		# 3. Final State			 

	# Operations that can be done on them
		# 1. Concatenation
		# 2. Union
		# 3. Kleene Star
		# 4. Positive Closure

class NFA:
	def __init__(self, start_state=None, accept_state=None, regex=None):
		self.start_state = start_state
		self.accept_state = accept_state
		if not start_state and not accept_state and regex:
			nfa = self.create_nfa(regex)
			self.start_state = nfa.start_state
			self.accept_state = nfa.accept_state

	def create_nfa(self, regex):
		"""
		Converts a regular expression in postfix notation to an NFA.
		"""
		NFAStack, index = [], 0

		for symbol in regex:
			if symbol == '.':  # Concatenation
				# Pop the operands
				nfa2 = NFAStack.pop()
				nfa1 = NFAStack.pop()
				#Concatenate with an epsilon transition
				nfa1.accept_state.add_transition('ϵ', nfa2.start_state)
				# Add to NFA Stack output
				NFAStack.append(NFA(nfa1.start_state, nfa2.accept_state))

			elif symbol == '|':  # Union
				# Pop the operands
				nfa2 = NFAStack.pop()
				nfa1 = NFAStack.pop()
				# we have a start and an end (between which we put the symbols)
				start = State("S"+str(index))
				accepting = State("S"+str(index+1))
				# Add the 2 paths with epsilon transition from start
				start.add_transition('ϵ',nfa1.start_state)
				start.add_transition('ϵ',nfa2.start_state)
				# Add the 2 paths with epsilon transition to the end
				nfa1.accept_state.add_transition('ϵ', accepting)
				nfa2.accept_state.add_transition('ϵ', accepting)
				# Add to NFA Stack output
				NFAStack.append(NFA(start,accepting))
				index+=2

			elif symbol == '*':  # Kleene star
				# Pop the operand
				nfa = NFAStack.pop()
				# we have a start and an end 
				start = State("S"+str(index))
				accepting = State("S"+str(index+1))
				# Add the 2 paths one with symbol and one empty to the end
				start.add_transition('ϵ',nfa1.start_state)
				start.add_transition('ϵ',accepting)
				# Add the 2 paths with epsilon transition to the end and back again to start
				nfa.accept_state.add_transition('ϵ', start)
				nfa.accept_state.add_transition('ϵ', accepting)
				# Add to NFA Stack output
				NFAStack.append(NFA(start,accepting))
				index+=2

			elif symbol == '+':  # Positive closure (A+)
				nfa = NFAStack.pop()  
				# we have a start and an end 
				start = State("S"+str(index))
				accepting = State("S"+str(index+1))
				# Add the path one with symbol 
				start.add_transition('ϵ',nfa.start_state)
				# Add the 2 paths with epsilon transition to the end  and back again to start
				nfa.accept_state.add_transition('ϵ', start)
				nfa.accept_state.add_transition('ϵ', accepting)
				# Add to NFA Stack output
				NFAStack.append(NFA(start,accepting))
				index+=2

			elif symbol == '?':  # Kleene star
				nfa = NFAStack.pop()  
				# we have a start and an end 
				start = State("S"+str(index))
				accepting = State("S"+str(index+1))
				# Add the 2 paths one with symbol and one empty to the end
				start.add_transition('ϵ',nfa1.start_state)
				start.add_transition('ϵ',accepting)
				# Add the path with epsilon transition to the end
				nfa.accept_state.add_transition('ϵ', accepting)
				# Add to NFA Stack output
				NFAStack.append(NFA(start,accepting))
				index+=2
				
			else:  # character/symbol/number
				start = State("S"+str(index))
				accepting = State("S"+str(index+1))
				# Add an epsilon transition
				start.add_transition(symbol,accepting)
				# Add to NFA Stack output
				NFAStack.append(NFA(start,accepting))
				index+=2
		return NFAStack.pop()  # Final NFA
	
	def get_states(self):
		'''
		Return states in the NFA as a list
		'''
		visited, statesList, queue = set(), [], [self.start_state]
		visited.add(self.start_state)
		while queue:
			state = queue.pop(0)
			statesList.append(state)
			for (transition) in state.transitions:
				if transition[1] not in visited:
					visited.add(transition[1])
					queue.append(transition[1])
		states={}
		for state in statesList:
			stateDictionary = {
                'isTerminatingState': state.accepting,
            }
			for symbol, nextState in state.transitions:
				if symbol not in stateDictionary:
					stateDictionary[symbol] = nextState.name
				else:
					stateDictionary[symbol] += ',' + nextState.name
			states[state.name] = stateDictionary
		
		return {'startingState': self.start_state.name,**states,}

	def get_graph(self, name="fsm", view=False):
		'''
		Return the NFA as a graph
		'''
		nfa = self.get_states()
		g = Digraph(engine='dot')
		for state, transitions in nfa.items():
			if state == 'startingState':
				continue
			if transitions['isTerminatingState']:
				g.node(state, shape='doublecircle')
			else:
				g.node(state, shape='circle')
			
			for symbol, nextState in transitions.items():
				if symbol == 'isTerminatingState':
					continue
				childStates = nextState.split(',')
				for child in childStates:
					g.edge(state, child, name=symbol)
		g.render(name, view=view)
		return g
	