from utils import *
from dfa import DFA
from nfa import NFA
from minDfa import MinDFA


def __main__():

    # 1. Get user Input
    regex = input("Enter a regular expression: ")
    print("You entered:", regex)
    regex_tests = ['(a*?)*',                            # 0 done
                   '(a*)*',                             # 1 done
                   '(b?a)',                             # 2 done
                   '(a*b*)([a-b]*)',                    # 3 done
                   '(a+?a+?)+?b',                       # 4 done
                   '(a+a+)+b',                          # 5 done
                   '(a|b)*a[ab]?',                      # 6 done
                   '[a-c]*',                            # 7 done
                   '[A-Ea-c]+1|2[0-9]*k?[ABC](ABC)',    # 8 done
                   '[a-f0-9]32',                        # 9 done
                   '[a-fA-C]',                          # 10 done
                   '[abc](d|e|f)',                      # 11 done
                   '[bc]*(cd)+',                        # 12 done
                   'a*b+[a-z]c?',                       # 13 done
                   'a*|b*',                             # 14 done
                   'a*b*ca',                            # 15 done
                   'a+|b+',                             # 16 done
                   'a+b',                               # 17 done
                   'a+b*',                              # 18 done
                   'a+b*a',                             # 19 done
                   'ab(b|c)*d+',                        # 20 done
                   'employ(er|ee|ment|ing|able)',       # 21 done
                   'kam*(o|ou)la?',                     # 22 done
                   'lex(eme|er|ical)[0-9]+'             # 23 done
                   ]

    # # 2. Check if the regex is valid
    if not is_regex_valid2(regex):
        print("Invalid regex")
        return

    # 2. Create a directory with the current regex
    folder_name = create_output_folder(regex, "outputs/")

    # 3. Turn regex to postfix
    postfixRegex = regex_to_postfix(regex)

    # 4. Turn postfix to NFA & Display
    nfa = NFA(regex=postfixRegex)
    nfa.get_graph(path="outputs/" + folder_name + '/')

    # 5. Write the NFA to a file
    write_json(nfa.to_json(), "outputs/" + folder_name + "/nfa.json")

    # 6. Convert NFA to DFA
    dfa = DFA(nfa=nfa)
    dfa.get_graph(path="outputs/" + folder_name + '/')

    # 7. Write the DFA to a file
    write_json(dfa.to_json(), "outputs/" + folder_name + "/dfa.json")

    # 8. Convert DFA to Minimized DFA
    miniDfa = MinDFA(dfa)
    miniDfa.get_graph(path="outputs/" + folder_name + '/')

    # 9. Write the Minimized DFA to a file
    write_json(miniDfa.to_json(), "outputs/" + folder_name + "/min_dfa.json")


if __name__ == '__main__':
    __main__()
