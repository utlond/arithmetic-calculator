"""
Created on Sat Feb 26 13:54:22 2022

Author: Carl Cassar
"""

def isInfValid(tokensLabels):
    infixValid = True
    listLength = len(tokensLabels)
    nuNum = tokensLabels.count("nu")
    opNum = tokensLabels.count("op")
    opParNum = tokensLabels.count("opPar")
    clParNum = tokensLabels.count("clPar")
    
    # Rule 1: Expression must contain at least 2 numbers and 1 operator.
    if (nuNum < opNum + 1) or opNum < 1:
        infixValid = False
        return infixValid
    
    # Rule 2: An operator can never occur at the start or the end of the
    # expression.
    
    elif tokensLabels[0] == "op" or tokensLabels[-1] == "op":
        infixValid = False
        return infixValid
    
    # Rule 3: The number of open parentheses must be equal to the number of
    # close parentheses.
    
    elif opParNum != clParNum:
        infixValid = False
        return infixValid   

    prev_token = tokensLabels[0]
    for i in range(1, listLength):
        
        # Rule 4: There can never be adjacent operator tokens or number tokens.
        
        if prev_token == "nu" and tokensLabels[i] == "nu":
            infixValid = False
            return infixValid
        elif prev_token == "op" and tokensLabels[i] == "op":
            infixValid = False
            return infixValid
        
        # Rule 5: An open parenthesis token can never be immediately followed
        # by a close parenthesis token or vice-versa.
        
        elif prev_token == "opPar" and tokensLabels[i] == "clPar":
            infixValid = False
            return infixValid
        elif prev_token == "clPar" and tokensLabels[i] == "opPar":
            infixValid = False
            return infixValid
        
        # Rule 6: An open parenthesis token can never be immediately followed
        # by an operator token, nor can an operator token be immediately
        # followed by a close parenthesis token.
        elif prev_token == "opPar" and tokensLabels[i] == "op":
            infixValid = False
            return infixValid
        elif prev_token == "op" and tokensLabels[i] == "clPar":
            infixValid = False
            return infixValid
        
        prev_token = tokensLabels[i]
        
    # Rule 7: Going from left to right in the expression, the number of
    # close parentheses can at no point be greater than the number of open
    # parentheses.
    
    opParCnt = 0; clParCnt = 0
     
    for i in range(listLength):
        if tokensLabels[i] == "opPar":
            opParCnt += 1
        elif tokensLabels[i] == "clPar":
            clParCnt += 1
        if opParCnt < clParCnt:
            infixValid = False
            return infixValid
        
    return infixValid


def precedence(strOperator):
    
    if strOperator in "+-":
        opPrecedence = 1
    elif strOperator in "*/":
        opPrecedence = 2
    elif strOperator == "^":
        opPrecedence = 3
    else:
        opPrecedence = -1   
    
    return opPrecedence


def shuntingYard(tokensList, tokensLabels):
    """
    The shunting-yard algorithm is used to convert the infix expression to postfix
    format. The code in this function implements this algorithm.
    """
    postfix = []
    firstOpIdx = tokensLabels.index("op")
    firstParIdx = -1
    if "opPar" in tokensLabels:
        firstParIdx = tokensLabels.index("opPar")
        firstIdx = min(firstOpIdx, firstParIdx)
        operators = [tokensList[firstIdx]]
    elif firstParIdx == -1:
        firstIdx = firstOpIdx
        operators = [tokensList[firstIdx]]   
    
    for i in range(len(tokensLabels)):
        # If the token is an integer, add the token to the end of postfix.
        if tokensLabels[i] == "nu":
            postfix = postfix + [tokensList[i]]
        # If the token is an operator...     
        elif (tokensLabels[i] == "op") and (i != firstIdx):
            # While operators is not empty and the last item in operators is
            # not an open parenthesis and precedence(token) <=
            # precedence(last item in operators)...
            """
            precedence(token) < precedence(last item in operators) gives right
            associativity
            precedence(token) <= precedence(last item in operators) gives left
            associativity
            
            In the next while loop I use left associativity.
            """
            while (len(operators) >= 1) and \
                (operators[-1] != "(") \
                and precedence(tokensList[i]) <= \
                    precedence(operators[-1]):
                # ...Remove the last item from operators and add it to postfix.
                postfix = postfix + [operators[-1]]
                operators = operators[0:-1]
            # Add token to the end of operators.
            operators = operators + [tokensList[i]]
        # If the token is an open parenthesis...
        elif (tokensList[i] == "(") and (i != firstIdx):
            # ...Add token to the end of operators.
            operators = operators + [tokensList[i]]
        # If the token is a close parenthesis...
        elif tokensList[i] == ")":
            # ...While the last item in operators is not an open parenthesis
            while operators[-1] != "(":
                # ...Remove the last item from operators and add it to postfix.
                postfix = postfix + [operators[-1]]
                operators = operators[0:-1]
            # Remove the open parenthesis from operators.
            operators = operators[0:-1]
            
    
    # While operators is not an empty list...
    while len(operators) >= 1:
        # ...Remove the last item from operators and add it to postfix.
        postfix = postfix + [operators[-1]]
        operators = operators[0:-1]
    
    
    return postfix

if __name__ == "__main__":
    
    print('\n')
    print("This program returns a list of tokens arranged in postfix form ", \
          "for arithmetic expressions.\n")
    userStr = input("Enter an arithmetic expression.\n")
    
    from calcLexer import parSpacesIdx, operIdx, genTokens
    
    [parOpIdx, parClIdx, spacesIdx, stripped_str] = parSpacesIdx(userStr)
    [comb, stripped, allIdx] = \
        operIdx(stripped_str, parOpIdx, parClIdx, spacesIdx)
    [tokensList, tokensLabels] = genTokens(comb, stripped_str, allIdx)
    
    if isInfValid(tokensLabels) is False:
        print("ERROR: Invalid expression.\n")
    else:
        postFixExp = shuntingYard(tokensList, tokensLabels)
        print('\n')
        print('**********************************\n')
        print("Tokens arranged in infix form: \n")
        print(tokensList, '\n')
        print('Tokens arranged in postfix form: \n')
        print(postFixExp, '\n')
        print('**********************************\n')

