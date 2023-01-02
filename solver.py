import numexpr
import itertools
import os


def printif(debug, statement):
  if debug:
    print(statement)


class m24_problem:
  # Create a class that stores the information about the Math 24 problem

  def __init__(self,
               nums,
               operations=['*', '/', '+', '-'],
               solve_value=24,
               debug=False):
    #Initialize the problem with a list of the numbers and a list of the operations allowed, as well as a numeric solve_value. The latter two are defaulted to the standard set of operations and 24.
    self.numbers = nums
    for i in self.numbers:
      i = str(i)
    self.card_as_string = str(self.numbers)
    self.operations = operations
    self.solve_value = solve_value
    self.solutions = []
    self.n_evaluated = 0
    self.debug = debug
    self.my_paths = []

  def create_possible_equations(self, level, history):
    #This function creates all possible equations to run given however many numbers you have. Each equation is represented with 4 elements in a list: the first two (0 and 1) are variables, the third element is the equation, and the fourth is a history store.
    #This function returns a list of those, e.g (with 3 numbers and just + and -):
    #[['a1', 'a2', 'a1+a2', False], ['a1', 'a2', 'a1-a2', False], ['a1', 'a2', 'a2-a1', False], ['a1', 'a3', 'a1+a3', False], ['a1', 'a3', 'a1-a3', False], ['a1', 'a3', 'a3-a1', False], ['a2', 'a3', 'a2+a3', False], ['a2', 'a3', 'a2-a3', False], ['a2', 'a3', 'a3-a2', False]]
    #So in the base case where you have only 2 numbers left, they are represented by a1 and a2, and there are up to 6 equations returned (a1+a2, a1*a2, a1-a2, a2-a1, a1/a2, and a2/a1). We exclude any cases where we would be dividing by zero.
    available_nums = []
    for i in range(1, len(self.numbers) + 1 - level):
      available_nums.append('a' + str(i))
    num_combos = list(itertools.combinations(available_nums, 2))
    equation_list = []

    for i in num_combos:
      for j in self.operations:
        if j == '+' or j == '*':
          equation_list.append(
            [i[0], i[1], str(i[0]) + str(j) + str(i[1]), history])
        else:
          if i[1] == 0 and j == '/':
            pass
          else:
            equation_list.append(
              [i[0], i[1], str(i[0]) + str(j) + str(i[1]), history])
          if i[0] == 0 and j == '/':
            pass
          else:
            equation_list.append(
              [i[0], i[1], str(i[1]) + str(j) + str(i[0]), history])
    #print(equation_list)
    return equation_list

  def create_all_paths(self, all_paths):
    #This function creates the possible equations at each level as lists, and then creates a big list of all possible paths by using the itertools chain and product functions. It does print then how many total paths are created.
    level_equations = []
    for level in range(0, len(self.numbers) - 1):
      level_equations.append(list(self.create_possible_equations(level,
                                                                 False)))
    all_paths = list(itertools.chain(itertools.product(*level_equations)))
    printif(self.debug, 'Created: ' + str(len(all_paths)) + ' paths!')
    return all_paths

  def math_calc_string(self, math_string):
    # This uses the numexpr package to evaluate a mathematical equation.
    return numexpr.evaluate(str(math_string)).item()

  def solver(self):
    # This is the meat of the program: the solver function. It:
    # Creates all possible equations using create_all_paths
    # Iterates through the paths and evaluates them

    #First, we create all paths:
    self.my_paths = self.create_all_paths([])

    #A path looks like this: for N numbers it contains N-1 elements. E.g.:
    #(['a1', 'a4', 'a1*a4', False], ['a1', 'a2', 'a1-a2', False], ['a1', 'a2', 'a1-a2', False])
    #Each element to a path has 4 parts: the two numbers, the equation step to try, and a history value (set to False at the start).

    #Now, for each path, we step through them:
    for path in self.my_paths:
      #print(path)
      #Start at equation 0, manage available numbers
      available_numbers = []
      for i in self.numbers:
        available_numbers.append(str(i))
      value = 0
      path_string = ''

      #Now we go through each i element within a path:
      for i in range(0, len(path)):
        #For a typical 4 number card, the length of the path is 4 and so this loop would execute at i=0,1,2, and 3.
        #We make a copy of the path element.
        equation = path[i].copy()
        #Replace numbers, evaluate each equation in order
        vals_to_remove = []
        #We sub out a1, a2, etc. for the actual numbers from the available_numbers array.
        #Thus, equation[2] represents the mathematical string we are going to evaluate (after the numbers are subbed in).
        for j in range(0, len(self.numbers) - i):
          string_to_replace = 'a' + str(j + 1)
          value_to_put_in = str(available_numbers[j])
          if string_to_replace in equation[2]:
            vals_to_remove.append(value_to_put_in)
            equation[2] = equation[2].replace(string_to_replace,
                                              value_to_put_in)
        #We now try to evaluate the value. If it exceeds 1 million, we assume the solution is not viable. This is done to avoid overflow errors especially when power operators are allowed.
        try:
          value = round(self.math_calc_string(equation[2]), 3)
          if value > 1000000:
            #printif(self.debug,"Hit value too high")
            break
          path_string += equation[2] + ' = ' + str(value) + ' \n'
        except:
          break
        #Update available numbers
        for val in vals_to_remove:
          #print('removing: '+val)
          available_numbers.remove(str(val))
        available_numbers.append(str(value))
        #Check if solved. If we get to the end of a path and the value is within a thousandth of the solve_value (typically 24), then the solving_path is set and the solution is returned to the screen.
        if i == len(path) - 1:
          if round(value, 3) == self.solve_value:
            solving_path = path
            return 'Card: '+self.card_as_string+' is solved!\n'\
        +'\nin '+str(self.n_evaluated)+' attempts'\
        +'\nSolution:\n'+path_string
          else:
            #Add up the number of failed iterations. Report back every 5,000.
            self.n_evaluated += 1
            if self.n_evaluated % 5000 == 0:
              printif(self.debug,
                      str(self.n_evaluated) + ' situations evaluated')
    return 'No solution found, bro! I tried ' + str(
      self.n_evaluated) + ' freaking options!'
