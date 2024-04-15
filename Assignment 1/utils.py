import re
import json


def is_regex_valid(regex):

    # 1- Check that the characters in regex are within the valid set of characters
    # 2- check that all brackets are closed
    regex_operations = ['|', '(', ')', '[', ']', '.',
                        '?', '*', '+', '-', '\\\\']
    bracket, parenthesis = 0, 0

    for char in regex:
        if not char.isalnum() and char != ' ' and char not in regex_operations:
            return False

        if char == '(':
            bracket += 1
        elif char == ')':
            bracket -= 1
        elif char == '[':
            parenthesis += 1
        elif char == ']':
            parenthesis -= 1
    if bracket != 0 or parenthesis != 0:
        return False

    return True


def is_regex_validdd(regex):
    try:
        re.compile(regex)
        return True
    except:
        return False


# Test
validity_check = is_regex_valid("[A-Zl]/ko;]")
print(validity_check)


def regex_to_postfix(regex):
    # Operators and precedance level: * (kleene star), + (one or more), ? (zero or one), . (concatenation), and | (ORing).
    operators = {'*': 5, '+': 4, '?': 3, '.': 2, '|': 1}
    # Initialize the postfix and stack (temp) strings to empty strings.
    postfix, stack = "", ""
    # 1. Check for square brakcets of letter as ORs and replace them with |. i.e. Character class
    for i in range(len(regex)):
        char = regex[i]
        if char == '[':
            j = i + 1
            while regex[j] != ']':
                if regex[j].isalnum() and regex[j + 1].isalnum():
                    regex = regex[:j + 1] + '|' + regex[j + 1:]
                j += 1

    # Replace all remaining square brackets with parentheses.
    # This is done because parentheses are used to group sub-expressions in regular expressions
    regex = regex.replace('[', '(')
    regex = regex.replace(']', ')')

    # print("postfix: ", regex)

    # Replace ranges in character classes with the individual characters they represent.
    hyphen_count = regex.count('-')
    for i in range(hyphen_count):
        for j in range(len(regex)):
            char = regex[j]
            if char == '-':
                final = regex[j + 1]
                first = regex[j - 1]
                temp_list = ''
                for k in range(int(ord(final) - ord(first))):
                    temp_list = temp_list + '|'
                    temp = chr(ord(first) + k + 1)
                    temp_list = temp_list + temp
                regex = regex[0: j] + temp_list + regex[j + 2:]
                break
    # print("postfix2", regex)

    # Insert a concatenation operator (.) between any two adjacent characters if there is no operator between them. OR there is a bracket
    dotIndices = []
    for i in range(len(regex) - 1):
        startOps = [')', "*", "+", "*"]
        endOps = ["*", "+", ".", "|", ")"]
        if regex[i] in startOps and regex[i+1] not in endOps:
            dotIndices.append(i)
        elif regex[i].isalnum() and (regex[i+1].isalnum() or regex[i+1] == '('):
            dotIndices.append(i)

    for i in range(len(dotIndices)):
        regex = regex[:dotIndices[i] + 1 + i] + \
            '.' + regex[dotIndices[i] + 1 + i:]
    # print("postfix: ", regex)

    # Shunt_Yard Algorithm
    for i in range(len(regex)):
        c = regex[i]
        # If the character is an opening parenthesis, push it onto the stack.
        if c == '(':
            stack = stack + c
        # If the character is a closing parenthesis, pop operators off the stack and append them to the postfix string until an opening parenthesis is found & delete the parenthesis
        elif c == ')':
            while stack[-1] != '(':
                # places the character at the end of the stack in the postfix expression
                postfix = postfix + stack[-1]
                # [:-1] denotes up to or including the last character
                stack = stack[:-1]
            stack = stack[:-1]  # removes the open bracket in the stack

        # If the character is an operator, pop operators off the stack and append them to the postfix string as long as they have higher or equal precedence to the current operator. Then push the current operator onto the stack.
        elif c in operators:
            while stack and operators.get(c, 0) <= operators.get(stack[-1], 0):
                postfix, stack = postfix + stack[-1], stack[:-1]
            stack = stack + c

        # If the character is a operand (i.e. not an operator or parenthesis), append it to the postfix string.
        else:
            postfix = postfix + c
    # After iterating over all characters of the regular expression, the function pops any remaining operators off the stack and appends them to the postfix string.
    while stack:
        postfix, stack = postfix + stack[-1], stack[:-1]
    # print("postfix: ", regex)

    # Finally, the function returns the postfix notation of the input regular expression.
    return postfix

# print(regex_to_postfix("[a-c]"))


def write_json(nfa, filename="fsm.json"):
    json_object = json.dumps(nfa, indent=4)
    with open(filename, "w") as f:
        json.dump(json_object, f)


def display_graph(nfa, filename="fsm.gv"):
    nfa.get_graph(name=filename)
    pass
