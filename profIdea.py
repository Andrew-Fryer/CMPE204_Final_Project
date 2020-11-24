from nnf import Var
from lib204 import Encoding

num_processors = 2
num_processes = 4
num_time_slots = 2 # adjust this and see if the formula is satisfiable
num_resources = 4

class Schedule:
  def __init__(self):
    self.schedule = {}

    for time in range(num_time_slots):
      for processor in range(num_processors):
        for process in range(num_processes):
          self.schedule[time, processor, process] = Var('schedule_' + str(time) + '_' + str(processor) + '_' + str(process))

  def get(self, time, processor, process):
    return self.schedule[time, processor, process]

class Process_requirements:
  def __init__(self):
    self.table = {}
    for process in range(num_processes):
      for resource in range(num_resources):
        self.table[process, resource] = Var('req_' + str(process) + '_' + str(resource))

  def get(self, process, resource):
    return self.table[process, resource]

s = Schedule()
r = Process_requirements()

# These are just for convienence below
T = Var('T')
F = Var('F')

def example_theory():
    E = Encoding()

    E.add_constraint(T)
    E.add_constraint(~F)


    # each process needs to run
    for process in range(num_processes):
      occurs = F
      for time in range(num_time_slots):
        for processor in range(num_processors):
          occurs = occurs | s.get(time, processor, process)
      E.add_constraint(occurs)

    # each process should only run once
    for process in range(num_processes):
      process_slots = []
      for time in range(num_time_slots):
        for processor in range(num_processors):
          process_slots.append(s.get(time, processor, process))
      for time in range(num_time_slots):
        for processor in range(num_processors):
          this_process_slot = s.get(time, processor, process)
          other_process_slots = filter(lambda x: x is not this_process_slot, process_slots)
          no_others = T
          for p in other_process_slots:
            no_others = no_others & ~p
          E.add_constraint(~this_process_slot | no_others)

    # no 2 processes can run at the same time on the same processor
    for p1 in range(num_processes):
      for p2 in range(p1 + 1, num_processes):
        for time in range(num_time_slots):
          for processor in range(num_processors):
            E.add_constraint(~s.get(time, processor, p1) | ~s.get(time, processor, p2))

    # no 2 processes can use the same resource at the same time
    for p1 in range(num_processes):
      for p2 in range(p1 + 1, num_processes):
        for resource in range(num_resources):
          E.add_constraint(~r.get(p1, resource) | ~r.get(p2, resource))

    return E

if __name__ == "__main__":

    T = example_theory()

    print("\nSatisfiable: %s" % T.is_satisfiable())
    #print("# Solutions: %d" % T.count_solutions())
    print("   Solution: %s" % T.solve())
