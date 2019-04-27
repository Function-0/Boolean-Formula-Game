from formula_game_functions import *
from random import randint

NOT, AND, OR = '-', '*', '+'
OPS = {0: NOT, 1: AND, 2: OR}
VARS = {0: 'x', 1: 'y', 2: 'z', 3: 'a', 4: 'b', 5: 'c', 6: 'd', 7:'e',
        8: 'f', 9: 'g', 10: 'h'}


def generate_formula(layers, var='x'):
    """(int[, str]) -> str

    Builds and returns a random formula of with a given number of layers,
    such that a formula with a layer of zero is simply the variable itself.

    NOTE: formulas with layers > 6 will get VERY LARGE!

    REQ: layers >= 0
    REQ: var == var.lower() and len(var) == 1
    """
    # Base case: 0th layer is simply the var itself (leaf).
    if layers == 0:
        formula = var
    # Recursive decomposition: n-1 approach.
    else:
        # Get a random operator.
        operator = OPS[randint(0, 2)]
        # Case 1: create an unary layer.
        if operator == NOT:
            formula = generate_formula(layers - 1, var)
            # Check if sub-formula is already negated.
            if formula[0] != NOT:
                formula = NOT + formula
        # Case 2: create a binary layer.
        else:
            # Recursively generate sub-formulas.
            sub_formula = generate_formula(layers - 1, var)
            # Generate another random variable.
            other_var = VARS[randint(0, 10)]
            other_formula = generate_formula(randint(0, layers), other_var)
            # Swap sub-formulas for random balance.
            if randint(0, 1) == 0:
                sub_formula, other_formula = other_formula, sub_formula
            # Concatenate the binary formula.
            formula = '(' + sub_formula + operator + other_formula + ')'
    # Return formula at current recursive call.
    return formula


if __name__ == '__main__':
    new_formula = generate_formula(5)
    print(new_formula)
    # a = "(-(((-h+d)*-(((-a*c)*-a)*(x+(-x*x))))*-((a*-z)+((x*h)*c)))+(((x*((h+a)+a))+-(-g+f))*-(f*g)))"
    valid_formulas = [
        'x',
        '-x',
        '(x+y)',
        '(x*y)',
        '(-x+y)',
        '(x+-y)',
        '(-x+-y)',
        '(-x*y)',
        '(x*-y)',
        '(-x*-y)',
        '-(x+y)',
        '-(x*y)',
        '((x+y)*z)',
        '-((x*y)+z)',
        '-((y*(-y*y))*-x)',
        '--x'
    ]
    invalid_formulas = [
        '-(x)',
        '(-x)',
        '(x)',
        'x+y',
        '(-(x))',
        '-',
        'x+',
        '*x',
        'X',
        '((x))',
        '(x+y',
        'x+y)',
        'xx',
        '()',
        ')(',
        '(xy)',
        ')x+y(',
        '123'
    ]
        
    # a = 'x'
    # b = '-y'
    # c = '(x+y)'
    # d = '(-x*y)'
    # e = '((x+y)+(y+x))'
    # f = '(((x+y)*(x+y))+((a+b)*(a+b)))'
    
    # aa = build_tree(a)
    # bb = build_tree(b)
    # cc = build_tree(c)
    # dd = build_tree(d)
    # ee = build_tree(e)
    # ff = build_tree(f)
    
    # A1 = play2win(aa, 'E', 'x' , '')
    # A2 = play2win(aa, 'A', 'x' , '') 
    # A3 = play2win(bb, 'E', 'y' , '')
    # A4 = play2win(bb, 'A', 'y' , '')
    # A5 = play2win(cc, 'AA', 'xy' , '')
    # A6 = play2win(cc, 'EE', 'xy' , '')
    # A7 = play2win(cc, 'AE', 'xy' , '0')
    # A8 = play2win(cc, 'EA', 'xy' , '0')
    # A9 = play2win(cc, 'AE', 'xy' , '1')
    # A10 = play2win(cc, 'EA', 'xy' , '1')
    # A11 = play2win(dd, 'AA', 'xy' , '')
    # A12 = play2win(dd, 'EE', 'xy' , '')
    # A13 = play2win(dd, 'AE', 'xy' , '0')
    # A14 = play2win(dd, 'EA', 'xy' , '0')
    # A15 = play2win(dd, 'AE', 'xy' , '1')
    # A16 = play2win(dd, 'EA', 'xy' , '1')
    # A17 = play2win(ee, 'AA', 'xy' , '')
    # A18 = play2win(ee, 'AA', 'xy' , '1')
    # A19 = play2win(ee, 'EE', 'xy' , '')
    # A20 = play2win(ee, 'EE', 'xy' , '0')
    # A21 = play2win(ee, 'AE', 'xy' , '')
    # A22 = play2win(ee, 'AE', 'xy' , '0')
    # A23 = play2win(ee, 'EA', 'xy' , '')
    # A24 = play2win(ee, 'EA', 'xy' , '1')
    # A25 = play2win(ff, 'EEEE', 'xyab' , '101')
    # A26 = play2win(ff, 'EEEE', 'xyab' , '10')
    # A27 = play2win(ff, 'EEEE', 'xyab' , '1')
    # A28 = play2win(ff, 'EEEE', 'xyab' , '')
    # A29 = play2win(ff, 'AAAA', 'xyab' , '101')
    # A30 = play2win(ff, 'AAAA', 'xyab' , '10')
    # A31 = play2win(ff, 'AAAA', 'xyab' , '1')
    # A32 = play2win(ff, 'AAAA', 'xyab' , '')
    # A33 = play2win(ff, 'AEAE', 'xyab' , '101')
    # A34 = play2win(ff, 'AEAE', 'xyab' , '10')
    # A35 = play2win(ff, 'AEAE', 'xyab' , '1')
    # A36 = play2win(ff, 'AEAE', 'xyab' , '')
    # B = (str(A1)+
         # str(A2)+
         # str(A3)+
         # str(A4)+
         # str(A5)+
         # str(A6)+
         # str(A7)+
         # str(A8)+
         # str(A9)+
         # str(A10)+
         # str(A11)+
         # str(A12)+
         # str(A13)+
         # str(A14)+
         # str(A15)+
         # str(A16)+
         # str(A17)+
         # str(A18)+
         # str(A19)+
         # str(A20)+
         # str(A21)+
         # str(A22)+
         # str(A23)+
         # str(A24)+
         # str(A25)+
         # str(A26)+
         # str(A27)+
         # str(A28)+
         # str(A29)+
         # str(A30)+
         # str(A32)+
         # str(A33)+
         # str(A34)+
         # str(A35)+
         # str(A36))
    # if(B=='10010110100010100011011011110001010'):
        # print(True)    