from nnf import Var
from lib204 import Encoding
from nnf import NNF
from nnf.operators import iff
import math
import time

def implication(l, r):
    return l.negate() | r

def neg(f):
    return f.negate()

def split(word): 
    return [char for char in word] 

def getMaxSlot(solution):
  #need to find the maximum slot, first create reverse array
  reverse_slots=[]
  for timeslot in reversed(range(num_time_slots)):
    reverse_slots.append(timeslot)

  maxslotFound = False
  for timeslot in reverse_slots:
    for processor in range(num_processors):
      for process in range(num_processes):
        num_code_blocks = code_blocks_for_processes[process]
        for code_block in range(num_code_blocks):
          var_name = 'schedule_' + str(timeslot) + '_' + str(processor) + '_' + str(process) + '_' + str(code_block);
          var_solution = solution[var_name]
          if var_solution:
            maxslotFound = True
            break

        if maxslotFound:
          break

      if maxslotFound:
        break

    if maxslotFound:
      break

  return timeslot

NNF.__rshift__ = implication
NNF.__invert__ = neg
# ^ this is a gift from Muise... thank-you!

num_processors = 3
num_processes = 4
num_resources = 3


code_blocks_for_processes= [3, 2, 2, 4]
#index of element corresponds to number of code blocks for the process
#ie proc 0 has 3 code blocks
#ie proc 1 has 3 code blocks
#ie proc 2 has 3 code blocks
#so in this case we have three block per process, but this will not 
#always be the case, can be adapted to match different process requirements


#in the order of proc 0 cb 0, proc 0, cb 1 and so on
    #numbers indicate the index of resources they will be using
    #x indicates no resource use
    #for resource listing: order does not matter, just has to be spaced
cb_resc_use_array = [
    "1 2" ,  #proc 0 cb 0 uses r0, r1, r2 
    "0",       #proc 0 cb 1 uses no resources
    "2",       #proc 0 cb 2 uses r0

    "2 0",       #proc 1 cb 0 uses r0
    "x",     #proc 1 cb 1 uses  r0
    #"x",       #proc 1 cb 2 uses no resources

    "1",     #proc 2 cb 0 uses r1, r2
    "1",     #proc 2 cb 1 uses r0, r1
    #"0"    #proc 2 cb 2 uses r0, r1, r2

    "0 1 2",     #proc 2 cb 0 uses r1, r2
    "x",     #proc 2 cb 1 uses r0, r1
    "0",    #proc 2 cb 2 uses r0, r1, r2
    "1 0"    #proc 2 cb 2 uses r0, r1, r2
    ]

#num of time slots will have to be adjusted to match the maximum case, ie all code blocks on one processor
#therefore num of time slots will be the total number of code blocks we have in the system
num_time_slots = 0 # adjust this and see if the formula is satisfiable
for i in code_blocks_for_processes:
  num_time_slots = num_time_slots + i
  #complete the cumulative sum




# This class simply instantiates variables (in the __init__ method) and then provides a clean way to access them (using the get method)
# This class represents all of the ways we can schedule the processes in the time slots on each of the processors
class Schedule:
  def __init__(self):
    self.schedule = {}

    #why time first, lets use processors:
    for time in range(num_time_slots):
      for processor in range(num_processors):
        for process in range(num_processes):
          #process will be index of current process, use to get number of code blocks
          process_code_blocks_num = code_blocks_for_processes[process]

          for code_block in range(process_code_blocks_num):
            self.schedule[time, processor, process, code_block] = Var('schedule_' + str(time) + '_' + str(processor) + '_' + str(process) + '_' + str(code_block))

  def get(self, time, processor, process, code_block):
    return self.schedule[time, processor, process, code_block]

