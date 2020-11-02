from nnf import Var
from lib204 import Encoding

num_processes = 2
num_resources = 2

def create_table_of_vars(prefix_char):
  return [[Var(prefix_char + str(i) + str(j)) for i in range(num_processes)] for j in range(num_resources)]

# Process has resource
h = create_table_of_vars('h')
print(h)

# Process is waiting for resource
w = create_table_of_vars('w')

# Process may ask for resource (in maximum)
m = create_table_of_vars('m')

# Process may be blocked, waiting for resource
#x = create_table_of_vars('x')

# If the system is safe now, then it is safe to run process
s = [Var('s' + str(i)) for i in range(num_processes)]
print(s)

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
      print(constraint)
      E.add_constraint(constraint)

    # holding and waiting are mutually exclusive
    for i in range(num_processes):
      for j in range(num_resources):
        E.add_constraint(~h[i][j] | ~w[i][j])
    
    # hij -> mij and wij -> mij

    # define xij in terms of hij and mij
#    for i in range(num_processes):
#      for j in range(num_resources):
#        print('todo')

    # circular wait creates an unsafe state

    for i in range(num_processes):
      process_is_safe = T
      for j in range(num_resources):
        resoure_is_allocated = F
#        for k in range(num_processes):
#          resource_is_allocated = resource_is_allocated | h[k][j]
#        process_may_be_stopped_by_resource = m[i][j] & (resource_is_allocated & ~h[i][j])
        # Wrap this in a function for deeper cycles
        for k in range(num_processes):
          for l in range(num_resources):
            # this only does cycles of length 2...
            process_is_safe = process_is_safe & m[i][j] & h[k][j] & w[k][l] & h[i][l]
      # s[i] = process_is_safe
      E.add_constraint(~s[i] | process_is_safe)
      #E.add_constraint(~process_is_safe | s[i])
      print('process', i, 'is safe:', process_is_safe)


    return E

def asdf(list_of_constraints):
  res = []
  for i in range(num_processes):
    for j in range(num_resources):
      res += map(lambda c : c & h & w, list_of_constraints)
  return res

# this generates a list of cycles
# where a cycle is a list of processes
def generate_cycles(length):
  if length == 1:
    return [[p] for p in range(num_processes)]
  res = []
  for c in generate_cycles(length - 1):
    for i in range(num_processes):
      res.append(c + [i])
  return res

print('cycles 4:', generate_cycles(4))

def cycle_to_constraint():
  constraint = T
  for p in l:
    constraint = constraint 


if __name__ == "__main__":

    T = example_theory()

    print("\nSatisfiable: %s" % T.is_satisfiable())
    print("# Solutions: %d" % T.count_solutions())
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        print(" %s: %.2f" % (vn, T.likelihood(v)))
    print()
