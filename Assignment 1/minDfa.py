from graphviz import Digraph
from utils import *


class MinDFA:

    def __init__(self, dfa):
        self.dfa = dfa
        self.states = self.minimize_dfa()

    def get_group_index(self, group):
        indeces = []
        for state in group:
            for index, __ in state.items():
                indeces.append(index)
        return indeces

    def minimize_dfa(self):
        # Get all states and symbols of DFA
        states = self.dfa.get_dfa_states()
        symbols = self.dfa.get_symbols()

        starting_state_name = states.pop('startingState')

        groups, acceptingStates, normalStates = [], [], []
        # seperate goups to accepting and normal states
        for symbol, transition in states.items():
            if transition["isTerminatingState"] == True:
                acceptingStates.append({symbol: transition})
            else:
                normalStates.append({symbol: transition})
        groups.append(acceptingStates)
        groups.append(normalStates)

        split = True
        while split:
            split = False  # unless we found a group needs to be split
            for index, group in enumerate(groups):
                if not group:
                    continue
                expectedGroups = {}
                firstState = next(iter(group))
                for _, transition in firstState.items():
                    for symbol in symbols:
                        if symbol in transition:
                            expectedGroups[symbol] = [i for i, group in enumerate(
                                groups) if transition[symbol] in self.get_group_index(group)][0]  # {transitionState1,  transitionState1}

                splittedStates = []
                for _, state in enumerate(group):
                    outputGroups = {}
                    for _, transition in state.items():
                        for symbol in symbols:
                            if symbol in transition:
                                List = [j for j, group in enumerate(
                                    groups) if transition[symbol] in self.get_group_index(group)]
                                outputGroups[symbol] = List[0]
                    # compare groups and split if different
                    if outputGroups != expectedGroups:
                        split = True
                        splittedStates.append(state)
                # add the new splittes states and remove old ones
                if len(splittedStates) > 0:
                    groups.insert(index+1, list(splittedStates))
                    groups[index] = [
                        state for state in group if state not in splittedStates]

        # Create new groups
        hashTable = {}
        for index, group in enumerate(groups):
            for state in group:
                for name, _ in state.items():
                    hashTable[name] = str(index)

        newGroups = {'startingState': hashTable[starting_state_name]}

        # iterate over the groups
        # for each state in the group loop over its symbol and transitionState
        # if the transition state belongs to another group, replace it with group number
        for index, group in enumerate(groups):
            for state in group:
                for _, transition in state.items():
                    if transition['isTerminatingState'] == True and len(transition) == 1:
                        newGroups[str(index)] = transition

                    for symbol, transitionState in transition.items():
                        if transitionState in hashTable:
                            transition[symbol] = str(
                                hashTable[transitionState])
                            newGroups[str(index)] = transition
        return newGroups

    def to_json(self):
        return self.states.copy()

    def get_graph(self, name="outputs/dfa_min_graph", view=False):
        '''
        Return Miminzed DFA as a graph
        '''
        graph = Digraph(engine='dot')
        starting_state = ''
        for state, transitions in self.states.items():
            if state == 'startingState':
                starting_state = self.states[state]
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
        graph.render(name, view=view)
        return graph
