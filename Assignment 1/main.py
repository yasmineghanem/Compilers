from utils import *
from dfa import DFA
from nfa import NFA
from minDfa import MinDFA


def __main__():

    # 1. Get user Input
    regex_1 = 'a*b+[a-z]'
    # regex_1 = 'a|b'
    # # 2. Check if the regex is valid
    if not is_regex_valid(regex_1):
        print("Invalid regex")

    # 3. Turn regex to postfix
    postfixRegex = regex_to_postfix(regex_1)
    print("postfix regex:", postfixRegex)

    # 4. Turn postfix to NFA & Display
    nfa = NFA(regex=postfixRegex)
    nfa.get_graph()

    # 5. Write the NFA to a file
    write_json(nfa.to_json())

    # 6. Convert NFA to DFA
    dfa = DFA(nfa=nfa)
    dfa.get_graph()

    # 7. Write the DFA to a file
    # write_json(nfa.to_json())

    # 8. Convert DFA to Minimized DFA
    miniDfa = MinDFA(dfa)
    miniDfa.get_graph()

    # 9. Write the Minimized DFA to a file
    # write_json(miniDfa.to_json())

if __name__ == '__main__':
    __main__()
