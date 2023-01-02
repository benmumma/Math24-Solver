import solver as ms

operation_set = ['+', '-','*','/']
solve_for = 24
card_values = [12,10,2,13]

m24_problem = ms.m24_problem(card_values, operation_set, solve_for, debug=True)
print(m24_problem.solver())