from nnf import Var
from lib204 import Encoding

num_processes = 2
num_resources = 2

def create_table_of_vars(prefix_char):
  return [[Var(prefix_char + str(i) + str(j)) for j in range(num_resources)] for i in range(num_processes)]

# Process has resource
h = create_table_of_vars('h')
#print(h)

# Process is waiting for resource
w = create_table_of_vars('w')

# Process may ask for resource (in maximum)
m = create_table_of_vars('m')

# These are just for convienence below
T = Var('T')
F = Var('F')

def example_theory():
    E = Encoding()

    E.add_constraint(T)
    E.add_constraint(~F)
    
    # holding is exclusive
    for j in range(num_resources):
      constraint = T
      for i in range(num_processes):
        constraint = constraint | ~h[i][j]
      print('holding is exclusive', constraint)
      E.add_constraint(constraint)

    for i in range(num_processes):
      for j in range(num_resources):
        # holding and waiting are mutually exclusive
        constraint = ~h[i][j] | ~w[i][j]
        print('holding and waiting are mutually exclusive', constraint)
        E.add_constraint(constraint)

        # holding implies max
        constraint = ~h[i][j] | m[i][j]
        print('holding implies max', constraint)
        E.add_constraint(constraint)

        # waiting implies max
        constraint = ~w[i][j] | m[i][j]
        print('waiting implies max', constraint)
        E.add_constraint(constraint)
    
      # hard code 2 processes and 2 resources for now:
      # These constraints ensure that the system is in a safe state
      E.add_constraint(~m[0][0] | ~h[1][0] | ~m[1][1] | ~h[0][1])
      E.add_constraint(~m[0][1] | ~h[1][1] | ~m[1][0] | ~h[0][0])

    return E

if __name__ == "__main__":

    T = example_theory()

    print("\nSatisfiable: %s" % T.is_satisfiable())
    print("# Solutions: %d" % T.count_solutions())
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        print(" %s: %.2f" % (vn, T.likelihood(v)))
    print()
