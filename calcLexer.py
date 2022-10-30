"""
Created on Thu Feb 24 11:08:56 2022

Author: Carl Cassar
"""

def isStrA_Num(strInput):
    """
    This function checks if a string input can be converted to a float or an
    integer.
    """
    isNum = True
    
    if type(strInput) != str:
        isNum = False
        return isNum
    
    stripped_str = strInput.strip()
    numOfDcmPts = stripped_str.count('.')
    numOfPluses = stripped_str.count('+')
    numOfMinuses = stripped_str.count('-')
    
    if (numOfDcmPts > 1) or (numOfPluses > 1) or (numOfMinuses > 1):
        isNum = False
        return isNum
    
    # Generate a string of all characters that can form part of a number:
        
    strComparator = "+-.0123456789"
    
    
    for i in range(len(stripped_str)):
        if (stripped_str[i] in strComparator) is False:
            isNum = False
            return isNum
        elif stripped_str[i] == "+" or stripped_str[i] == "-":
            if (i != 0) or (len(stripped_str) < 2):
                isNum = False
                return isNum
        elif stripped_str[i] == ".":
            if i == (len(stripped_str) - 1):
                isNum = False
                return isNum
    
    return isNum, stripped_str
        

        
def parSpacesIdx(userStrInput):
    stripped_str = userStrInput.strip()
    parOpenIdx = []; parCloseIdx = []; spacesIdx = []
    
    for i in range(len(stripped_str)):
        if stripped_str[i] == "(":
            parOpenIdx = parOpenIdx + [i]
        elif stripped_str[i] == ")":
            parCloseIdx = parCloseIdx + [i]
        elif stripped_str[i] == " ":
            spacesIdx = spacesIdx + [i]
    
    return parOpenIdx, parCloseIdx, spacesIdx, stripped_str

"""
A + or - is part of a number if:
    It is the first character in the string.
    It comes after a *, /, ^ or (.
"""


def operIdx(stripped_str, parOpenIdx, parCloseIdx, spacesIdx):
    
    prev_char = ''
    oIdx = []
    charStr = "*/^("
    pmStr = "+-"
    
    for i in range(len(stripped_str)):
        # If the string is '*', '/' or '^', the index can be added to the list
        # of operator indexes.
        if (stripped_str[i] == "*") or (stripped_str[i] == "/") \
            or (stripped_str[i] == "^"):
            oIdx = oIdx + [i]
        # If the string is '+' or '-', not the first character in the string
        # and comes after a '*', '/', '^' or '(', then it is an operator and
        # the index can be added to the list of operator indexes.
        elif (stripped_str[i] in pmStr) and (prev_char != '') and \
            (prev_char in charStr) is False:
            oIdx = oIdx + [i]
        # By making sure that 'prev_char' never contains whitespace, we make
        # sure that we are comparing the current character with the previous
        # non-whitespace character.
        if stripped_str[i] != " ":
            prev_char = stripped_str[i]
    # combIdx contains the indexes of parentheses, spaces and operators.        
    combIdx = parOpenIdx + parCloseIdx + spacesIdx + oIdx
    combIdx = sorted(combIdx)
    allIdx = list(range(len(stripped_str)))
    
    return combIdx, stripped_str, allIdx


