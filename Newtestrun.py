
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
# These are the propositions used to tell us which critical sections need to go before the other.
# This is where the confusion really starts. Originally the idea was to have a proposition, for saying
# which way the the critical sections are scheduled, but what we only need is a propositon to say that 
# a pair of critical sections need to be scheduled.

# So originally we had the following:
#     q was used to represent resource scheduling for resource 1, and the number subscripts are for:
#     (1) a11, (2) a21, (3) b11, (4) b21

#     Since all the above propositions stand for critical sections that make use of the same resource,
#     r1 then we would have to schedule them if they are true
#     therefore the different ways/possibilities of scheduling:

    # q12 = Var('q12') #true if a11 is scheduled before a21,
    # q13 = Var('q13') #true if a11 is scheduled before b11
    # q14 = Var('q14') #true if a11 is scheduled before b21
    # q21 = Var('q21') #true if a12 is scheduled before a11
    # q23 = Var('q23') #true if a12 is scheduled before b11
    # q24 = Var('q24') #true if a12 is scheduled before b21
    # q31 = Var('q31') #true if b11 is scheduled before a11
    # q32 = Var('q32') #true if b11 is scheduled before a21
    # q34 = Var('q34') #true if b11 is scheduled before b21 
    # q41 = Var('q41') #true if b21 is scheduled before a11
    # q42 = Var('q42') #true if b21 is scheduled before a21
    # q43 = Var('q43') #true if b21 is scheduled before b11

    # This was the original idea, and then we would have constraints:
    # if q12 is true, then q21 must be false because
    # if q12 is true, then a11 is scheduled before a21,
    # meaning that it cant be the case that a21 is scheduled before a11 ie that q21 is true
    # so original constraints: q12 >>~q21, q21 >> ~q12
    # This applies for the other propositions:

    # E.add_constraint(~q12 | ~q21)
    # E.add_constraint(~q13 | ~q31)
    # E.add_constraint(~q14 | ~q41)
    # E.add_constraint(~q23 | ~q32)
    # E.add_constraint(~q24 | ~q42)
    # E.add_constraint(~q34 | ~q43)

    # Then we would have the connection between the segment propositons and the scheduling propositons:
    # We know that if p1_crit_sect1 and p1_crit_sect2 make use of the same resource (either r1 or r2)
    # they must be scheduled. So assuming, they use r1, then a11 and a21 would be true
    # Therefore they need to be scheduled (a11 & a21) >> (q12 | q21)
    # The or is present because they could be scheduled either way.
    # So we would have the following constraints:
    # E.add_constraint( (~a11 | ~a21) | (q12 | q21) )
    # E.add_constraint( (~a11 | ~b11) | (q13 | q31) )
    # E.add_constraint( (~a11 | ~b21) | (q14 | q41) )
    # E.add_constraint( (~a21 | ~b11) | (q23 | q32) )
    # E.add_constraint( (~a21 | ~b21) | (q24 | q42) )
    # E.add_constraint( (~b11 | ~b21) | (q34 | q43) )

# However, this is an issue because of the way implications, for p >> q
# if p is false, then q can be true or false
# Furthermore, the use of | in (q12 | q21) means that there could be a case where both of them 
# are true, but that is limited by our constraint.

# But this scheduling propositon and scheduling constraints do not do the job properly
# and this was displayed in the sample solution generated, in the solution we had:

# a11 - false
# a12 - false
# a21 - false
# a22 - false

# but we had the following:
# p12 - true
# p21 - false

# This should not be the case, because all of the the 'a' propositions are false, then 
# the p1 critical sections do not make use of any resources, therefore there is no scheduling
# required which means that p12 and p21 should both be false

# However because of the very constraint, we applied
# where p12 >> ~p21
# one of them being false, will force the other to be true. Hence we have an error
# This tells me that the constraints are wrong or the scheduling propositions are wrong

# I decided to modify the scheduling propositons.
    # Rather than having propositions for the specific ways that the segments can be scheduled
    # we can just have propositions for if there is a scheduling required, this will cut the 
    # current propositions in half. So instead we have the following, using the same notation:
    # (1) a11, (2) a21, (3) b11, (4) b21

    q12 = Var('q12') #true if a11 and a21 need to be scheduled
    q13 = Var('q13') #true if a11 and b11 need to be scheduled
    q14 = Var('q14') #true if a11 and b21 need to be scheduled
    q23 = Var('q23') #true if a21 and b11 need to be scheduled
    q24 = Var('q24') #true if a21 and b21 need to be scheduled
    q34 = Var('q34') #true if b11 and b21 need to be scheduled

    # This will generate a new version of constraints

# ------------------------------RESOURCE 2 SCHEDULING PROPOSTIONS------------------------------------------
Applying the same change from resource 1. Now p represents resource 2 and the subscripts references are
(1) a12, (2) a22, (3) b12, (4) b22

    p12 = Var('p12') #true if a12 and a22 need to be scheduled
    p13 = Var('p13') #true if a12 and b12 need to be scheduled
    p14 = Var('p14') #true if a12 and b22 need to be scheduled
    p23 = Var('p23') #true if a22 and b12 need to be scheduled
    p24 = Var('p24') #true if a22 and b22 need to be scheduled
    p34 = Var('p34') #true if b12 and b22 need to be scheduled

#----------------------------------------CONSTRAINTS-----------------------------------------------------
# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    E = Encoding()
    
    #if two critical sections make use of the same constraints then they need to be scheduled
    E.add_constraint( (~a11 | ~a21) | q12 ) #(a11 & a21) >> q12
                                            #if p1_crit_sect1 uses r1 (a11) and p1_crit_sect2 uses r1 (a21)
                                            #then they must be scheduled (q12)

    E.add_constraint( (~a11 | ~b11) | q13 ) #(a11 & b11) >> q13
    E.add_constraint( (~a11 | ~b21) | q14 ) #(a11 & b21) >> q14
    E.add_constraint( (~a21 | ~b11) | q23 ) #(a21 & b11) >> q23
    E.add_constraint( (~a21 | ~b21) | q24 ) #(a21 & b21) >> q24
    E.add_constraint( (~b11 | ~b21) | q34 ) #(b11 & b21) >> q34

    E.add_constraint( (~a12 | ~a22) | p12 ) #(a12 & a22) >> p12
                                            #if p1_crit_sect1 uses r2 (a12) and p1_crit_sect2 uses r2 (a22)
                                            #then they must be scheduled (p12)

    E.add_constraint( (~a12 | ~b12) | p13 ) #(a12 & b12) >> p13
    E.add_constraint( (~a12 | ~b22) | p14 ) #(a12 & b22) >> p14
    E.add_constraint( (~a22 | ~b12) | p23 ) #(a22 & b12) >> p23
    E.add_constraint( (~a22 | ~b22) | p24 ) #(a22 & b22) >> p24
    E.add_constraint( (~b12 | ~b22) | p34 ) #(b12 & b22) >> p34



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
