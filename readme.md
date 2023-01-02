### Math 24 Solver 

This is a fairly basic script that can solve Math 24 cards. It is reasonably abstacted such that it can handle more than 4 numbers, other operations (e.g. mod or powers) and solve for an arbitrary number other than 24.

The solver.py file contains the m24_problem class which creates an object that refelects a single card or problem.

To use this as seen in the main.py file, you can instantiate a m24_problem with a list of numbers (typically 4), and optionally a solve value and a set of allowed operators. Then, you can run the m24_problem's solver function to obtain the result.

The solver function operationally creates a list of all potential paths by which it could solve a card. It then iterates through these until a solution is found. Because the initial number of paths scales exponentially with more numbers included, we recommend not to extend past six numbers.