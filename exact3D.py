import sympy as sp

# create symbol and value of N
q = sp.Symbol("q")
N = 6

# expression which we will multiply as with the given function
expr = 1.

# we only need to multiply with n up to N, as all higher terms give a 
# sum where the lowest exponent for q (besides 0) is greater than N
for n in range(1, N + 1):
    expr *= 1/(1 - q**n)**(0.5*(n + 1)*n)
    
# print the found expression and evaluate the wanted term
print(expr)
print(int(expr.diff(q, N).subs(q, 0)/sp.factorial(N)))