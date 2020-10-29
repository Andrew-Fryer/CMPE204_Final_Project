
from nnf import Var
from lib204 import Encoding

#2 processes each with 2 segments, 2 resources
#each segment can make use of only one resource
#goal is to use propositional values to determine a schedule
#for processes on two CPU cores

#a refers to code segments for process 1
#first number subscript indicates with segment it is (1 -first segment, 2 - second segment)
#second number subscript indicates what resource is being used

a11 = Var('a11') #true if proc 1 crit sect 1 uses resource 1
a12 = Var('a12') #true if proc 1 crit sect 1 uses resource 2
a21 = Var('a21') #true if proc 1 crit sect 2 uses resource 1
a22 = Var('a22') #true if proc 1 crit sect 2 uses resource 2

#same thing for process 2 code segments, this time with b rather
#than a

b11 = Var('b11')
b12 = Var('b12')
b21 = Var('b21')
b22 = Var('b22')

#scheduling propositions, truth values used to determine possible
#scheduling
#let q refer to scheduling props for resource 1
#let p refer to scheduling props for resource 2

#subscript refers to code segment, for q:
# 1: a11, 2: a21, 3: b11, 4: b21

q12 = Var('q12') #true if a11 is scheduled before a21
q13 = Var('q13') #true if a11 is scheduled before b11
q14 = Var('q14') #true if a11 is scheduled before b21
q21 = Var('q21') #true if a21 is scheduled before a11
q23 = Var('q23')
q24 = Var('q24')
q31 = Var('q31')
q32 = Var('q32')
q34 = Var('q34')
q41 = Var('q41')
q42 = Var('q42')
q43 = Var('q43')

#similar thing for resource 2 where we use p and:
## 1: a12, 2: a22, 3: b12, 4: b22
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
    E.add_constraint( f.negate(a11 & a21) | (q12 | q21) )
    E.add_constraint( f.negate(a11 & b11) | (q13 | q31) )
    E.add_constraint( f.negate(a11 & b21) | (q14 | q41) )
    E.add_constraint( f.negate(a21 & b11) | (q23 | q32) )
    E.add_constraint( f.negate(a21 & b21) | (q24 | q42) )
    E.add_constraint( f.negate(b11 & b21) | (q34 | q43) )

    E.add_constraint( f.negate(a12  & a22) | (p12 | p21) )
    E.add_constraint( f.negate(a12  & b12) | (p13 | p31) )
    E.add_constraint( f.negate(a12  & b22) | (p14 | p41) )
    E.add_constraint( f.negate(a22  & b12) | (p23 | p32) )
    E.add_constraint( f.negate(a22  & b22) | (p24 | p42) )
    E.add_constraint( f.negate(b12  & b22) | (p34 | p43) )


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
