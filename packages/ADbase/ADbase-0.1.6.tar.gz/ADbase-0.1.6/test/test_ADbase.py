from ADbase import *
import numpy as np
import math
import pytest

'''
For this milestone, we only consider scalar input, so for the name attribute here, we just store the name of 'self' instance after the operations,
and use default name attribute in the test file, which would be all 'x', but we will improve this part for next milestone.
For the next milestone, we will store all the sorted unique variable names, like ['x','y','z'] and calculate their corresponding derivatives, like [[1,0,0],[0,1,0],[0,0,1]].      
'''
# Testing inputs
def test_invalid_der():
    with pytest.raises(TypeError):
        x = AD(0, 'hello', 'x')

def test_invalid_val():
    with pytest.raises(TypeError):
        x = AD('hello', 1, 'x')

def test_invalid_name():
    with pytest.raises(TypeError):
        x = AD(0 , 1, 1)
# Testing __str__
def test_str():
    x = AD(0 , 1, 'x')
    assert x.__str__() == 'Value is:0, derivative is:1, Name is:x'
    
        
# Testing __add__
def test_add():
    #add constant
    x = AD(0, 1, 'x')
    z = x + 2
    assert z.value == 2
    assert z.deriv == 1
    assert z.name == 'x'
    
    #add AD
    y = AD(2, 1)
    k = x + y
    assert k.value == 2
    assert k.deriv == 2
    assert k.name == 'x'    
    
    #type error
    with pytest.raises(TypeError):
        x+'s'

# Testing __radd__
def test_radd():
    #add constant
    x = AD(0, 1, 'x')
    z = 2 + x
    assert z.value == 2
    assert z.deriv == 1
    assert z.name == 'x'

    #add AD
    y = AD(2, 1)
    k = y + x
    assert k.value == 2
    assert k.deriv == 2
    assert k.name == 'x'    
    
    #type error
    with pytest.raises(TypeError):
        's'+ x

# Testing __mul__
def test_mul():
    #multiply constant
    x = AD(1, 1, 'x')
    z = x * 3
    assert z.value == 3
    assert z.deriv == 3
    assert z.name == 'x'

    #multiply AD
    y = AD(2, 1)
    k = x * y
    assert k.value == 2
    assert k.deriv == 3
    assert k.name == 'x'    
    
    #type error
    with pytest.raises(TypeError):
        x*'s'
    
    #situation1
    m = x * y + 4
    assert m.value == 6
    assert m.deriv == 3
    assert m.name == 'x' 

# Testing __rmul__
def test_rmul():
    #multiply constant
    x = AD(1, 1, 'x')
    z = 3 * x
    assert z.value == 3
    assert z.deriv == 3
    assert z.name == 'x'

    #multiply AD
    y = AD(2, 1)
    k = y * x
    assert k.value == 2
    assert k.deriv == 3
    assert k.name == 'x'    
    
    #type error
    with pytest.raises(TypeError):
        's'*x

# Testing __neg__
def test_neg():
    x = AD(1, 1, 'x')
    z = -x
    assert z.value == -1
    assert z.deriv == -1
    assert z.name == 'x'  

# Testing __sub__
def test_sub():
    #sub constant
    x = AD(0, 1, 'x')
    z = x - 2
    assert z.value == -2
    assert z.deriv == 1
    assert z.name == 'x'
    
    #sub AD
    y = AD(2, 1)
    k = x - y
    assert k.value == -2
    assert k.deriv == 0
    assert k.name == 'x'    
    
    #type error
    with pytest.raises(TypeError):
        x - 's'

# Testing __rsub__
def test_rsub():
    #sub constant
    x = AD(0, 1, 'x')
    z = 2 -x
    assert z.value == 2
    assert z.deriv == -1
    assert z.name == 'x'
    
    #sub AD
    y = AD(2, 1)
    k = y-x
    assert k.value == 2
    assert k.deriv == 0
    assert k.name == 'x'    
    
    #type error
    with pytest.raises(TypeError):
        's' -x
        
# Testing __truediv__
def test_truediv():
    #truediv constant
    x = AD(2, 1, 'x')
    z = x / 2
    assert z.value == 1
    assert z.deriv == 1/2
    assert z.name == 'x'
    
    #truediv AD
    y = AD(2, 1)
    k = x / y
    assert k.value == 1
    assert k.deriv == 0
    assert k.name == 'x' 
    
    #divisor is 0
    with pytest.raises(ZeroDivisionError):
        x / 0
    m = AD(0, 1)
    with pytest.raises(ZeroDivisionError):
        x / m
    
    
    #type error
    with pytest.raises(TypeError):
        x / 's'
        
        
# Testing __rtruediv__
def test_rtruediv():
    #truediv constant
    x = AD(2, 1, 'x')
    z = 2/x
    assert z.value == 1
    assert z.deriv == -1/2
    assert z.name == 'x'
    
    #truediv AD
    y = AD(2, 1)
    k = y/x 
    assert k.value == 1
    assert k.deriv == 0
    assert k.name == 'x' 
    
    #divisor is 0
    m = AD(0, 1)
    with pytest.raises(ZeroDivisionError):
        2 / m

    with pytest.raises(ZeroDivisionError):
        x / m
    #type error
    with pytest.raises(TypeError):
        's' / x 
        
