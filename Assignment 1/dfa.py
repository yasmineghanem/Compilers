from collections import deque
from graphviz import Digraph
from nfa import NFA, State
from utils import *


class DFA:
    def __init__(self, nfa):
        self.nfa = nfa
        self.states = self.nfa_to_dfa()

    def get_dfa_states(self):
        return self.states.copy()

    def get_symbols(self):
        return self.nfa.get_symbols()

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
            if state == closure[-1]:
                closure_string += state.name
            else:
                closure_string += state.name + ','

        return closure, closure_string

    def get_next_states(self, states, symbol):
        # print('States:', states)

        next_states = set()

        for state in states:
            for transition, next_state in state.transitions:
                # print(
                #     f"State: {state.name}, Transition: {transition}, Symbol: {symbol}, Next State: {next_state.name}")
                if transition == symbol:
                    next_states.add(next_state)

        return next_states

    def nfa_to_dfa(self):
        possible_symbols = self.nfa.get_symbols()

        start_state, start_state_string = self.epsilon_closure(
            [self.nfa.start_state])
        self.states = {'startingState': start_state_string}

        # create a queue to store the states that need to be processed
        queue = deque()
        names_queue = deque()
        queue.append(start_state)
        names_queue.append(start_state_string)

        # create a set to store the states that have been processed
        processed_states = set([start_state_string])

        while queue:
            current_state = queue.popleft()
            current_state_name = names_queue.popleft()
            for symbol in possible_symbols:
                next_states, next_states_string = self.epsilon_closure(
                    self.get_next_states(current_state, symbol))
                if (next_states):
                    if next_states_string not in processed_states:
                        queue.append(next_states)
                        names_queue.append(next_states_string)
                        processed_states.add(next_states_string)
                    self.states.setdefault(current_state_name, {})[
                        symbol] = next_states_string
            self.states.setdefault(current_state_name, {})[
                'isTerminatingState'] = self.nfa.is_accepting(current_state)

        return self.states

    def to_json(self):
        return self.states.copy()

    def get_graph(self, path="outputs/", view=False):
        '''
        Return the DFA as a graph
        '''
        dfa = self.get_dfa_states()
        graph = Digraph(engine='dot')
        starting_state = ''
        for state, transitions in dfa.items():
            if state == 'startingState':
                starting_state = dfa[state]
                continue
            if transitions['isTerminatingState']:
                if state == starting_state:
                    graph.node(state, shape='doublecircle', color='blue')
                else:
                    graph.node(state, shape='doublecircle')
            else:
                if state == starting_state:
                    graph.node(state, shape='circle', color='blue')
                else:
                    graph.node(state, shape='circle')

            for symbol, nextState in transitions.items():
                if symbol == 'isTerminatingState':
                    continue
                graph.edge(state, nextState, label=symbol)
        graph.render(path + "dfa_graph", view=view)
        return graph
