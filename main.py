import solver as ms

operation_set = ['+','-','*','/']
solve_for = 24
card_values = [2,2,3,10]

m24_problem = ms.m_problem_max(card_values,operation_set,solve_for, debug = True)
print(m24_problem.solver())