# This class also instantiates variables and provides a way to access them
# This class holds all of the information about which processes use which resources.
# Generally, we will want to provide values for each of these variables and then see if a schedule exists that satisfies these requirements.
class Process_requirements:
  def __init__(self):
    self.table = {}

    #will be handling resource allocation
    #each block has a proposition for the resources they are using.

    for process in range(num_processes):
      #retrieve number of code blocks for given process
      process_code_blocks_num = code_blocks_for_processes[process]
      for code_block in range(process_code_blocks_num):
        #now define the resource proposition choices for a given code block
        for resource in range(num_resources):
          self.table[process, code_block, resource] = Var('req_' + str(process) + '_' + str(code_block)+ '_' + str(resource))

  def get(self, process, code_block, resource):
    return self.table[process, code_block, resource]

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


    #set up resource propositions
    #use these to set up the constraints
    arr_index = 0
    for process in range(num_processes):
      num_code_blocks = code_blocks_for_processes[process]
      for code_block in range(num_code_blocks):

        is_cb_using_resc = []
        for resource in range(num_resources):
          is_cb_using_resc.append(0)

        #now we use the cb_resc_use_array to set appropriate values to true
        #print(str(arr_index))
        used_rescs = cb_resc_use_array[arr_index].split()
        #split will split by spaces
        #used rescs will be an array of resources being used by the code block
        for used_resc in used_rescs:
          if used_resc != "x":
            usedresc_index = int(used_resc)
            #since int can use directly in code
            # print(used_rescs)
            # print("For process "+str(process)+", code block "+str(code_block)+", resource:"+str(used_resc))
            is_cb_using_resc[usedresc_index] = 1
            #ie resources that are used set to true, resources that are not used will remain false
            #1 is true, 0 is false

        #finally implement constraints using the array
        for resource in range(num_resources):
          is_used = is_cb_using_resc[resource]
          cur_rec_prop = r.get(process, code_block, resource)
          if is_used == 1:
            #then add truth constraint for that resource
            E.add_constraint(cur_rec_prop)
          else:
            #so it is false constraint so add it
            E.add_constraint(~cur_rec_prop)

        #now increment the array index for the next code block
        arr_index = arr_index +1

    #adapting so that each process code block needs to run at least once
    for process in range(num_processes):
      num_code_blocks = code_blocks_for_processes[process]
      for code_block in range(num_code_blocks):
        occurs = F
        for time in range(num_time_slots):
          for processor in range(num_processors):
            occurs = occurs | s.get(time, processor, process, code_block);
        E.add_constraint(occurs);

    # Let's add constraints so that each process code block cannot be run more than once:
    for process in range(num_processes):
      # We can keep track of each of the slots that a process code block could run on.
      # (A slot is time slot on a specific processor.)
      num_code_blocks = code_blocks_for_processes[process]

      for code_block in range(num_code_blocks):
        code_block_slots = []

        #iterate to generate all the propositions for the different code block slots.
        for time in range(num_time_slots):
          for processor in range(num_processors):
            code_block_slots.append(s.get(time, processor, process, code_block))
        # okay, we shoul have them all now...

        # So, for each slot the process could run in...
        for slot in code_block_slots:
          # We will build up a formula from each of the other process slots
          other_slots = filter(lambda x: x is not slot, code_block_slots)
          no_others = T
          for p in other_slots:
            no_others = no_others & ~p
          # The formula says that if the process is running in this slot, it is not running in any of the others.
          E.add_constraint(~slot | no_others)

    # Let's add constraints so that no 2 process code blocks can run at the same time on the same processor:
    for p1 in range(num_processes):
      #two code blocks cannot run at the same time on the same processor, 
      #so for a given code block 
      num_code_blocks = code_blocks_for_processes[p1]
      for c1 in range(num_code_blocks):
        #this is the one we are matching the rest two
        #need to implement it against the other processes
        for p2 in range(num_processes):
          num_code_blocks2 = code_blocks_for_processes[p2]
          #retrieve number of code blocks for the given process
          for c2 in range(num_code_blocks2):
            #need to eliminate the case where we compare c1 to itself
            if p1 == p2 and c1 == c2:
              #we are with the same code block of the same process so do not add constraint
              0
            else:
              #do the constrain addition
              for time in range(num_time_slots):
                for processor in range(num_processors):
                  E.add_constraint(~s.get(time, processor, p1, c1) | ~s.get(time, processor, p2, c2))


    # Let's add constraints so that no 2 process code blocks can use the same resource at the same time step:
    for p1 in range(num_processes):
      #two code blocks cannot run at the same time on the same processor, 
      #so for a given code block 
      num_code_blocks = code_blocks_for_processes[p1]
      for c1 in range(num_code_blocks):
        #this is the one we are matching the rest two
        #need to implement it against the other processes
        for p2 in range(num_processes):
          num_code_blocks2 = code_blocks_for_processes[p2]
          #retrieve number of code blocks for the given process
          for c2 in range(num_code_blocks2):
            #need to eliminate the case where we compare c1 to itself
            if p1 == p2 and c1 == c2:
              #we are with the same code block of the same process so do not add constraint
              0;
            else:
              #do the constrain addition
              for resource in range(num_resources):
                for time in range(num_time_slots):

                  p1_c1_running_at_this_time = F
                  for processor in range(num_processors):
                    p1_c1_running_at_this_time = p1_c1_running_at_this_time | s.get(time, processor, p1, c1)

                  p1_c1_using_resource = r.get(p1, c1, resource) & p1_c1_running_at_this_time

                  p2_c2_running_at_this_time = F
                  for processor in range(num_processors):
                    p2_c2_running_at_this_time = p2_c2_running_at_this_time | s.get(time, processor, p2, c2)

                  p2_c2_using_resource = r.get(p2, c2, resource) & p2_c2_running_at_this_time

                  E.add_constraint(~p1_c1_using_resource | ~p2_c2_using_resource)


    #constraint so that code blocks of a process run in order
    #in this case for a given code block k on timestep t, all earlier code blocks  (c_0 to c_k-1)
    #must be on timestep 0 to t-1, ie they cannot be on timestep t to n
    #including t because k might have a dependency on k-1
    for process in range(num_processes):
      num_code_blocks = code_blocks_for_processes[process]
      for c1 in range(num_code_blocks):
        #prompt = "\n\nFor PROCESS "+str(process)+"; CODE BLOCK "+str(c1)+":"
        #print(prompt)
        #prompt = "If p"+str(process)+"_cb"+str(c1)" is true, then:"
        #suppose we are dealing with code block k
        #other code blocks 1 to k should be behind it in time steps
        #irrespective of what processor it is
        #so if k is true for a given time step t
        #then code blocks 0 to k-1 cannot be true for timesteps t to n
        # t is included because, if k is running on timestep t
        for t1 in range(num_time_slots):
          c1_at_t1 = T;
          #prompt = "\nIf cb"+str(c1)+" at timestep "+str(t1)+" is true, then:"
          #print(prompt)
          #t1 is the timeslot that c1 is in
          #so bring back other code blocks below it
          ealier_blocks_not_on_later_slots = T;
          for c_prev in range(0,c1):
            for t2 in range(t1, num_time_slots):
              for processor2 in range(num_processors):
                #prompt = "Then cb"+str(c_prev)+" at timestep "+str(t2)+" on processor "+str#(processor2)+" should be false"
                #print(prompt)
                #prompt = "Current value for above:"
                #print(prompt)
                #print(s.get(t2, processor2, process, c_prev))
                ealier_blocks_not_on_later_slots = ealier_blocks_not_on_later_slots & neg(s.get(t2, processor2, process, c_prev))
                #if c1_t1 is true, then the rest of the ealier code blocks (c0 to c1-1) should not be 
                #in any later time block (t1+1 to tn) in any processor, they must run either sequentially 
          #now add the constraint in the case
          c1_at_t1 = F
          for processor in range(num_processors):
            c1_at_t1 = c1_at_t1 | s.get(t1, processor, process, c1);
          #p->q ie ~p | q
          #if c1_at_t1 is true, then all other ealier code blocks on later time steps in any processor should be false
          E.add_constraint(~c1_at_t1 | ealier_blocks_not_on_later_slots)
          #end t1 num_time_slots loop



    #if block k is on time step t, then blocks k+1 to n cannot be on timestep 0 to timestep t
    #this is in part covered by the previous constraint however it does not cover the case for code block 0

    for process in range(num_processes):
      #only have to do one codeblock c0
      c0 = 0
      num_code_blocks = code_blocks_for_processes[process]
      
      for t1 in range(num_time_slots):
        #for processor in range(num_processors):
        #t1 is the time slot c0 is in 
        later_blocks_not_on_earlier_slots = T
        for cb_ahead in range(1,num_code_blocks):
          #cannot be in time step less than or equal to t
          for t2 in range(0,t1):
            #t2 is timesteps less than or equal to t
            for processor2 in range(num_processors):
              later_blocks_not_on_earlier_slots = later_blocks_not_on_earlier_slots & neg(s.get(t2,processor2,process,cb_ahead))
              #so they cannot be in timesteps before time step block 0 is in so those schedule propositions must be false
        c0_at_t1= F     
        for processor in range(num_processors):
          c0_at_t1 = c0_at_t1 | s.get(t1,processor,process,c0)
        #if c0_at_t1 is true, then later code blocks 1ton cannot be on t0 to t1
        E.add_constraint(~c0_at_t1 | later_blocks_not_on_earlier_slots)

    return E

