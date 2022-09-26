import re
from fractions import Fraction

class Equation:

    # instance attributes
    def __init__(self, equation, ):

        self.equation = equation
        if not self.__validEquation():

            raise ValueError("Invalid Equation")
        self.LHS = equation.split("=")[0] #LeftHand side of the equation
        self.RHS = equation.split("=")[1] #RightHand side of the equation

    def __validEquation(self):
        """
        Validates if the equation is true
        :return true if valid, else false:
        """
        #if equation missing parenthesis or equal sign
        if self.equation.count("(") != self.equation.count(")") or len(self.equation.split("=")) != 2:
            return False

        #if missing a variable
        elif not any( [x.isalpha() for x in self.equation]):
            return False

        return True


    # instance method
    def Solve(self):

        '''
        Solving the equation by calling desired methods
        :return None:
        '''
        print(self.equation)
        #Getting values with brackets in the LeftHand side of the equation
        LHSoperands = self.LHS.split(")")

        #Getting values with brackets in the RightHand side of the equation
        RHSoperands = self.RHS.split(")")

        #If the closing/opening brackets are missing or there are no values on either side of the equation


        #Doing distribution operation on values with brackets
        for i in range(len(LHSoperands)):

            if "(" in LHSoperands[i]:
                LHSoperands[i] = self.__distributioOperation(LHSoperands[i])

        for i in range(len(RHSoperands)):

            if "(" in RHSoperands[i]:
                RHSoperands[i] = self.__distributioOperation(RHSoperands[i])


        if len(LHSoperands) > 1 or len(RHSoperands) > 1:
            print("\nDistribution")
            print(''.join(LHSoperands) + " = " + ''.join(RHSoperands))


        #Adding the common factors after distribution
        equation = self.__addCommonFactors(''.join(LHSoperands)) + \
                   " = " + self.__addCommonFactors(''.join(RHSoperands))

        if len(equation): print("\nAdd the numbers")

        print(equation)

        #Rearrangin the numbers, storing constants on one side and variables/co-efficients on one side
        equation = self.__reArrangeNumbers(equation)

        #Getting and printing the solution
        self.__getSolution(equation)

        return equation




    def __distributioOperation(self, equation):
            '''

            Perform distribution rule

            :param equation:
            :return distributed equation:
            '''

            #numbers before the start of the bracket
            multiplier = equation.split("(")[0].strip().lstrip()

            #find first number before the opening bracket
            match = re.search('([-+]?\s?\d?)$', multiplier)

            #Numbers before the bracket
            outsideBrackets = multiplier[:match.start()]

            multiplier = multiplier[match.start(): match.end()].replace(" ", "")

            #If there's no digit before the bracket then the number is -+1
            if  not len(multiplier) or multiplier == "+" or multiplier == "-":
                multiplier =  -1 if multiplier == "-" else 1
            else:
                multiplier = int(multiplier)

            #Getting the numbers/variables in the brackets
            distributes =  equation.split("(")[1]


            #Return the distributed equation plus the numbers before the brackets
            return  outsideBrackets.replace(" ", "") + ''.join([

                "{0:+}".format(int(x) * multiplier) if x.isnumeric() else x if x.isalpha() else ""
                for x in distributes

            ]).replace(" ", "")


    def __reArrangeNumbers(self, equation):
        '''
        Storing constants on one side and variables/co-efficients on the other side
        :param equation:
        :return arranged equation:
        '''

        #Getting all the variables in the equation
        equationVariables =  list( set([

            x for x in  equation if x.isalpha()

        ]))


        equation = equation.split("=")

        newRHS = []
        newLHS = []

        for letter in equationVariables:

           #coefficients/variables on the LeftHand side of the equation
           for num in re.findall(r'[+-]?\w+', equation[0]):
                #Co-efficients/variables are stored on the left


               if letter in num:

                  newLHS.append(num)

              #Constants are stored on the right with their sign changed
               elif num.lstrip("+-").isdigit():

                    newRHS.append("{0:+}".format(-1 * int(num)))


           #constants are stored on the RightHand side of the equation
           for num in re.findall(r'[+-]?\w+', equation[1]):

               #Co-efficients/variables are stored on the left with their signs changed
               if letter in num:
                   newNum =  '{0:+}'.format(-1 * int(num.replace(letter, "") ) )
                   newLHS.append(newNum + letter)

               #Constants are stored on the right
               elif num.lstrip("+-").isdigit():

                   newRHS.append("{0:+}".format(int(num)))

        #Adding common factor on either side of the equation
        equation = self.__addCommonFactors("".join(newLHS)) + \
                   " = " + str(eval(self.__addCommonFactors("".join(newRHS))))

        if len(equation): print("\nRearrange")

        print(equation)

        return equation


    def __getSolution(self, equation):
        """
        Printing the final solution
        :param equation:
        :return: None
        """
        equation = equation.split("=")
        print("\nSolution")

        total = Fraction( eval(equation[1])  /  eval(equation[0][:-2]) ).limit_denominator()

        print(equation[0].strip()[-1] + " = " + str(total))



    def __addCommonFactors(self, equation):
        """
        Adding all the common variable/factors on one side of the equation
        :param equation:
        :return added equation:
        """

        #Getting all the operands in the equation
        operands = [
            op.replace(" ", "") +  "1" if not bool(re.search("\d", op)) else op.replace(" ", "")
            for op in re.findall('[+-]?\s?\w+', equation) ]


        #Getting the variables of the equation
        equationVariables =  list( set([

           x for x in  equation if x.isalpha()

        ]))


        #Dictionary of variable mapping to a list of its constants
        sumVariables = {}

        for letter in equationVariables:

            sumVariables[letter] = []

            for var in operands:
                if letter in var:


                    var = var.replace(letter, "")

                    start = re.search( '[+-]?\s?\d+', var).start()

                    end = re.search( '[+-]?\s?\d+', var).end()

                    sumVariables[letter].append( int( var[start: end]  ))


        #Getting sum of all the constants
        sumConstants = sum([
            int( x.replace(" ", "") ) for x in operands if x.replace(" ","").lstrip("+-").isdigit() ])

        total = ""

        for key, val in sumVariables.items():

            #Storing the sum of all common values and adding them to the total
            total +=  '{0:+}'.format(sum(val))   + key


        #Adding the sum of the constants to the sum of common variables
        if sumConstants != 0:
            total +=' {0:+}'.format(sumConstants).lstrip().strip()


        if total.strip() == "": total = "0"

        #For readability, making sure that the first number does not display the positive sign
        if len(total) and total[0] == "+":
            total = total.strip()[1:]

        return total

blu = Equation("3x + 6 = 5x")

# blu.Solve()