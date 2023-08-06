#3: Summing a Series
import matplotlib.pyplot as plt
from sympy import sympify
from sympy import Poly,Symbol,summation,pprint,solve,Integral,Derivative
from sympy import solve_poly_inequality,solve_rational_inequalities,solve_univariate_inequality,sin

#Solving the inequality
def inequality_solver(expr):
    '''
    For example :-
    
    expr='-x**2 + 4 < 0'
    pprint(inequality_solver(expr))
    
    expr='((x-1)/(x+2)) > 0'
    pprint(inequality_solver(expr))

    expr='sin(x)-0.6>0'
    pprint(inequality_solver(expr))
    '''
    expressed_x=Symbol('x')
    expr=sympify(expr)
    ineq_obj=expr
    lhs=ineq_obj.lhs
    ans=[]
    if lhs.is_polynomial():
        p=Poly(lhs,expressed_x)
        rel=ineq_obj.rel_op
        ans=solve_poly_inequality(p,rel)
    elif lhs.is_rational_function(): 
        numer,denom=lhs.as_numer_denom()
        p1=Poly(numer)
        p2=Poly(denom)
        rel=ineq_obj.rel_op
        ans=solve_rational_inequalities([[((p1, p2), rel)]])
    else:
        ans=solve_univariate_inequality(ineq_obj,expressed_x,relational=False)
        
    return ans
# Finding the Roots of a Quadratic Equation
def roots(a, b, c):
    '''
    For example :-
    r1,r2=roots(1,1,1)
    print(r1,r2)
    '''
    D = (b*b - 4*a*c)**0.5
    root_1 = (-b + D)/(2*a)
    root_2 = (-b - D)/(2*a)
    return(root_1,root_2)



# Exploring a Quadratic(General) Function Visually
def plot_general_equation(expr,x_values):
    '''
    For example :-
    x_values=list(range(-1000,1000))
    expr='x*x*x*x+5*x*x*x+10*x*x+12*x+1'
    plot_general_equation(expr,x_values)
    '''
    expr=sympify(expr)
    expressed_x=Symbol('x')
    y_values=[]
    for x in x_values:
        y=expr.subs({expressed_x:x})
        y_values.append(y)
    plt.plot(x_values, y_values)
    plt.xlabel('x-coordinate')
    plt.ylabel('y-coordinate')
    plt.title('Expressed General Equation')
    plt.show()
    

# Solving n pairs of equations
def solve_n_equations(expressions):
    '''
    For example :-
    x=Symbol('x')
    y=Symbol('y')
    z=Symbol('z')
    expr1=2*x+2*y+2*z
    expr2=4*x+4*y+4*z
    expr3=3*x+3*y+3*z
    expressions=(expr1,expr2,expr3)
    print(solve_n_equations(expressions))

    '''
    solutions=solve(expressions,dict=True)
    return solutions



# Summing a series by using the nth term
def seriesSummation(expr,upto):
    '''
    For example :-
    expr = input('Enter the nth term: ')
    upto = int(input('Enter the number of terms: '))

    Let's say :-
    expr = a*n+d
    upto = 10000
    s = 50005000*a + 10000*d 
    
    s=seriesSummation(expr,upto)
    pprint(s)
    '''
    n = Symbol('n')
    expr = sympify(expr)
    s = summation(expr, (n, 1, upto))
    return s

# Finding the Derivative of a equation wrt to variable
def find_derivative(expr,variable):
    '''
    For example :-
    St='5*u*t**2+2*t+8'
    Stt=find_derivative(St,'t')
    pprint(Stt)
    Sttt=find_derivative(Stt,'t')
    pprint(Sttt)
    '''
    variable=Symbol(variable)
    expr=sympify(expr)
    d=Derivative(expr,variable).doit()
    return d

# Finding the Indefinite Integral of a equation wrt to variable
def find_indefinite_integral(expr,variable):
    '''
    For example :-
    St='5*u*t**2+2*t+8'
    Stt=find_indefinite_integral(St,'t')
    pprint(Stt)
    Sttt=find_indefinite_integral(Stt,'t')
    pprint(Sttt)
    '''
    variable=Symbol(variable)
    expr=sympify(expr)
    i=Integral(expr,variable).doit()
    return i


# Finding the Definite Integral of a equation wrt to variable
def find_definite_integral(expr,variable,lower_limit,upper_limit):
    '''
    For example :-
    St='5*u*t**2+2*t+8'
    Stt=find_definite_integral(St,'t',0,10)
    pprint(Stt)
    Sttt=find_definite_integral(Stt,'u',0,1000)
    pprint(Sttt)
    '''
    variable=Symbol(variable)
    expr=sympify(expr)
    area=Integral(expr,(variable,lower_limit,upper_limit)).doit()
    return area

#Finding the length of the integral
def find_length(expr,variable,lower_limit,upper_limit):
    '''
    For example :-
    p=find_length(expr='x',variable='x',lower_limit=-5,upper_limit=10)
    print(p)
    '''
    variable=Symbol(variable)
    expr=sympify(expr)
    d=Derivative(expr,variable).doit()
    new_expr=pow(1+pow(d,2),0.5)
    ans=Integral(new_expr,(variable,lower_limit,upper_limit)).doit()
    return ans


