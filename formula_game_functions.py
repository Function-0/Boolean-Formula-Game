"""
# Copyright Nick Cheng, 2016
# Copyright Ibrahim Jomaa, 2017
# Distributed under the terms of the GNU General Public License.
#
# This file is part of Assignment 2, CSCA48, Winter 2017
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This file is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

# Do not change this import statement, or add any of your own!
from formula_tree import FormulaTree, Leaf, NotTree, AndTree, OrTree

# Do not change any of the class declarations above this comment

# Add your functions here.

# CONSTANTS:
# Legend: |build_tree = 1       |
#         |draw_formula_tree = 2|
#         |evaluate = 3         |
#         |play2win = 4         |
OPEN_BRACKET = '('  # 1
CLOSED_BRACKET = ')'  # 1
LOWERCASE_LETTERS = "abcdefghijklmnopqrstuvwxyz"  # 1
TWO_SPACES = "  "  # 2
ONE_SPACE = " "  # 2
NEW_LINE = "\n"  # 2
PLAYERS = {'E': 1, 'A': 0}  # 4
CONNECTIVES = {'-': NotTree, '+': OrTree, '*': AndTree}  # 2 3
NOT = '-'  # 1 2 3
AND = '*'  # 1 2 3
OR = '+'  # 1 2 3


def build_tree(formula):
    '''(str) -> FormulaTree or NoneType
    Returns the root of the equivalent FormulaTree that represents the given
    formula. Said formula must be a vaid formula, and if not, NoneType is
    instead returned.

    >>> formula_1 = 'x'
    >>> expected_1 = "Leaf('x')"
    >>> result_1 = str(build_tree(formula_1))
    >>> expected_1 == result_1
    True

    >>> formula_2 = "(x*-c)"
    >>> expected_2 = "AndTree(Leaf('x'), NotTree(Leaf('c')))"
    >>> result_2 = str(build_tree(formula_2))
    >>> expected_2 == result_2
    True

    >>> formula_3 = "((x+(z*e))+-x)"
    >>> expected_3 = "OrTree(OrTree(Leaf('x'), AndTree(Leaf('z'),\
 Leaf('e'))), NotTree(Leaf('x')))"
    >>> result_3 = str(build_tree(formula_3))
    >>> expected_3 == result_3
    True

    >>> formula_4 = "-((x+(a+c))+((b+d)*f))"
    >>> expected_4 = "NotTree(OrTree(OrTree(Leaf('x'), OrTree(Leaf('a'),\
 Leaf('c'))), AndTree(OrTree(Leaf('b'), Leaf('d')), Leaf('f'))))"
    >>> result_4 = str(build_tree(formula_4))
    >>> expected_4 == result_4
    True

    >>> formula_5 = "(-(x+(x*f))*(((z+y)*-g)*((h*d)+(z*-b))))"
    >>> expected_5 = "AndTree(NotTree(OrTree(Leaf('x'), AndTree(Leaf('x'),\
 Leaf('f')))), AndTree(AndTree(OrTree(Leaf('z'), Leaf('y')),\
 NotTree(Leaf('g'))), OrTree(AndTree(Leaf('h'), Leaf('d')),\
 AndTree(Leaf('z'), NotTree(Leaf('b'))))))"
    >>> result_5 = str(build_tree(formula_5))
    >>> expected_5 == result_5
    True

    >>> formula_6 = "(((-x*-y)*-h)+-(-f*((z+(g+c))+((z+-a)+(((e*c)+e)*\
(f+(a+g)))))))"
    >>> expected_6 = ("OrTree(AndTree(AndTree(NotTree(Leaf('x')),\
 NotTree(Leaf('y'))), NotTree(Leaf('h'))),\
 NotTree(AndTree(NotTree(Leaf('f')), OrTree(OrTree(Leaf('z'),\
 OrTree(Leaf('g'), Leaf('c'))), OrTree(OrTree(Leaf('z'),\
 NotTree(Leaf('a'))), AndTree(OrTree(AndTree(Leaf('e'), Leaf('c')),\
 Leaf('e')), OrTree(Leaf('f'), OrTree(Leaf('a'), Leaf('g')))))))))")
    >>> result_6 = str(build_tree(formula_6))
    >>> expected_6 == result_6
    True

    >>> formula = "(((-x*-y)*-h)+-(-f*((z+(g+c))++((z+-a)+(((e*c)+e)*\
 (f+(a+g)))))))"
    >>> expected_7 = None
    >>> result_7 = build_tree(formula)
    >>> expected_7 == result_7
    True
    '''
    # Assume that the formula is void
    result = None
    # Obtain the length of the formula
    formula_len = len(formula)
    # If the formula has 1 character and is a lowercase letter
    if ((formula_len == 1) and (formula in LOWERCASE_LETTERS)):
        # A Leaf node that contains the character (variable) is created
        result = Leaf(formula)
    # Else, if the formula has 2 characters, where the 1st character is '-' and
    # the 2nd character is a lowercase letter
    elif ((formula_len == 2) and
          ((formula[0] == NOT) and
          (formula[-1] in LOWERCASE_LETTERS))):
        # A Not node connected to a leaf node that contains the 2nd character
        # (variable) is created
        result = NotTree(Leaf(formula[-1]))
    # Else, if the formula has more than 2 characters
    elif (formula_len > 2):
        # Obtain the 1st character from the formula
        first_char = formula[0]
        # If the 1st character is '-'
        if (first_char == NOT):
            # Create a Not node:
            # The Not node's child will be the recursive call to the function,
            # with the 1st character removed from the formula
            sub_tree = build_tree(formula[1:])
            result = NotTree(sub_tree)
            # If the Not node's child does not exist
            if (not sub_tree):
                # This formula is void
                result = None
        # Else, if the formula is closed by brackets
        elif ((first_char == OPEN_BRACKET) and
              (formula[-1] == CLOSED_BRACKET)):
            # Remove those brackets
            formula = formula[1:-1]
            # Update the length of the formula
            formula_len = len(formula)
            # Get the indices of '+' or '*' in the formula that allows the
            # formula to be split into 2 sub formulas:
            # Holds all the indices where we have possibly found '+' or '*'
            # that satisfies the above condition
            indices_of_interest = set()
            # A formula can be split into 2 sub formulas if when either '+' or
            # '*' is found, we are not in a sub formula. Therefore, we must
            # have balanced brackets when either '+' or '*' is found
            sub_formulas = 0
            # Go through each character in the formula
            for index in range(formula_len):
                # Obtain the current character
                char = formula[index]
                # If the character is '('
                if (char == OPEN_BRACKET):
                    # We have entered a sub formula
                    sub_formulas += 1
                # Else, if the character is ')'
                elif (char == CLOSED_BRACKET):
                    # We have exited a sub formula
                    sub_formulas -= 1
                # Else, if the character is either '+' or '*', and we are not
                # in any sub formulas
                elif (((char == OR) or
                       (char == AND)) and
                      (sub_formulas == 0)):
                    # Add the index to our set
                    indices_of_interest.add(index)
            # If the set of indices is not empty, and does not contain more
            # than 1 entry
            if ((indices_of_interest) and (len(indices_of_interest) == 1)):
                # Obtain the index of interest to split the formula into 2
                # sub formulas
                index_of_interest = indices_of_interest.pop()
                # Create either a Or node or a And node:
                node = CONNECTIVES[formula[index_of_interest]]
                # The specified node's left child will be the recursive call to
                # the function, with the string slice to the left of where
                # either '+' or '*' was found in the formula
                left_sub_tree = build_tree(formula[:index_of_interest])
                # The specified node's right child will be the recursive call
                # to the function, with the string slice to the right of where
                # either '+' or '*' was found in the formula
                right_sub_tree = build_tree(formula[index_of_interest + 1:])
                result = node(left_sub_tree, right_sub_tree)
                # If either left or right child does not exist
                if ((not left_sub_tree) or (not right_sub_tree)):
                    # This formula is void
                    result = None
    # Returns the FormulaTree equivalent to the given formula
    return result

# Helper function for draw_formula_tree


def _helper_draw_formula_tree(root, depth_level):
    r'''(FormulaTree, int) -> tuple of (str, int)
    Returns a tuple of: the string of the equivalent FormulaTree
    (i.e. a drawn out FormulaTree), and the depth_level that we are currently
    traversing within said tree.
    REQ: root is a vaild FormulaTree
    REQ: depth_level == 0

    >>> expected_1_depth = 0
    >>> expected_1_str = "x"
    >>> expected_1 = (expected_1_str, expected_1_depth)
    >>> formula_1 = "x"
    >>> depth_level_1 = 0
    >>> result_1 = _helper_draw_formula_tree(build_tree(formula_1),
    ... depth_level_1)
    >>> expected_1 == result_1
    True

    >>> expected_2_depth = 0
    >>> expected_2_str = "* - c\n  x"
    >>> expected_2 = (expected_2_str, expected_2_depth)
    >>> formula_2 = "(x*-c)"
    >>> depth_level_2 = 0
    >>> result_2 = _helper_draw_formula_tree(build_tree(formula_2),
    ... depth_level_2)
    >>> expected_2 == result_2
    True

    >>> expected_3_depth = 0
    >>> expected_3_str = "+ - x\n  + * e\n      z\n    x"
    >>> expected_3 = (expected_3_str, expected_3_depth)
    >>> formula_3 = "((x+(z*e))+-x)"
    >>> depth_level_3 = 0
    >>> result_3 = _helper_draw_formula_tree(build_tree(formula_3),
    ... depth_level_3)
    >>> expected_3 == result_3
    True

    >>> expected_4_depth = 0
    >>> expected_4_str = "- + * f\n      + d\n        b\n    + + "
    >>> expected_4_str += "c\n        a\n      x"
    >>> expected_4 = (expected_4_str, expected_4_depth)
    >>> formula_4 = "-((x+(a+c))+((b+d)*f))"
    >>> depth_level_4 = 0
    >>> result_4 = _helper_draw_formula_tree(build_tree(formula_4),
    ... depth_level_4)
    >>> expected_4 == result_4
    True

    >>> expected_5_depth = 0
    >>> expected_5_str = "* * + * - b\n        z\n      * d\n        h\n"
    >>> expected_5_str += "    * - g\n      + y\n        z\n  - + * f\n"
    >>> expected_5_str += "        x\n      x"
    >>> expected_5 = (expected_5_str, expected_5_depth)
    >>> formula_5 = "(-(x+(x*f))*(((z+y)*-g)*((h*d)+(z*-b))))"
    >>> depth_level_5 = 0
    >>> result_5 = _helper_draw_formula_tree(build_tree(formula_5),
    ... depth_level_5)
    >>> expected_5 == result_5
    True

    >>> expected_6_depth = 0
    >>> expected_6_str = "+ - * + + * + + g\n                a\n"
    >>> expected_6_str += "              f\n            + e\n"
    >>> expected_6_str += "              * c\n                e\n"
    >>> expected_6_str += "          + - a\n            z\n        + + c\n"
    >>> expected_6_str += "            g\n          z\n      - f\n  * - h\n"
    >>> expected_6_str += "    * - y\n      - x"
    >>> expected_6 = (expected_6_str, expected_6_depth)
    >>> formula_6 = "(((-x*-y)*-h)+-(-f*((z+(g+c))+((z+-a)+(((e*c)+e)*"
    >>> formula_6 += "(f+(a+g)))))))"
    >>> depth_level_6 = 0
    >>> result_6 = _helper_draw_formula_tree(build_tree(formula_6),
    ... depth_level_6)
    >>> expected_6 == result_6
    True
    '''
    # Obtain the symbol of the node
    symbol = root.symbol
    # Store the node's symbol in a string, and add 1 space
    formula_str = symbol + ONE_SPACE
    # If we have a Not node
    if (symbol == NOT):
        # Obtain the recursive call to the function with the Not node's child
        # as the root, having increased the depth level
        (sub_tree_str, sub_tree_depth_level) = (
            _helper_draw_formula_tree(root.children[0], depth_level + 1))
        # Add the recursive call's string to our string
        formula_str += sub_tree_str
    # Else, if we have a Leaf node
    elif (symbol not in CONNECTIVES):
        # Retract 1 space from our string
        formula_str = formula_str[:-1]
    # Else, we either have a And or Or node
    else:
        # Obtain the recursive call to the function with the specified
        # node's right child as the root, having increased the depth level
        (right_sub_tree_str, right_sub_tree_depth_level) = (
            _helper_draw_formula_tree(root.children[-1], depth_level + 1))
        # Add the right child's recursive call's string to our string
        formula_str += right_sub_tree_str
        # Obtain the recursive call to the funtion with the specified
        # node's left child as the root, having increased the depth level
        (left_sub_tree_str, left_sub_tree_depth_level) = (
            _helper_draw_formula_tree(root.children[0], depth_level + 1))
        # Add a newline character to our string
        formula_str += NEW_LINE
        # Add a multiple of 2 character spaces based on our current
        # depth level to our string
        formula_str += ((depth_level + 1) * TWO_SPACES)
        # Add the left child's recursive call's string to our string
        formula_str += left_sub_tree_str
    # Returns the tuple of: the FormulaTree's string and the depth level that
    # we are currently traversing within said tree
    result = (formula_str, depth_level)
    return result


def draw_formula_tree(root):
    r'''(FormulaTree) -> str
    Returns the string of the equivalent FormulaTree
    (i.e. a drawn out FormulaTree).
    REQ: root is a vaild FormulaTree

    >>> expected_1 = "x"
    >>> formula_1 = "x"
    >>> result_1 = draw_formula_tree(build_tree(formula_1))
    >>> expected_1 == result_1
    True

    >>> expected_2 = "* - c\n  x"
    >>> formula_2 = "(x*-c)"
    >>> result_2 = draw_formula_tree(build_tree(formula_2))
    >>> expected_2 == result_2
    True

    >>> expected_3 = "+ - x\n  + * e\n      z\n    x"
    >>> formula_3 = "((x+(z*e))+-x)"
    >>> result_3 = draw_formula_tree(build_tree(formula_3))
    >>> expected_3 == result_3
    True

    >>> expected_4 = "- + * f\n      + d\n        b\n    + + "
    >>> expected_4 += "c\n        a\n      x"
    >>> formula_4 = "-((x+(a+c))+((b+d)*f))"
    >>> result_4 = draw_formula_tree(build_tree(formula_4))
    >>> expected_4 == result_4
    True

    >>> expected_5 = "* * + * - b\n        z\n      * d\n        h\n"
    >>> expected_5 += "    * - g\n      + y\n        z\n  - + * f\n"
    >>> expected_5 += "        x\n      x"
    >>> formula_5 = "(-(x+(x*f))*(((z+y)*-g)*((h*d)+(z*-b))))"
    >>> result_5 = draw_formula_tree(build_tree(formula_5))
    >>> expected_5 == result_5
    True

    >>> expected_6 = "+ - * + + * + + g\n                a\n"
    >>> expected_6 += "              f\n            + e\n"
    >>> expected_6 += "              * c\n                e\n"
    >>> expected_6 += "          + - a\n            z\n        + + c\n"
    >>> expected_6 += "            g\n          z\n      - f\n  * - h\n"
    >>> expected_6 += "    * - y\n      - x"
    >>> formula_6 = "(((-x*-y)*-h)+-(-f*((z+(g+c))+((z+-a)+(((e*c)+e)*"
    >>> formula_6 += "(f+(a+g)))))))"
    >>> result_6 = draw_formula_tree(build_tree(formula_6))
    >>> expected_6 == result_6
    True
    '''
    # Obtain the string equivalent of the FormulaTree
    (formula_tree_str, depth_level) = _helper_draw_formula_tree(root, 0)
    # Returns the string version of the FormulaTree
    return formula_tree_str


# Helper function for evaluate
def _helper_evaluate(root, vars_to_values):
    '''(FormulaTree, dict of {str: int}) -> int
    Given the values for each variable in the FormulaTree, vars_to_values:
    Returns the truth value, either 1 (True) or 0 (False) of the formula.
    REQ: root is a valid FormulaTree
    REQ: len(vars_to_values) >= 1
    REQ: vars_to_values contains the variables that are found in the
         FormulaTree, and each variables' values are either '1' or '0'

    >>> formula_1 = 'x'
    >>> expected_1 = 1
    >>> var_to_values_1 = {'x': 1}
    >>> result_1 = _helper_evaluate(build_tree(formula_1), var_to_values_1)
    >>> expected_1 == result_1
    True

    >>> formula_2 = "(x*-c)"
    >>> expected_2 = 0
    >>> var_to_values_2 = {'x': 1, 'c': 1}
    >>> result_2 = _helper_evaluate(build_tree(formula_2), var_to_values_2)
    >>> expected_2 == result_2
    True

    >>> formula_3 = "((x+(z*e))+-x)"
    >>> expected_3 = 1
    >>> var_to_values_3 = {'x': 0, 'z': 1, 'e': 1}
    >>> result_3 = _helper_evaluate(build_tree(formula_3), var_to_values_3)
    >>> expected_3 == result_3
    True

    >>> formula_4 = "-((x+(a+c))+((b+d)*f))"
    >>> expected_4 = 0
    >>> var_to_values_4 = {'x': 0, 'c': 1, 'a': 1, 'b': 1, 'd': 0, 'f': 0}
    >>> result_4 = _helper_evaluate(build_tree(formula_4), var_to_values_4)
    >>> expected_4 == result_4
    True

    >>> formula_5 = "(-(x+(x*f))*(((z+y)*-g)*((h*d)+(z*-b))))"
    >>> expected_5 = 0
    >>> var_to_values_5 = {'x': 1, 'f': 0, 'z': 1, 'y':0, 'g': 1, 'h': 1,
    ... 'd': 1, 'b': 1}
    >>> result_5 = _helper_evaluate(build_tree(formula_5), var_to_values_5)
    >>> expected_5 == result_5
    True

    >>> formula_6 = "(((-x*-y)*-h)+-(-f*((z+(g+c))+((z+-a)+(((e*c)+e)*\
(f+(a+g)))))))"
    >>> expected_6 = 0
    >>> var_to_values_6 = {'x': 0, 'y': 1, 'h': 1, 'f': 0, 'z': 0, 'g': 0,
    ... 'c': 0, 'a': 0, 'e': 1}
    >>> result_6 = _helper_evaluate(build_tree(formula_6), var_to_values_6)
    >>> expected_6 == result_6
    True
    '''
    # Obtain the symbol of the node
    symbol = root.symbol
    # If we have a Leaf node
    if (symbol not in CONNECTIVES):
        # The truth value of the variable is the truth value of the formula
        result = int(vars_to_values[symbol])
    # Else, if we have a Not node
    elif (symbol == NOT):
        # The truth value of the formula is the recursive call to the function
        # with the Not node's child as the root, applied with the Not
        # connective
        result = int(not _helper_evaluate(root.children[0], vars_to_values))
    # Else, if we have an Or node
    elif (symbol == OR):
        # The truth value of the formula is the recursive calls to the function
        # with the Or node's left and right children as the root, applied with
        # the Or connective
        left_sub_tree_result = (
            _helper_evaluate(root.children[0], vars_to_values))
        right_sub_tree_result = (
            _helper_evaluate(root.children[-1], vars_to_values))
        result = int(left_sub_tree_result or right_sub_tree_result)
    # Else, if we have a And node
    elif (symbol == AND):
        # The truth value of the formula is the recursive calls to the function
        # with the And node's left and right children as the root, applied
        # with the And connective
        left_sub_tree_result = (
            _helper_evaluate(root.children[0], vars_to_values))
        right_sub_tree_result = (
            _helper_evaluate(root.children[-1], vars_to_values))
        result = int(left_sub_tree_result and right_sub_tree_result)
    # Returns the truth value of the formula
    return result


def evaluate(root, variables, values):
    '''(FormulaTree, str, str) -> int
    Given the variables in the FormulaTree; and the values
    corresponding to those variablesm in order: Returns the truth value,
    either 1 (True) or 0 (False) of the formula.
    REQ: root is a vaild FormulaTree
    REQ: len(variables) >= 1
    REQ: len(values) >= 1
    REQ: variables contains variables that are found in the FormulaTree
    REQ: characters in values are either '0' or '1'

    >>> formula_1 = 'x'
    >>> expected_1 = 1
    >>> variables_1 = 'x'
    >>> values_1 = '1'
    >>> result_1 = evaluate(build_tree(formula_1), variables_1, values_1)
    >>> expected_1 == result_1
    True

    >>> formula_2 = "(x*-c)"
    >>> expected_2 = 0
    >>> variables_2 = "xc"
    >>> values_2 = "11"
    >>> result_2 = evaluate(build_tree(formula_2), variables_2, values_2)
    >>> expected_2 == result_2
    True

    >>> formula_3 = "((x+(z*e))+-x)"
    >>> expected_3 = 1
    >>> variables_3 = "xze"
    >>> values_3 = "011"
    >>> result_3 = evaluate(build_tree(formula_3), variables_3, values_3)
    >>> expected_3 == result_3
    True

    >>> formula_4 = "-((x+(a+c))+((b+d)*f))"
    >>> expected_4 = 0
    >>> variables_4 = "xcabdf"
    >>> values_4 = "011100"
    >>> result_4 = evaluate(build_tree(formula_4), variables_4, values_4)
    >>> expected_4 == result_4
    True

    >>> formula_5 = "(-(x+(x*f))*(((z+y)*-g)*((h*d)+(z*-b))))"
    >>> expected_5 = 0
    >>> variables_5 = "xfzyghdb"
    >>> values_5 = "10101111"
    >>> result_5 = evaluate(build_tree(formula_5), variables_5, values_5)
    >>> expected_5 == result_5
    True

    >>> formula_6 = "(((-x*-y)*-h)+-(-f*((z+(g+c))+((z+-a)+(((e*c)+e)*\
(f+(a+g)))))))"
    >>> expected_6 = 0
    >>> variables_6 = "xyhfzgcae"
    >>> values_6 = "011000001"
    >>> result_6 = evaluate(build_tree(formula_6), variables_6, values_6)
    >>> expected_6 == result_6
    True
    '''
    # Create a dictionary mapping each variable to their respected values:
    # Obtain the number of variables
    num_vars = len(variables)
    # Holds the dictionary mapping variables to values
    vars_to_values = dict()
    # Go through each variable
    for index in range(num_vars):
        # Add the variable and its respected value into our dictionary
        vars_to_values[variables[index]] = values[index]
    # Obtain the truth value of the formula
    truth_value = _helper_evaluate(root, vars_to_values)
    # Returns the formula's truth value
    return truth_value

# Helper function for play2win


def _helper_play2win(root, turns, variables, values, player, solution_set,
                     index):
    '''(FormulaTree, str, str, str, str, set of int, int) -> set of int
    Given the turn order, turns; the variables in the FormulaTree; the values
    corresponding to those variables in order; the player that we intend to
    help win; the best next move the player can make, solution_set; and the
    index of where the player is found in the turn order: Returns the best
    next move the player can make. If the return set is empty, this means
    that the best next move the player can make is said player's default move
    (1 for 'E', 0 for 'A').
    REQ: root is a valid FormulaTree
    REQ: len(turns) >= 1
    REQ: len(variables) >= 1
    REQ: len(values) >= 1
    REQ: player is in {'E', 'A'}
    REQ: solution_set = set()
    REQ: index is a vaild index found in turns
    REQ: len(turns) > len(values)
    REQ: variables contains variables that are found in the FormulaTree
    REQ: characters in values are either '0' or '1'

    >>> formula_1 = 'x'
    >>> turns_1 = 'E'
    >>> variables_1 = 'x'
    >>> values_1 = ''
    >>> player_1 = 'E'
    >>> solution_set_1 = set()
    >>> index_1 = 0
    >>> expected_1 = {1}
    >>> result_1 = _helper_play2win(build_tree(formula_1), turns_1,
    ... variables_1, values_1, player_1, solution_set_1, index_1)
    >>> expected_1 == result_1
    True

    >>> formula_2 = "-y"
    >>> turns_2 = 'A'
    >>> variables_2 = 'y'
    >>> values_2 = ''
    >>> player_2 = 'A'
    >>> solution_set_2 = set()
    >>> index_2 = 0
    >>> expected_2 = {1}
    >>> result_2 = _helper_play2win(build_tree(formula_2), turns_2,
    ... variables_2, values_2, player_2, solution_set_2, index_2)
    >>> expected_2 == result_2
    True

    >>> formula_3 = "(x+y)"
    >>> turns_3 = "EA"
    >>> variables_3 = "xy"
    >>> values_3 = '0'
    >>> player_3 = 'A'
    >>> solution_set_3 = set()
    >>> index_3 = 1
    >>> expected_3 = {0}
    >>> result_3 = _helper_play2win(build_tree(formula_3), turns_3,
    ... variables_3, values_3, player_3, solution_set_3, index_3)
    >>> expected_3 == result_3
    True

    >>> formula_4 = "(-x*y)"
    >>> turns_4 = "AE"
    >>> variables_4 = "xy"
    >>> values_4 = '1'
    >>> player_4 = 'E'
    >>> solution_set_4 = set()
    >>> index_4 = 1
    >>> expected_4 = set()
    >>> result_4 = _helper_play2win(build_tree(formula_4), turns_4,
    ... variables_4, values_4, player_4, solution_set_4, index_4)
    >>> expected_4 == result_4
    True

    >>> formula_5 = "((x+y)+(y+x))"
    >>> turns_5 = "EA"
    >>> variables_5 = "xy"
    >>> values_5 = ''
    >>> player_5 = 'E'
    >>> solution_set_5 = set()
    >>> index_5 = 0
    >>> expected_5 = set()
    >>> result_5 = _helper_play2win(build_tree(formula_5), turns_5,
    ... variables_5, values_5, player_5, solution_set_5, index_5)
    >>> expected_5 == result_5
    True

    >>> formula_6 = "(((x+y)*(x+y))+((a+b)*(a+b)))"
    >>> turns_6 = "AEAE"
    >>> variables_6 = "xyab"
    >>> values_6 = "10"
    >>> player_6 = 'A'
    >>> solution_set_6 = set()
    >>> index_6 = 2
    >>> expected_6 = set()
    >>> result_6 = _helper_play2win(build_tree(formula_6), turns_6,
    ... variables_6, values_6, player_6, solution_set_6, index_6)
    >>> expected_6 == result_6
    True
    '''
    # Obtain the number of variables and values
    var_num = len(variables)
    values_num = len(values)
    # If each variable corresponds to 1 value
    if (var_num == values_num):
        # Evaluate the FormulaTree
        result = evaluate(root, variables, values)
        # If the result equals to our player's desired result
        if (result == PLAYERS[player]):
            # Add the last value in the values string to the solution set
            solution_set.add(int(values[-1]))
    else:
        # Recursively call the function with '1' added to the string of values
        solution_set_1 = (
            _helper_play2win(root, turns, variables, values + '1', player,
                             solution_set, index))
        # Recursively call the function with '0' added to the values
        solution_set_2 = (
            _helper_play2win(root, turns, variables, values + '0', player,
                             solution_set, index))
        # Combine the solution sets
        solution_set = solution_set_1.union(solution_set_2)
        # If the current player is not the one we wish to help and the
        # solution set contains only 1 value
        if ((turns[values_num] != player) and
            (len(solution_set) == 1)):
            # The solution set is void
            solution_set = set()
        # Else, if the current player is the one we wish to help and the
        # solution set contains 2 values
        elif ((turns[values_num] == player) and
              (len(solution_set) == 2)):
            # The solution set is void
            solution_set = set()
        # Else, if the solution set is not empty and it is possible to extract
        # the original first move that was made by our player that we want to
        # win before we went and created hypothetical senarios
        elif (solution_set and (len(values) >= index + 1)):
            # Empty the solution set
            solution_set.pop()
            # And add the original first move
            solution_set.add(int(values[index]))
    # Returns the solution set for the player that we want to win
    return solution_set


def play2win(root, turns, variables, values):
    '''(FormulaTree, str, str, str) -> int
    Given the turn order, turns; the variables in the FormulaTree; and the
    values corresponding to those variables in order: Returns the best next
    move the player can make. If there is no best next move that the player
    can make, or the best next move is arbitrary, the player's default move
    is returned instead (1 for 'E', 0 for 'A').
    REQ: root is a valid FormulaTree
    REQ: len(turns) >= 1
    REQ: len(variables) >= 1
    REQ: len(values) >= 1
    REQ: len(turns) > len(values)
    REQ: variables contains variables that are found in the FormulaTree
    REQ: characters in values are either '0' or '1'

    >>> formula_1 = 'x'
    >>> turns_1 = 'E'
    >>> variables_1 = 'x'
    >>> values_1 = ''
    >>> expected_1 = 1
    >>> result_1 = play2win(build_tree(formula_1), turns_1,
    ... variables_1, values_1)
    >>> expected_1 == result_1
    True

    >>> formula_2 = "-y"
    >>> turns_2 = 'A'
    >>> variables_2 = 'y'
    >>> values_2 = ''
    >>> expected_2 = 1
    >>> result_2 = play2win(build_tree(formula_2), turns_2,
    ... variables_2, values_2)
    >>> expected_2 == result_2
    True

    >>> formula_3 = "(x+y)"
    >>> turns_3 = "EA"
    >>> variables_3 = "xy"
    >>> values_3 = '0'
    >>> expected_3 = 0
    >>> result_3 = play2win(build_tree(formula_3), turns_3,
    ... variables_3, values_3)
    >>> expected_3 == result_3
    True

    >>> formula_4 = "(-x*y)"
    >>> turns_4 = "AE"
    >>> variables_4 = "xy"
    >>> values_4 = '1'
    >>> expected_4 = 1
    >>> result_4 = play2win(build_tree(formula_4), turns_4,
    ... variables_4, values_4)
    >>> expected_4 == result_4
    True

    >>> formula_5 = "((x+y)+(y+x))"
    >>> turns_5 = "EA"
    >>> variables_5 = "xy"
    >>> values_5 = ''
    >>> player_5 = 'E'
    >>> solution_set_5 = set()
    >>> index_5 = 0
    >>> expected_5 = 1
    >>> result_5 = play2win(build_tree(formula_5), turns_5,
    ... variables_5, values_5)
    >>> expected_5 == result_5
    True

    >>> formula_6 = "(((x+y)*(x+y))+((a+b)*(a+b)))"
    >>> turns_6 = "AEAE"
    >>> variables_6 = "xyab"
    >>> values_6 = "10"
    >>> expected_6 = 0
    >>> result_6 = play2win(build_tree(formula_6), turns_6,
    ... variables_6, values_6)
    >>> expected_6 == result_6
    True
    '''
    # Determine which player are we trying to help win:
    # Obtain the number of values
    values_num = len(values)
    player = turns[values_num]
    # Obtain the solution set for the player we are trying to help
    solution_set = (
        _helper_play2win(root, turns, variables, values, player, set(),
                         values_num))
    # If the solution set is empty
    if (not solution_set):
        # Have the player choose their default value
        result = PLAYERS[player]
    # Else, have the player choose their value based off of the value in the
    # solution set
    else:
        result = solution_set.pop()
    # Returns the best next move for the player whose turn is next
    return result

if (__name__ == "__main__"):
    import doctest
    doctest.testmod()
    