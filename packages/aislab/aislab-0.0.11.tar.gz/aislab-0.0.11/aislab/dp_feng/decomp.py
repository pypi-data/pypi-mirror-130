"""
author: OPEN-MAT
date: 	15.06.2019
Matlab version: 26 Apr 2009
Course: Multivariable Control Systems
"""
import numpy as np
from aislab.gnrl.sf import *
####################################################################################
# def trnd():
####################################################################################
def permdl(x, w=None, T=7, Ne=None):
    if w is None: w = ones(x.shape)
    T = int(T)
    N = len(x)
    n = np.floor(N/T).astype(int)
    S = x[:n*T].reshape(n, T)
    W = w[:n*T].reshape(n, T)
    if N > n*T:
        ss = nans((1, np.ceil(N/T).astype(int)*T - N))
        S = np.vstack((S, np.hstack((x[n*T:].T, ss))))
        W = np.vstack((W, np.hstack((w[n*T:].T, ss))))
    Nw = np.nansum(W, axis=0).astype(float)
    Nw[Nw == 0] = 1e-6
    pm = np.nansum(S*W, axis=0)/Nw
    ind = T if len(x) % T == 0 else len(x) % T
    pm = np.roll(pm, -ind)
    return pm
####################################################################################
# 	T determination = f(Rxx), f(fft), ...
