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

# Process may be blocked, waiting for resource
#x = create_table_of_vars('x')

# If the system is safe now, then it is safe to run process
s = [Var('s' + str(i)) for i in range(num_processes)]
#print(s)

#after looking at s, don't pick a process that is waiting for anythin...

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
    
    # circular wait creates an unsafe state
    for c in generate_circular_wait_constraints():
      E.add_constraint(c)
      print('circular', c)

    return E

# this generates a list of cycles
# where a cycle is a list of processes
# todo: don't allow duplicates
def generate_cycle_list_up_to_length(length):
  cycle_list_to_one_less = [[p] for p in range(num_processes)]
  res = [] # note that cycle lists of length 1 are excluded
  for n in range(length):
    cycle_list = []
    for c in cycle_list_to_one_less:
      for i in (x for x in range(num_processes) if x not in c):
        cycle_list.append(c + [i])
    cycle_list_to_one_less = cycle_list
    res += cycle_list
  return res
#print('cycles 4:', generate_cycle_list_up_to_length(4))

# todo: don't allow duplicates
def generate_lists_of_resources(length, j):
  if length == 1:
    return [[j]]
  prev_list = generate_lists_of_resources(length - 1, j)
  res = []
  for l in prev_list:
    for r in range(num_resources):
      res.append(l + [r])
  return res
#print('lists of 4 resources', generate_lists_of_resources(4))

class Cycle:
  def __init__(self, list_of_processes, list_of_resources):
    assert len(list_of_processes) == len(list_of_resources) + 1
    self.processes = list_of_processes
    self.resources = list_of_resources

  def toConstraint(self):
    constraint = h[self.processes[0]][self.resources[0]]
    for i in range(1, len(self.processes)):
      prev_proc = self.processes[i-1]
      proc = self.processes[i]
      res = self.resources[i-1]
      constraint = constraint & w[prev_proc][res] & h[proc][res]
    return constraint

def cycle_list_to_constraints(cycle_list, j):
  assert len(cycle_list) > 1
  return [Cycle(cycle_list, resource_list).toConstraint() for resource_list in generate_lists_of_resources(len(cycle_list) - 1, j)] # todo make more efficient
#print('constraint for [0, 1, 0]', cycle_list_to_constraints([0, 1, 0]))

def generate_circular_wait_constraints():
  constraints = []
  for i in range(num_processes):
    for j in range(num_resources):
      for c in helper(j):
        constraints.append(~h[i][j] & m[i][j] & c)
  return constraints

def helper(j):
  constraints = []
  for cycle_list in generate_cycle_list_up_to_length(num_processes):
    constraints += cycle_list_to_constraints(cycle_list, j)
  return constraints

if __name__ == "__main__":

    T = example_theory()

    print("\nSatisfiable: %s" % T.is_satisfiable())
    print("# Solutions: %d" % T.count_solutions())
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        print(" %s: %.2f" % (vn, T.likelihood(v)))
    print()
