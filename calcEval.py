"""
Created on Sat Feb 26 22:32:53 2022

Author: Carl Cassar
"""

def evalRPN(rpnTokens):
    """
    This function evaluates a postfix expression.

    Postfix expressions are also known as Reverse Polish Notation or RPN, hence
    the function name.

    Evaluating a postfix expression is easier than evaluating an infix expression
    because it does not contain any brackets and there are no operator precedence
    rules to consider. A postfix expression can be evaluated using the following
    algorithm:
    """
    
    
    from calcLexer import isStrA_Num
    
    # Create a new empty list, values
    values = []
    
    # For each token in the postfix expression...
    for i in range(len(rpnTokens)):
        #...If the token is a number...
        if isStrA_Num(rpnTokens[i]) != False:
            #...Convert it to a number and add it to the end of values.
            values = values + [float(rpnTokens[i])]
        # Otherwise i.e. if it's an operator...
        else:
            # Remove an item from the end of values and call it right.
            rtOperand = values[-1]
            values = values[0:-1]
            # Remove an item from the end of values and call it left.
            ltOperand = values[-1]
            values = values[0:-1]
            
            # Apply the operator to the left and right operands.
            if rpnTokens[i] == "+":
                interimAns = ltOperand + rtOperand
            elif rpnTokens[i] == "-":
                interimAns = ltOperand - rtOperand
            elif rpnTokens[i] == "*":
                interimAns = ltOperand * rtOperand
            elif rpnTokens[i] == "/":
                interimAns = ltOperand / rtOperand
            elif rpnTokens[i] == "^":
                interimAns = ltOperand ** rtOperand
            # Append the result to the end of values.
            values = values + [interimAns]
            
    # Return the first item in values as the value of the expression.
    calcAns = values[0]
    
    if calcAns == int(calcAns):
        calcAns = int(calcAns)
    
    return calcAns

# ----------------------------------------------------------------------------

if __name__ == "__main__":
    
    print('\n')
    print("This program returns the answer for a valid arithmetic ", \
          "expression.\n")
    userStr = input("Enter an arithmetic expression.\n")
    
    from calcLexer import parSpacesIdx, operIdx, genTokens
    
    [parOpIdx, parClIdx, spacesIdx, stripped_str] = parSpacesIdx(userStr)
    [comb, stripped, allIdx] = \
        operIdx(stripped_str, parOpIdx, parClIdx, spacesIdx)
    [tokensList, tokensLabels] = genTokens(comb, stripped_str, allIdx)
    
    from calcParser import isInfValid, shuntingYard
    
    if isInfValid(tokensLabels) is False:
        print("ERROR: Invalid expression.\n")
    else:
        postFixExp = shuntingYard(tokensList, tokensLabels)
        finalAns = evalRPN(postFixExp)
        print('\n')
        print('**********************************\n')
        print("Tokens arranged in infix form: \n")
        print(tokensList, '\n')
        print('Tokens arranged in postfix form: \n')
        print(postFixExp, '\n')
        print('**********************************\n')
        print("Computed answer: \n")
        print(finalAns, '\n')
        print('**********************************\n')
        
