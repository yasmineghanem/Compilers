from graphviz import Digraph
from utils import *

class MinDFA:

    def __init__(self, dfa):
        self.dfa = dfa
        self.states = self.minimize_dfa(dfa)
        
    def get_group_index(self, group):
        indeces = []
        for state in group:
            for index, __ in state.items():
                indeces.append(index)
        return indeces
    
    def minimize_dfa(self,dfa):
        states = self.dfa.get_dfa_states() 
        symbols = self.dfa.get_symbols()
        states.pop('startingState')
        groups, acceptingStates, normalStates = [], [], []
        for symbol, transition in states.items():
            if transition["isTerminatingState"] == True:
                acceptingStates.append({symbol: transition})
            else:
                normalStates.append({symbol:transition})
        groups.append(acceptingStates)
        groups.append(normalStates)
        split = True
        while split:
            split = False # unless we found a group needs to be split
            # groups = [[{symbol: transition}],[{symbol: transition}]]
            for index, group in enumerate(groups):
                if not group:
                    continue
                expectedGroups = {}
                firstState = next(iter(group)) # {statename1: {symbol: transitionState1, symbol: transitionState2}}
                for _, transition in firstState.items():
                    for symbol in symbols:
                        if symbol in transition:
                            expectedGroups[symbol]=  [i for i, group in enumerate(groups) if transition[symbol] in self.get_group_index(group)][0] # {transitionState1,  transitionState1}
                
                splittedStates = []
                for _,state in enumerate(group):
                    outputGroups = {}
                    for _, transition in state.items():
                        for symbol in symbols:
                            if symbol in transition:
                                List = [j for j, group in enumerate(groups) if transition[symbol] in self.get_group_index(group)]
                                outputGroups[symbol] = List[0]
                    # compare groups and split if different
                    if outputGroups != expectedGroups:
                        split = True
                        splittedStates.append(state)
                # add the new splittes states and remove old ones
                if len(splittedStates) > 0:
                    groups.insert(index+1, list(splittedStates))
                    groups[index] = [state for state in group if state not in splittedStates] 
        
		# Create new groups 
        newGroups = {'startingState':0}
        groupCopy = groups.copy()
        # create a hashtable for the states (group number is the key)
        hashTable = {}
        for index, group in enumerate(groups):
            for state in group:
                for i, value in state.items():
                    hashTable[i] = str(index)
        
        # iterate over the groups
        # for each state in the group loop over its symbol and transitionState
        # if the transition state belongs to another group, replace it with group number
        for index, group in enumerate(groupCopy):
            for state in group:
                for key, value in state.items():
                    for symbol, transitionState in value.items():
                        
                        if transitionState in hashTable:
                            value[symbol] = str(hashTable[transitionState])
                            newGroups[str(index)] = value
        return newGroups
        
    def to_json(self):
        return self.states
    
    def get_graph(self, name="outputs/dfa_min_graph",view=False):
        '''
        Return Miminzed DFA as a graph
        '''
        graph = Digraph(engine='dot')
        for state, transitions in self.states.items():
            if state == 'startingState':
                continue
            if transitions['isTerminatingState']:
                graph.node(state, shape='doublecircle')
            else:
                graph.node(state, shape='circle')
                
            for symbol, nextState in transitions.items():
                if symbol == 'isTerminatingState':
                    continue
                children_states = nextState.split(',')
                for child in children_states:
                    graph.edge(state, child, label=symbol)
        graph.render(name, view=view)
        return graph
    
           