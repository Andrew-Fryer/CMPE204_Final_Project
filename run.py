
from nnf import Var
from lib204 import Encoding

# Processes may go next
p1 = Var('p1')
p2 = Var('p2')

# Resources
#r1 = Var('r1')
#r2 = Var('r2')

# Process is waiting for resource
w11 = Var('w11')
w12 = Var('w12')
w21 = Var('w21')
w22 = Var('w22')

# Process has resource
h11 = Var('h11')
h12 = Var('h12')
h21 = Var('h21')
h22 = Var('h22')

# Process may ask for resource (in maximum)
m11 = Var('m11')
m12 = Var('m12')
m21 = Var('m21')
m22 = Var('m22')

#
# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.
def example_theory():
    E = Encoding()
    
    # Mutually exclusive
    E.add_constraint(h11>>~h21)
    E.add_constraint(h21>>~h11)
    E.add_constraint(h12>>~h22)
    E.add_constraint(h22>>~h12)

    E.add_constraint(h11 >> ~w11)

    E.add_constraint(a | b)
    E.add_constraint(a | b)
    E.add_constraint(a | b)
    E.add_constraint(a | b)
    E.add_constraint(a | b)
    E.add_constraint(a | b)
    E.add_constraint(a | b)
    E.add_constraint(a | b)
    E.add_constraint(~a | ~x)
    E.add_constraint(c | y | z)
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
