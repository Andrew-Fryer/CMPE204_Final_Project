from nnf import Var
from lib204 import Encoding

num_processors = 2
num_processes = 3
num_time_slots = 2 # adjust this and see if the formula is satisfiable
num_resources = 1

# This class simply instantiates variables (in the __init__ method) and then provides a clean way to access them (using the get method)
# This class represents all of the ways we can schedule the processes in the time slots on each of the processors
class Schedule:
  def __init__(self):
    self.schedule = {}

    for time in range(num_time_slots):
      for processor in range(num_processors):
        for process in range(num_processes):
          self.schedule[time, processor, process] = Var('schedule_' + str(time) + '_' + str(processor) + '_' + str(process))

  def get(self, time, processor, process):
    return self.schedule[time, processor, process]

# This class also instantiates variables and provides a way to access them
# This class holds all of the information about which processes use which resources.
# Generally, we will want to provide values for each of these variables and then see if a schedule exists that satisfies these requirements.
class Process_requirements:
  def __init__(self):
    self.table = {}
    for process in range(num_processes):
      for resource in range(num_resources):
        self.table[process, resource] = Var('req_' + str(process) + '_' + str(resource))

  def get(self, process, resource):
    return self.table[process, resource]

# Now, we instantiate one of each of the classes.
# So, we have:
s = Schedule() # a schedule
r = Process_requirements() # and information about which processes use which resources

# These are just for convienence below
T = Var('T')
F = Var('F')

def example_theory():
    E = Encoding()

    # Let's make sure that T is always true and F is always false :)
    E.add_constraint(T)
    E.add_constraint(~F)


    # Let's add constraints so that each process needs to run at least once:
    for process in range(num_processes):
      # We can build up a formula which is each variable that indicates that the process is runs at some time on some processor, all "or"ed together
      occurs = F
      for time in range(num_time_slots):
        for processor in range(num_processors):
          occurs = occurs | s.get(time, processor, process)
      # and now add that constraint
      E.add_constraint(occurs)

    # Let's add constraints so that each process cannot be run more than once:
    for process in range(num_processes):
      # We can keep track of each of the slots that a process could run on.
      # (A slot is time slot on a specific processor.)
      process_slots = []
      for time in range(num_time_slots):
        for processor in range(num_processors):
          process_slots.append(s.get(time, processor, process))
      # okay, we shoul have them all now...

      # So, for each slot the process could run in...
      for process_slot in process_slots:
        # We will build up a formula from each of the other process slots
        other_process_slots = filter(lambda x: x is not process_slot, process_slots)
        no_others = T
        for p in other_process_slots:
          no_others = no_others & ~p
        # The formula says that if the process is running in this slot, it is not running in any of the others.
        E.add_constraint(~process_slot | no_others)

    # Let's add constraints so that no 2 processes can run at the same time on the same processor:
    for p1 in range(num_processes):
      for p2 in range(p1 + 1, num_processes):
        for time in range(num_time_slots):
          for processor in range(num_processors):
            E.add_constraint(~s.get(time, processor, p1) | ~s.get(time, processor, p2))

    # Let's add constratints so that no 2 processes can use the same resource at the same time:
    for p1 in range(num_processes):
      for p2 in range(p1 + 1, num_processes):
        for resource in range(num_resources):
          E.add_constraint(~r.get(p1, resource) | ~r.get(p2, resource))

    # Finally, we can add constraints to tell the system which processes use which resources:
    # For example:
    # process 0 uses resource:
    E.add_constraint(r.get(0, 0))
    # process 1 also uses resource
    E.add_constraint(r.get(0, 0))
    # process 2 also uses resource
    E.add_constraint(r.get(0, 0))
    # (So, processes 0, 1, and 2, cannot be run concurrently)
    return E

if __name__ == "__main__":

    T = example_theory()

    print("\nSatisfiable: %s" % T.is_satisfiable())
    #print("# Solutions: %d" % T.count_solutions())
    print("solution:")
    solution = T.solve()
    for time in range(num_time_slots):
      for processor in range(num_processors):
        for process in range(num_processes):
          var_name = 'schedule_' + str(time) + '_' + str(processor) + '_' + str(process)
          print(var_name, solution[var_name])
    #print("   Solution: %s" % T.solve())
