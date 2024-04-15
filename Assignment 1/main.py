from utils import *
from dfa import DFA
from nfa import NFA
from minDfa import MinDFA


def __main__():

    # 1. Get user Input
    regex_tests = [ '(a*?)*', #0
                   '(a*)*', #1 done
                   '(b?a)', #2
                   '(a*b*)([a-b]*)', #3
                   '(a+?a+?)+?b', #4
                   '(a+a+)+b', #5
                   '(a|b)*a[ab]?', #6
                   '[a-c]*', #7
                   '[A-Ea-c]+1|2[0-9]*k?[ABC](ABC)', #8
                   '[a-f0-9]32', #9
                   '[a-fA-C]', #10
                   '[abc](d|e|f)', #11
                   '[bc]*(cd)+', #12
                   'a*b+[a-z]c?', #13
                   'a*|b*', #14
                   'a*b*ca', #15
                   'a+|b+', #16
                   'a+b', #17
                   'a+b*', #18
                   'a+b*a', #19
                   'ab(b|c)*d+', #20
                   'Aym[o+o+]na?', #21
                   'employ(er|ee|ment|ing|able)', #22
                   'kam*(o|ou)la?', #23
                   'lex(eme|er|ical)[0-9]+' #24
                   ]
    
    # # 2. Check if the regex is valid
    if not is_regex_valid(regex_tests[2]):
        print("Invalid regex")
        return

    # 3. Turn regex to postfix
    postfixRegex = regex_to_postfix(regex_tests[2])
    print("postfix regex:", postfixRegex)

    # 4. Turn postfix to NFA & Display
    nfa = NFA(regex='b?a.')
    nfa.get_graph()

    # 5. Write the NFA to a file
    write_json(nfa.to_json(),"outputs/nfa.json")

    # 6. Convert NFA to DFA
    dfa = DFA(nfa=nfa)
    dfa.get_graph()

    # 7. Write the DFA to a file
    write_json(dfa.to_json(),"outputs/dfa.json")

    # 8. Convert DFA to Minimized DFA
    miniDfa = MinDFA(dfa)
    miniDfa.get_graph()

    # 9. Write the Minimized DFA to a file
    write_json(miniDfa.to_json(),"outputs/min_dfa.json")

if __name__ == '__main__':
    __main__()
