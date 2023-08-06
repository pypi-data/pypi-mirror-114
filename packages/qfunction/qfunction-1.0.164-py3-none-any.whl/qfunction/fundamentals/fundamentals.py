from numpy import power,exp,sqrt,pi,array
from sys import float_info as float_h
from qfunction.fundamentals.canonic import prod
zero = 44e-15
inf = 1/zero


def limit(f,x,delta_x=zero):
    return f(x+delta_x)


def q_exp(u,q=1):
	power = lambda q_: 1/(1-q_)
	power = limit(power,q)
	q_exp_base = lambda q_: pow((1+u*(1-q_)),power)
	return limit(q_exp_base,q)


def radian(angle):
	return angle*(2*pi)/360

## q-sum ##
def q_sum(*args,q=1)->float:
    den_ = lambda q_: 1-q_
    den = limit(den_,q)
    sm_r = sum(args)
    pr_r = prod(*args)
    return sm_r + (den)*pr_r

## q-ln ##
def q_ln(u,q=1):
    den_ = lambda q_: 1-q_
    den = limit(den_,q)
    return (power(u,den)-1)/den

## q-multi ##
def q_mult(*u,q=1):
    den_ = lambda q_: 1-q_
    den = limit(den_,q)
    args = array(list(u))
    args = args**(den)
    #print(args)
    res = args.sum() -1
    #print(res)
    
    #print(den)
    return power(res,1/den)

## q-sub ##
def q_sub(a,b,q=1):
    den_ = lambda q_: 1-q_
    den = limit(den_,q)
    return (a-b)/(1+(den)*b)

