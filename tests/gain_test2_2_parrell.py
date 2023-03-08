from scipy import integrate
from scipy.integrate import solve_ivp
import numpy as np
import math

def f(t, y):
    print(y)
    theta = math.pi/4
    ham = np.array([[1,0],[1,np.exp(-1j*theta*t)]])

    return-1j * np.dot(ham,y)



y0 = np.eye(2,dtype= np.complex128)
t0 = 0
tmax = 10**(-6)




# idea is to pass in the full arrays of beta_s..i..p..delta to the solve ivp and use np to vectorize

integrate.solve_ivp(fun = f,t_span  =(t0,tmax),y0 = [1j,0],method='RK45',vectorized=True)