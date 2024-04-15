from dfa import DFA
from utils import *
from nfa import NFA


def __main__():

    # 1. Get user Input
    regex_1 = 'a+|b+'

    # # 2. Check if the regex is valid
    if not is_regex_valid(regex_1):
        print("Invalid regex")

    # 3. Turn regex to postfix
    postfixRegex = regex_to_postfix(regex_1)
    print("postfix regex:", postfixRegex)

    # # 4. Turn postfix to NFA
    nfa = NFA(regex=postfixRegex)
    print("NFA:", nfa.get_states())

    # # 5. Write the FSM to a file
    # convert list of states to json
    # json_states = nfa.to_json()
    # write_json(json_states)

    # # 6. Display the NFA as a graph
    # display_graph(nfa)

    # 7. Convert NFA to DFA
    dfa = DFA(nfa=nfa)
    dfa.get_graph()


if __name__ == '__main__':
    __main__()