if __name__ == "__main__":

    T = example_theory()

    print("\nSatisfiable: %s" % T.is_satisfiable())
    if T.is_satisfiable:
      print("Attempting to find optimum solution.....");
      #print("# Solutions: %d" % T.count_solutions())
      
      #find optimum by performing trial and error
      #assume optimum is where tasks are split equally across processors,
      #so maximum slot should be total time slot divided by the number of processors
      start = time.time()
      T.solve()
      end = time.time()
      elapsed = end-start
      trials = math.ceil(2.71828**(0-(elapsed-5)))
      print("Estimated Number of Trials Per Step: "+str(trials))
      
      optimumMaxSlot = math.ceil(num_time_slots / num_processors);
      solutionFound = False
      final_solution = []
      while solutionFound == False:
        #print("Attempting Optimum Maximum Slots: "+str(optimumMaxSlot))
        for i in range(0,trials):
          #for a given minimum time slot, try 100 different solutions 
          solution= T.solve()
          #for a given solution get maxslot
          maxSlot = getMaxSlot(solution)+1
          if maxSlot <= optimumMaxSlot:
            #if the number of max slots for this solution is less than or equal to our guessed
            #minimum then we have found a somewhat optimum solution so 
            solutionFound = True;
            final_solution = solution;
            break
          #otherwise continue iterating

        #if no solution is found for that minimum, then increment our optimum slots by 1 and try again
        if solutionFound == False:
          optimumMaxSlot += 1;

        #while loop will always be satisfied since optimum max slot will eventually be incremented to 
        # a do able value

      print("Estimated Optimum Solution Highest Slot Index: "+str(maxSlot-1))
      print("Proposition Truth Values:")
      solution = final_solution;

      #put the solution in schedule form
      procrs_arrays = []
      timeslot_header = []
      timeslot_header.append("Timeslots")
      for t in range(num_time_slots):
        timeslot_header.append("T"+str(t))

      for i in range(num_processors):
        newarray = []
        for t in range(num_time_slots):
          #create processor array with timeslot places
          newarray.append("-")
        procrs_arrays.append(newarray)
        #add that to array of processor arrays

      for timeslot in range(num_time_slots):
        for processor in range(num_processors):
          processor_array = procrs_arrays[processor]
          for process in range(num_processes):
            num_code_blocks = code_blocks_for_processes[process]
            for code_block in range(num_code_blocks):
              var_name = 'schedule_' + str(timeslot) + '_' + str(processor) + '_' + str(process) + '_' + str(code_block)
              var_solution = solution[var_name]
              print(var_name+": "+str(var_solution))

              #now perform check to see where it should go
              if var_solution == True:
                #if it is true then put a value for the corresponding timeslot on the corresponding processor
                processor_array[timeslot] = "p"+str(process)+"_cb"+str(code_block)

      #print resouce usage statistics
      print()
      print("Resource Usage Statistics:")
      arr_index = 0
      for process in range(num_processes):
        print("-------------")
        num_code_blocks = code_blocks_for_processes[process]
        for code_block in range(num_code_blocks):
          prompt="p"+str(process)+"_cb"+str(code_block)+" uses: "
          is_cb_using_resc = []
          for resource in range(num_resources):
            is_cb_using_resc.append(0)

          #now we use the cb_resc_use_array to set appropriate values to true
          used_rescs = cb_resc_use_array[arr_index].split()
          #split will split by spaces
          #used rescs will be an array of resources being used by the code block
          for used_resc in used_rescs:
            if used_resc != "x":
              prompt = prompt+"r"+used_resc+", "
            else:
              prompt = prompt+"no resources"

          #now increment the array index for the next code block
          print(prompt)
          arr_index = arr_index +1

      #now print schedule to console or ouptut
      print()
      print("In Schedule Format:")
      header_prompt = timeslot_header[0]+"\t"
      for t in range(1,len(timeslot_header)):
        header_prompt = header_prompt+timeslot_header[t]+"\t"
      print(header_prompt)

      for arr_index in range(len(procrs_arrays)):
        proc_prompt = "P"+str(arr_index)+"\t"
        procr_array = procrs_arrays[arr_index]

        for value in procr_array:
          proc_prompt = proc_prompt + value +"\t"

        print(proc_prompt) 


      #print("   Solution: %s" % T.solve())
    else:
      print("no valid solution")

    