def genTokens(combIdx, stripped_str, allIdx):
    # Initialise an empty list called 'idx'. This will contain all the indexes
    # which do not store spaces, parentheses or operators.
    idx = []
    for i in range(len(allIdx)):
        if (allIdx[i] in combIdx) is False:
            idx = idx + [i]
    
    # 'gap_start_idx' will contain a subset of 'idx'. In this case, gap means
    # any block of indexes which do not contain any spaces, parentheses or
    # operators. Therefore, 'gap_start_idx' will be a list of all the first
    # indexes of each gap, i.e. if there are 3 blocks which do not contain any
    # spaces, parentheses or operators, then 'gap_start_idx' will be a list
    # of length 3, containing the first index of each block.
    gap_start_idx = [idx[0]]
    
    # Note: If the user inputs a valid arithmetic expression, these gaps will
    # contain the numbers of the expression.
    
    
    for i in range(1, len(idx)):
        if (idx[i] - idx[i - 1]) != 1:
            gap_start_idx = gap_start_idx + [idx[i]]
            
    combGap = sorted(combIdx + gap_start_idx)
    # 'gapList' will be populated by the strings contained in each gap.
    gapList = list(range(len(gap_start_idx)))
    # 'gap_size' will contain the size of each gap. Therefore, 'gap_start_idx'
    # and 'gap_size' together will tell us which elements to copy from
    # 'stripped_str' to 'gapList'.
    gap_size = list(range(len(gap_start_idx)))
    gap_to_end = False
    
    # If there are no spaces, parentheses or operators after the last element
    # in 'gap_start_idx', then it means that the string expression ends with
    # a gap. In this case, the string that must be copied to 'gapList' is
    # simply all the last elements of 'stripped_str', starting from the last
    # index in 'gap_start_idx'.
    if gap_start_idx[-1] == combGap[-1]:
        gap_to_end = True
        gapList[-1] = stripped_str[gap_start_idx[-1]:]
        gap_size[-1] = len(gapList[-1])
    
    # For all indexes in 'gap_start_idx' except the last one, I calculate the
    # size of each gap, and copy the relevant elements from 'stripped_str' to
    # 'gapList'.
    for i in range(len(gap_start_idx) - 1):
        gap_size[i] = combGap[combGap.index(gap_start_idx[i]) + 1] - \
            combGap[combGap.index(gap_start_idx[i])]
        gapList[i] = \
            stripped_str[gap_start_idx[i]:(gap_start_idx[i] + gap_size[i])]
    
    # If 'stripped_str' does not end with a gap, then I can also apply the
    # previous two commands for the last index in 'gap_start_idx'.
    if gap_to_end is False:
        i += 1
        gap_size[i] = combGap[combGap.index(gap_start_idx[i]) + 1] - \
            combGap[combGap.index(gap_start_idx[i])]
        gapList[i] = \
            stripped_str[gap_start_idx[i]:(gap_start_idx[i] + gap_size[i])]
    
    # If the arithmetic expression entered by the user is valid, any parts of
    # the string which are not spaces, parentheses or operators, should contain
    # numbers. Here, I check whether these parts are numbers, and if not I
    # return an error message to the user.
    for i in range(len(gapList)):
        if isStrA_Num(gapList[i]) is False:
            print("ERROR: Some tokens cannot be generated.\n")
            return
    
    # If the program reaches the next lines of code, it means that all the
    # blocks which did not contain spaces, parentheses or operators, did in
    # fact contain valid numbers (positive or negative integers or floats).
    
    # When initialised, 'strippedList' is a list of the same length as
    # 'stripped_str'. 
    strippedList = list(stripped_str)
    j = 0
    # The for loop copies number tokens from 'gapList' into the appropriate
    # index of 'strippedList'. The appropriate index corresponds to the first
    # index of each block. Since any block containing parts of the same
    # number are being concatenated into a single element in the 'strippedList'
    # the remaining indexes which previously contained the remaining parts of
    # the number are now being replaced by whitespace since they are no longer
    # needed.
    for i in idx:
        if i in gap_start_idx:
            strippedList[i] = gapList[j]
            j += 1
        elif (i in gap_start_idx) is False:
            strippedList[i] = ' '
    
    # Initialisation of 'tokensList' and 'tokensLabels'.
    tokensList = []; tokensLabels = []
    j = 0
    # All non-whitespace substrings in 'strippedList' are copied to 
    # 'tokensList'. For each token, an appropriate token label is also
    # generated and stored in 'tokensLabels'.
    for i in range(len(strippedList)):
        if strippedList[i] != " ":
            tokensList = tokensList + [strippedList[i]]
            if (tokensList[j] in "+-*/^") and len(tokensList[j]) == 1:
                tokensLabels = tokensLabels + ["op"]
            elif tokensList[j] == "(":
                tokensLabels = tokensLabels + ["opPar"]
            elif tokensList[j] == ")":
                tokensLabels = tokensLabels + ["clPar"]
            else:
                tokensLabels = tokensLabels + ["nu"]
            
            j += 1
    
    return tokensList, tokensLabels

if __name__ == "__main__":
    print('\n')
    print("This program returns tokens for arithmetic expressions.\n")
    userStr = input("Enter an arithmetic expression.\n")
    [parOpIdx, parClIdx, spacesIdx, stripped_str] = parSpacesIdx(userStr)
    [comb, stripped, allIdx] = \
        operIdx(stripped_str, parOpIdx, parClIdx, spacesIdx)
    [tokensList, tokensLabels] = genTokens(comb, stripped_str, allIdx)
    
    print('\n')
    print('**********************************\n')
    print("Tokens: \n")
    print(tokensList, '\n')
    print('Token labels where "nu" means number, "op" means operator, and ', \
          '"opPar" and "clPar" mean open and close parentheses respectively:')
    print('\n')
    print(tokensLabels, '\n')
    print('**********************************\n')

