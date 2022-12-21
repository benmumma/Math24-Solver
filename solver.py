import numexpr
import itertools

import os

def printif(debug,statement):
    if debug:
        print(statement)

class m_problem_max:
    def __init__(self,nums,operations,solve_value, debug = False):
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
    
    def create_possible_equations(self, level,history):
        available_nums = []
        for i in range(1,len(self.numbers)+1-level):
            available_nums.append('a'+str(i))
        num_combos = list(itertools.combinations(available_nums, 2))
        equation_list = []
        for i in num_combos:
            for j in self.operations:
                if j == '+' or j == '*':
                    equation_list.append([i[0],i[1],str(i[0])+str(j)+str(i[1]),history])
                else: 
                    if i[1] == 0 and j == '/':
                        pass
                    else:
                        equation_list.append([i[0],i[1],str(i[0])+str(j)+str(i[1]),history])
                    if i[0] == 0 and j == '/':
                        pass
                    else:
                        equation_list.append([i[0],i[1],str(i[1])+str(j)+str(i[0]),history])
        return equation_list
    
    def create_all_paths(self, all_paths):
        level_equations = []
        for level in range(0,len(self.numbers)-1):
                level_equations.append(list(self.create_possible_equations(level,False)))
        all_paths = list(itertools.chain(itertools.product(*level_equations)))
        printif(self.debug,'Created: '+str(len(all_paths))+' paths!')
        return all_paths
    
    def math_calc_string(self, math_string):
        return numexpr.evaluate(str(math_string)).item()
     
    def solver(self):
        self.my_paths = self.create_all_paths([])
        for path in self.my_paths:
            #Start at equation 0, manage available numbers
            available_numbers = []
            for i in self.numbers:
                available_numbers.append(str(i))
            value = 0
            path_string = ''
            for i in range(0,len(path)):
                equation = path[i].copy()
                #Replace numbers, evaluate each equation in order
                vals_to_remove = []
                for j in range(0,len(self.numbers)-i):
                    string_to_replace = 'a'+str(j+1)
                    value_to_put_in = str(available_numbers[j])
                    if string_to_replace in equation[2]:
                        vals_to_remove.append(value_to_put_in)
                        equation[2] = equation[2].replace(string_to_replace,value_to_put_in)
                try:
                    value = round(self.math_calc_string(equation[2]),3)
                    if value > 100000:
                        #printif(self.debug,"Hit value too high")
                        break
                    path_string += equation[2]+' = '+str(value)+' \n'
                except:
                    break
                #Update available numbers
                for val in vals_to_remove:
                    #print('removing: '+val)
                    available_numbers.remove(str(val))
                available_numbers.append(str(value))
                #Check if solved:
                if i == len(path)-1:
                    if round(value,3) == self.solve_value:
                        solving_path = path
                        return 'Card: '+self.card_as_string+' is solved!\n'\
                    +'\nin '+str(self.n_evaluated)+' attempts'\
                    +'\nSolution:\n'+path_string
                    else:
                        #print('End Iteration.')
                        self.n_evaluated += 1
                        if self.n_evaluated%5000 == 0:
                            printif(self.debug,str(self.n_evaluated)+' situations evaluated')
        return 'No solution found, bro! I tried '+str(self.n_evaluated)+' freaking options!'