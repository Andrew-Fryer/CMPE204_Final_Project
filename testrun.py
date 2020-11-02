
from nnf import Var
from lib204 import Encoding

# ---------------------------------GOAL---------------------------------------------------------
# The goal here was to use propositional logic and deduction to figure out how to schedule two processes with their critical
# sections, onto a CPU with 2 cores.
# So essentially, there are two mini processors that can run in parallel.
# The problem contains the following:
# process 1:
#     has 2 critical sections: p1_crit_sect1 and p1_crit_sect2
# process 2:
#     has 2 critical sections: p2_crit_sect1 and p2_crit_sect2

# Also have two shared resources: r1 and r2
# A critcal section can make use of only one shared resource.
# Critical sections that make use of the same shared resource will have to be scheduled (ie cannot run in parallel)

# The deduction will use propositions to determine which critical sections need to be scheduled and which sections can 
# run in parallel. This will generate the following proposition

# -----------------------------------------PROCESS 1 SEGMENT PROPOSITIONS ----------------------------------------
# For process 1 segment propositions, we will use the letter a
# p1_crit_sect1 is denoted by a1 and p1_crit_sect2 is denoted by a2,
# these proposition address the different possibilities for resource use by the critical sections

a11 = Var('a11') #true if p1_crit_sect1 uses r1
a12 = Var('a12') #true if p1_crit_sect1 uses r2
a21 = Var('a21') #true if p1_crit_sect2 uses r1
a22 = Var('a22') #true if p1_crit_sect2 uses r2

# -----------------------------------------PROCESS 2 SEGMENT PROPOSITIONS ----------------------------------------
# For process 2 segment propositions, we will use the letter b
# p2_crit_sect1 is denoted by b1 and p2_crit_sect2 is denoted by b2,
# these proposition address the different possibilities for resource use by the critical sections

b11 = Var('b11') #true if p2_crit_sect1 uses r1
b12 = Var('b12') #true if p2_crit_sect1 uses r2
b21 = Var('b21') #true if p2_crit_sect2 uses r1
b22 = Var('b22') #true if p2_crit_sect2 uses r2

# ------------------------------RESOURCE 1 SCHEDULING PROPOSTIONS------------------------------------------


# So originally we had the following:
#     q was used to represent resource scheduling for resource 1, and the number subscripts are for:
#     (1) a11, (2) a21, (3) b11, (4) b21

#     Since all the above propositions stand for critical sections that make use of the same resource,
#     r1 then we would have to schedule them if they are true
#     therefore the different ways/possibilities of scheduling

    q12 = Var('q12') #true if a11 is scheduled before a21,
    q13 = Var('q13') #true if a11 is scheduled before b11
    q14 = Var('q14') #true if a11 is scheduled before b21
    q21 = Var('q21') #true if a12 is scheduled before a11
    q23 = Var('q23') #true if a12 is scheduled before b11
    q24 = Var('q24') #true if a12 is scheduled before b21
    q31 = Var('q31') #true if b11 is scheduled before a11
    q32 = Var('q32') #true if b11 is scheduled before a21
    q34 = Var('q34') #true if b11 is scheduled before b21 
    q41 = Var('q41') #true if b21 is scheduled before a11
    q42 = Var('q42') #true if b21 is scheduled before a21
    q43 = Var('q43') #true if b21 is scheduled before b11

# ------------------------------RESOURCE 2 SCHEDULING PROPOSTIONS------------------------------------------
#similar thing for resource 1, now r2 is represented by p
# (1) a12, (2) a22, (3) b12, (4) b22
p12 = Var('p12')
p13 = Var('p13')
p14 = Var('p14')
p21 = Var('p21')
p23 = Var('p23')
p24 = Var('p24')
p31 = Var('p31')
p32 = Var('p32')
p34 = Var('p34')
p41 = Var('p41')
p42 = Var('p42')
p43 = Var('p43')

#
# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    E = Encoding()
    
    # if a11 is scheduled before a21 then it cant be the case
    #that a21 is scheduled before a11, not possible
    E.add_constraint(~q12 | ~q21)
    E.add_constraint(~q13 | ~q31)
    E.add_constraint(~q14 | ~q41)
    E.add_constraint(~q23 | ~q32)
    E.add_constraint(~q24 | ~q42)
    E.add_constraint(~q34 | ~q43)

    #same for resource 2
    E.add_constraint(~p12 | ~p21)
    E.add_constraint(~p13 | ~p31)
    E.add_constraint(~p14 | ~p41)
    E.add_constraint(~p23 | ~p32)
    E.add_constraint(~p24 | ~p42)
    E.add_constraint(~p34 | ~p43)

    #and implication constraints for the resources
    E.add_constraint( (~a11 | ~a21) | (q12 | q21) )
    E.add_constraint( (~a11 | ~b11) | (q13 | q31) )
    E.add_constraint( (~a11 | ~b21) | (q14 | q41) )
    E.add_constraint( (~a21 | ~b11) | (q23 | q32) )
    E.add_constraint( (~a21 | ~b21) | (q24 | q42) )
    E.add_constraint( (~b11 | ~b21) | (q34 | q43) )

    E.add_constraint( (~a12  | ~a22) | (p12 | p21) )
    E.add_constraint( (~a12  | ~b12) | (p13 | p31) )
    E.add_constraint( (~a12  | ~b22) | (p14 | p41) )
    E.add_constraint( (~a22  | ~b12) | (p23 | p32) )
    E.add_constraint( (~a22  | ~b22) | (p24 | p42) )
    E.add_constraint( (~b12  | ~b22) | (p34 | p43) )


    return E


if __name__ == "__main__":

    T = example_theory()

    print("\nSatisfiable: %s" % T.is_satisfiable())
    print("# Solutions: %d" % T.count_solutions())
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    # for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
    #     print(" %s: %.2f" % (vn, T.likelihood(v)))
    # print()
