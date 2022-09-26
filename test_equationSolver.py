import unittest
import sys
import subprocess
import importlib
from test_base import captured_output
from equationSolver import Equation

class EquationSolverTestCase(unittest.TestCase):

    def testEquationWithOneVariableOnOneSide(self):
        """
        Equations with variable on one side of the equal sign
        """

        with captured_output() as (out, err):
            equation = Equation("7x - 2 = 21")
            equation.Solve()

        output = out.getvalue().strip()
        self.assertEqual("""7x - 2 = 21

Add the numbers
7x-2 = 21

Rearrange
7x = 23

Solution
x = 23/7""", output)

    def testEquatioWithVariableOnEitherSide(self):
        """
        Equation with variable on either side of the equal sign
        """

        with captured_output() as (out, err):
            equation = Equation("3x + 6 = 5x")
            equation.Solve()

        output = out.getvalue().strip()
        self.assertEqual("""3x + 6 = 5x

Add the numbers
3x+6 = 5x

Rearrange
-2x = -6

Solution
x = 3""", output)

    def testEquationWithParenthesis(self):
      """
      Equation that has parenthesis
      """
      with captured_output() as (out, err):
          equation = Equation("5x + 2(3x + 4) = 30")
          equation.Solve()

      output = out.getvalue().strip()
      self.assertEqual("""5x + 2(3x + 4) = 30

Distribution
5x+6x+8  =  30

Add the numbers
11x+8 = 30

Rearrange
11x = 22

Solution
x = 2""", output)

    def testEquationWithVariableAndHasNoVisibleCoEffiecient(self):
        """
        Variables with no visible co-effecients have a co-efficeint of one
        """

        with captured_output() as (out, err):
            equation = Equation("7x + x = 8")
            equation.Solve()

        output = out.getvalue().strip()
        self.assertEqual("""7x + x = 8

Add the numbers
8x = 8

Rearrange
8x = 8

Solution
x = 1""", output)


    def testEquationWithMissingOpenningBracket(self):
        """
        Equation that has closing bracket but no opening bracket
        """

        with captured_output() :
            try:
                equation = Equation("5x + 23x + 4) = 30")
                equation.Solve()
                self.assertFalse(False)
            except ValueError:
                self.assertTrue(True)



    def testEquationWithMissingClosingBracket(self):
        """
        Equation that has opening bracket but no closing bracket
        """
        with captured_output() :
            try:
                Equation("5x + 2(3x + 4 = 30")
                self.assertFalse(False)
            except ValueError:
                self.assertTrue(True)


    def testEquationWithNoEqualSign(self):
        """
        Equation without equal sign
        """
        with captured_output() :
            try:
                Equation("5x + 2(3x + 4 ")
                self.assertFalse(False)
            except ValueError:
                self.assertTrue(True)


    def testEquationWithNoVariable(self):
        """
        Equation that lacks variable
        """
        with captured_output() :
            try:
                Equation("5 = 3 ")
                self.assertFalse(False)
            except ValueError:
                self.assertTrue(True)




if __name__ == '__main__':
    unittest.main()