# Testing __pow__
def test_pow():
    # pow constant
    x = AD(2, 1, 'x')
    z = x **2
    assert z.value == 4
    assert z.deriv == 4
    assert z.name == 'x'    
    
    y = AD(-1, 1)
    with pytest.raises(ValueError):
        y ** (0.5)  
        
    k= AD(0, 1, 'k')
    with pytest.raises(ZeroDivisionError):
        k ** (0)  
    with pytest.raises(ZeroDivisionError):
        k ** (1)  
    with pytest.raises(ZeroDivisionError):
        k ** (-1) 
        
    # pow AD
    m = AD(0.5, 1)
    with pytest.raises(ValueError):
        y ** m          
    with pytest.raises(ZeroDivisionError):
        k ** y       
    with pytest.raises(ZeroDivisionError):
        k ** k   
        
    l = x **x
    assert l.value == 4
    assert l.deriv == (1*np.log(2) + 1)*4
    assert l.name == 'x'

    #type error
    with pytest.raises(TypeError):
        x**('s') 
        
        
# Testing __rpow__
def test_rpow():
    # rpow constant
    x = AD(2, 1, 'x')
    z = 2 **x
    assert z.value == 4
    assert z.deriv == 4 * np.log(2)
    assert z.name == 'x'    

    with pytest.raises(ValueError):
        (-3) ** x 
    
    y = AD(-1, 1)
    with pytest.raises(ZeroDivisionError):
        0 ** (y) 
          
    k= AD(0, 1)
    with pytest.raises(ZeroDivisionError):
        0 ** (k) 

    #type error
    with pytest.raises(TypeError):
        ('s')** x 
        
# Testing __sin__       
def test_sin():
    x = AD(0.5, 1, 'x')
    z = x.sin()
    assert z.value == np.sin(0.5)
    assert z.deriv == np.cos(0.5)
    
# Testing __sinh__       
def test_sinh():
    x = AD(0.5, 1, 'x')
    z = x.sinh()
    assert z.value == np.sinh(0.5)
    assert z.deriv == np.cosh(0.5)   
    

# Testing __arcsin__       
def test_arcsin():
    x = AD(0.5, 1, 'x')
    z = x.arcsin()
    assert z.value == np.arcsin(0.5)
    assert z.deriv ==  ((1 - 0.5 ** 2) ** (-0.5))    
    k= AD(-2, 1)
    with pytest.raises(ValueError):
        k.arcsin()  
    
# Testing __cos__       
def test_cos():
    x = AD(0.5, 1, 'x')
    z = x.cos()
    assert z.value == np.cos(0.5)
    assert z.deriv == -np.sin(0.5)
    
# Testing __cosh__       
def test_cosh():
    x = AD(0.5, 1, 'x')
    z = x.cosh()
    assert z.value == np.cosh(0.5)
    assert z.deriv == np.sinh(0.5)   
    

# Testing __arccos__       
def test_arccos():
    x = AD(0.5, 1, 'x')
    z = x.arccos()
    assert z.value == np.arccos(0.5)
    assert z.deriv ==  - ((1 - 0.5 ** 2) ** (-0.5))   
    
    k= AD(-2, 1)
    with pytest.raises(ValueError):
        k.arccos()  
        
# Testing __tan__       
def test_tan():
    x = AD(0.5, 1, 'x')
    z = x.tan()
    assert z.value == np.tan(0.5)
    assert z.deriv == 1 / np.power(np.cos(0.5), 2)
    
    k= AD(1.5*np.pi, 1)
    with pytest.raises(ValueError):
        k.tan()     
    
    
# Testing __tanh__       
def test_tanh():
    x = AD(0.5, 1, 'x')
    z = x.tanh()
    assert z.value == np.tanh(0.5)
    assert z.deriv == 1 - (np.tanh(0.5))**2      
    

# Testing __arctan__       
def test_arctan():
    x = AD(0.5, 1, 'x')
    z = x.arctan()
    assert z.value == np.arctan(0.5)
    assert z.deriv ==  (1 + 0.5 ** 2) ** (-1)


# Testing __exp__       
def test_exp():
    x = AD(0.5, 1, 'x')
    z = x.exp()
    assert z.value == np.exp(0.5)
    assert z.deriv ==  np.exp(0.5)

# Testing __ln__       
def test_ln():
    x = AD(0.5, 1, 'x')
    z = x.ln()
    assert z.value == np.log(0.5)
    assert z.deriv ==  2
    k= AD(-3, 1)
    with pytest.raises(ValueError):
        k.ln()  

# Testing __ln_base__       
def test_ln_base():
    x = AD(0.5, 1, 'x')
    z = x.ln_base(2)
    assert z.value == math.log(0.5,2)
    assert z.deriv ==  2  / np.log(2)
    k= AD(-3, 1)
    with pytest.raises(ValueError):
        k.ln_base(2)     
  
 # Testing __sqrt__       
def test_sqrt():
    x = AD(0.5, 1, 'x')
    z = x.sqrt()
    assert z.value == np.sqrt(0.5)
    assert z.deriv ==  0.5 * 0.5 **(-0.5)
 
 
# Testing __logistic__       
def test_logistic():
    x = AD(0.5, 1, 'x')
    z = x.logistic()
    assert z.value == 1 / (1 + np.exp(-0.5))
    assert z.deriv ==  np.exp(-0.5) / ((1 + np.exp(-0.5)) ** 2)
    

