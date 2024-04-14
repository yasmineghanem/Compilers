from collections import deque
import graphviz
import nfa


class DFA:
    def __init__(self, nfa) -> None:
        self.nfa = nfa
        self.states = dict()

    def epsilon_closure(self, state):
        # Epsilon closure of a set of states is the set of states reachable from the input set of states
        # by following epsilon transitions
        closure = set(state)
        # the same state could be added multiple times
        possible_states = list(state)

        while possible_states:
            current_state = possible_states.pop()
            for symbol, next_state in current_state.get_transitions():
                if next_state not in closure:
                    if symbol == 'ϵ':
                        closure.add(next_state)
                        possible_states.append(next_state)

        # sort the states in the closure
        closure = sorted(closure, key=lambda x: x.name)

        # convert to string
        closure_string = ''
        for state in closure:
            closure_string += state.name + ','

        return closure

    def nfa_to_dfa(self):
        nfa_states = self.nfa.get_states()

        # Create the start state of the DFA
        initial_dfa_state = self.epsilon_closure(nfa_states[0])
        self.states['startingState'] = initial_dfa_state


        print('Initial State:', initial_dfa_state)
