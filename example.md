## Example

In the bottom figure below, I run the ‘calcEval.py’ file, and use the program to calculate an arithmetic expression. In this case, I input the following expression into the console:

-8.2 + (14 * 5 / 2) + 7 ^ 2

The output shows two lists of tokens, the first in infix form and the second in postfix form. Taking a closer look at the postfix form, here is how the expression is evaluated.

The evaluator scans the list from left to right and finds the first operator. Once it locates the first operator, it applies the operator to the two number tokens preceding it. The operator is removed and the 2 operands are substituted by a single operand which is the sub-result of the previous calculation. This process is repeated until all the expression has been evaluated. This is better shown by the worked example in the steps provided below, starting from the original postfix expression emitted by the parser.

![example breakdown](https://github.com/utlond/arithmetic-calculator/blob/main/example_breakdown.png)

![example output](https://github.com/utlond/arithmetic-calculator/blob/main/example_output.png)
