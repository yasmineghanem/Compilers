import re
import json
import os


def create_output_folder(regex, output_path="outputs/"):

    if not os.path.exists(output_path):
        # create a new directory for the given regex
        os.makedirs(output_path)

    # get number of files in the directory
    folder_name = str(len([name for name in os.listdir(output_path)]))

    os.makedirs(output_path + folder_name)

    # create a new file to write the regex in
    with open(output_path + folder_name + "/regex.txt", "w") as f:
        f.write(regex)

    return folder_name


def is_regex_valid(regex):
    '''
    Checks if regex entered is valid
    Returns True/False
    '''
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
# validity_check = is_regex_valid("[A-Zl]/ko;]")
# print(validity_check)


def regex_to_postfix(regex):
    '''
    Turns regex to Postfix notation using Shunt Yard Algorithm
    Returns: postfix regex
    '''
    # Operators and precedance level: * (kleene star), + (one or more), ? (zero or one), . (concatenation), and | (ORing).
    operators = {'*': 5, '+': 4, '?': 3, '.': 2, '|': 1}
    # Initialize the postfix and stack (temp) strings to empty strings.
    postfix, stack = "", ""

    # Insert a concatenation (.) between any two adjacent symbols if there is none exists/bracket
    dotsIndex = []
    i = 0
    while i < len(regex)-1:
        startOps = [')', "*", "+", ']', '?']
        endOps = ["*", "+", ".", "|", ")", ']', '?']
        if regex[i] == '[':
            while regex[i] != ']':
                i += 1
            if i+1 < len(regex) and (regex[i+1].isalnum() or regex[i+1] == '(' or regex[i+1] == '['):
                dotsIndex.append(i)
        elif regex[i] in startOps and regex[i+1] not in endOps:
            dotsIndex.append(i)
        elif regex[i].isalnum() and (regex[i+1].isalnum() or regex[i+1] == '(' or regex[i+1] == '['):
            dotsIndex.append(i)
        i += 1
    for i in range(len(dotsIndex)):
        regex = regex[:dotsIndex[i] + 1 + i] + \
            '.' + regex[dotsIndex[i] + 1 + i:]

    # Shunt_Yard Algorithm
    for i in range(len(regex)):
        c = regex[i]
        # If we have a parenthesis push till closing parenthesis, pop operators from stack and append them to the output postfix string til the opening parenthesis
        if c == '(':
            stack = stack + c
        elif c == ')':
            while stack[-1] != '(':
                # place the character at the end of the stack
                postfix = postfix + stack[-1]
                stack = stack[:-1]
            stack = stack[:-1]  # remove the parenthesis
        elif c == '?':
            postfix = postfix + c
        # If the character is an operator append if higher precedence and push the other one to stack.
        elif c in operators:
            while stack and operators.get(c, 0) <= operators.get(stack[-1], 0):
                postfix, stack = postfix + stack[-1], stack[:-1]
            stack = stack + c

        # Appendf the character is a operand not operator/parenthesis)
        else:
            postfix = postfix + c
    # Pop remaining operators
    while stack:
        postfix, stack = postfix + stack[-1], stack[:-1]

    return postfix


def write_json(fsm, filename="outputs/dummy.json"):
    '''
    Turns fsm json object to json file
    '''
    json_object = json.dumps(fsm, indent=4)
    with open(filename, "w") as f:
        json.dump(fsm, f)
