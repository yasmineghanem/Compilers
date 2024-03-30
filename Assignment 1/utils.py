# includes all utility functions for the assignment

class NFAState:
    def __init__(self, state_name):
        self.state_name = state_name # the name of the state
        self.transitions = {} # possible transitions from this state
        self.epsilon_transitions = [] # possible epsilon transitions from this state
        self.is_accepting = False # is this state an accepting state