#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 16:21:50 2021

@author: telu
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import lu

from pySDC.implementations.collocation_classes.gauss_lobatto import \
    CollGaussLobatto
from pySDC.implementations.collocation_classes.gauss_radau_left import \
    CollGaussRadau_Left
from pySDC.implementations.collocation_classes.gauss_radau_right import \
    CollGaussRadau_Right
from pySDC.implementations.collocation_classes.equidistant import \
    Equidistant
from pySDC.core.Sweeper import sweeper

collDict = {'LOBATTO': CollGaussLobatto,
            'RADAU_LEFT': CollGaussRadau_Left,
            'RADAU_RIGHT': CollGaussRadau_Right,
            'EQUID': Equidistant}

lColors = plt.rcParams['axes.prop_cycle'].by_key()['color']

# Problem parameters
tBeg = 0
tEnd = 1
lam = -10.0+0j  # \lambda coefficient from the space operator
numType = np.array(lam).dtype
u0 = 1  # initial solution

# Time interval decomposition
L = 2  # number of time steps
times = np.linspace(tBeg, tEnd, num=L+1)
dt = times[1]-times[0]


# SDC parameters
sweepType = 'IE'
nodesType = 'RADAU_RIGHT'
initCond = 'U0'

# Plot parameters
plotSDC = True
plotPFASST = False
plotOrder = False
plotError = True

# Order analysis
lM = [5, 9]  # (on which number of nodes doing the order analysis.
# -- should be consecutive values in [3, 5, 9, 17, ... 2**i + 1]

figSuffix = f'{sweepType}-{nodesType}-{lam}-IC={initCond}-u0={u0}'


def setInitCond(u):
    if initCond == 'ZERO':
        u[:] = 0
    elif initCond == 'U0':
        u[:] = u0
    elif initCond == 'RAND':
        np.random.seed(0)
        u[:] = np.random.rand(*u.shape)
    else:
        raise ValueError(f'wrong initial condition {initCond}')


def runPFASSTandFriends(M, nSweep):

    # Generate nodes, deltas and Q using pySDC
    coll = collDict[nodesType](M, 0, 1)
    sw = sweeper({'collocation_class': collDict[nodesType], 'num_nodes': M})
    nodes = coll._getNodes
    deltas = coll._gen_deltas
    Q = coll._gen_Qmatrix[1:, 1:]

    # Generate Q_\Delta
    QDelta = np.zeros((M, M))
    if sweepType in ['BE', 'FE']:
        offset = 1 if sweepType == 'FE' else 0
        for i in range(offset, M):
            QDelta[i:, :M-i] += np.diag(deltas[:M-i])
    elif sweepType == 'LU_Tibo':
        QT = Q.T.copy()
        [_, _, U] = lu(QT, overwrite_a=True)
        QDelta = U.T
    elif sweepType in ['LU', 'IE']:
        QDelta = sw.get_Qdelta_implicit(coll, sweepType)[1:, 1:]
    elif sweepType == 'EE':
        QDelta = sw.get_Qdelta_explicit(coll, sweepType)[1:, 1:]
    else:
        raise ValueError(f'sweepType={sweepType}')

    # Scaling with lam*dt
    Q = Q*lam*dt
    QDelta = QDelta*lam*dt

    # Generate other matrices
    H = np.zeros((M, M), dtype=numType)
    H[:, -1] = 1
    I = np.identity(M)

    # Generate operators
    ImQDelta = I - QDelta
    ImQ = I - Q

    def sweep(u, uStar, f):
        u += np.linalg.solve(ImQDelta, H.dot(uStar) + f - ImQ.dot(u))

    # Variables
    f = np.zeros((L, M), dtype=numType)
    f[0] = 0
    u = np.zeros((L, M), dtype=numType)
    t = np.array([t + dt*nodes for t in times[:-1]])

    # SDC solution
    uSDC = u.copy()
    setInitCond(uSDC)
    uStar = u[0]
    for l in range(L):
        # All sweeps for one interval
        for n in range(nSweep):
            sweep(uSDC[l], uStar, f[l])
        uStar = uSDC[l]

    # Parareal-SDC solution <=> pipelined SDC <=> RIDC ?
    uPar = u.copy()
    setInitCond(uPar)
    # uPar[:] = u0
    for n in range(nSweep):
        # Sequential sweep on all intervals
        uStar = u[0]*0
        for l in range(L):
            sweep(uPar[l], uStar, f[l])
            uStar = uPar[l]

    # PFASST solution
    uPFA = u.copy()
    setInitCond(uPFA)
    uPFA_half = u.copy()
    for n in range(nSweep):
        # First sequential sweep (coarse)
        uStar = u[0]*0
        for l in range(L):
            sweep(uPFA[l], uStar, f[l])
            uStar = uPFA[l]
            np.copyto(uPFA_half[l], uPFA[l])  # save for postprocessing
        # Second parallel sweep (fine)
        uStar = u[0]*0
        for l in range(L):
            uStarPrev = uPFA[l].copy()
            sweep(uPFA[l], uStar, f[l])
            uStar = uStarPrev

    return uSDC, uPar, uPFA, uPFA_half, t


# %% First tests
# Numerical solutions
# uSDC, uPar, uPFA, t = runPFASSTandFriends(M, nSweep)

# # Exact solution
# uExact = np.exp(t*lam)

# # Plot solution and error
# if False:
#     plt.figure('Solution (amplitude)')
#     for sol, lbl, sym in [[uExact, 'Exact', 'o-'],
#                           [uSDC, 'SDC', 's-'],
#                           [uPar, 'Parareal', '>-'],
#                           [uPFA, 'PFASST', 'p-']]:
#         plt.plot(t.ravel(), sol.ravel().real, sym, label=lbl)
#     plt.legend()
#     plt.grid(True)
#     plt.xlabel('Time')

#     plt.figure('Solution (phase)')
#     for sol, lbl, sym in [[uExact, 'Exact', 'o-'],
#                           [uSDC, 'SDC', 's-'],
#                           [uPar, 'Parareal', '>-'],
#                           [uPFA, 'PFASST', 'p-']]:
#         plt.plot(t.ravel(), sol.ravel().imag, sym, label=lbl)
#     plt.legend()
#     plt.grid(True)
#     plt.xlabel('Time')

# eSDC = np.abs(uExact.ravel()-uSDC.ravel())
# ePar = np.abs(uExact.ravel()-uPar.ravel())
# ePFA = np.abs(uExact.ravel()-uPFA.ravel())

# plt.figure('Error')
# plt.semilogy(t.ravel(), eSDC, 's-', label=f'SDC {nSweep} sweep')
# plt.semilogy(t.ravel(), ePar, '>-', label=f'Parareal {nSweep} iter')
# plt.semilogy(t.ravel(), ePFA, 'p-', label=f'PFASST {nSweep} iter')
# plt.legend()
# plt.grid(True)
# plt.xlabel('Time')

# %% Error and order analysis

eSDC, ePar, ePFA, ePFA_half = [], [], [], []
lSol = ['SDC', 'Par', 'PFA', 'PFA_half']

for nSweep in [1, 2, 3, 4]:
    for s in lSol:
        exec(f'e{s}.append([])')
    for M in lM:
        uSDC, uPar, uPFA, uPFA_half, t = runPFASSTandFriends(M, nSweep)
        for v in ['u'+s for s in lSol]+['t']:
            exec(f'{v} = {v}[:, ::(M-1)//2].ravel()[1:]')
        for s in lSol:
            exec(f'e{s}[-1].append(abs(u{s} - np.exp(lam*t)).ravel())')
for s in lSol:
    exec(f'e{s} = np.array(e{s})')


# %% Error plot for less number of nodes
# -- uses the lowest value for M in lM

if plotError and plotSDC:
    plt.figure(f'err-SDC&Par-{figSuffix}-M={lM[0]}')
    lbl = True
    for err, ls in zip([eSDC, ePar],
                       ['-', 's--']):
        for (i, e), c in zip(enumerate(err), lColors):
            label = f'sweep {i+1}' if lbl else None
            plt.semilogy(t, e[0], ls, c=c, label=label)
        lbl = False
    plt.vlines(times[1:], 0, 1, colors='gray')
    plt.title('"-" = SDC, "--s" = Gauss-Seidel MS-SDC')
    plt.xlabel('Time')
    plt.ylabel('Absolute error')
    plt.ylim(1e-10, 1)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

if plotError and plotPFASST:
    plt.figure(f'err-PFASST-{figSuffix}-M={lM[0]}')
    lbl = True
    for err, ls in zip([ePFA, ePFA_half],
                       ['-', 's--']):
        for (i, e), c in zip(enumerate(err), lColors):
            label = f'sweep {i+1}' if lbl else None
            plt.semilogy(t, e[0], ls, c=c, label=label)
        lbl = False
    plt.vlines(times[1:], 0, 1, colors='gray')
    plt.title('"-" = PFASST, "--s" = PFASST after "coarse" sweep')
    plt.xlabel('Time')
    plt.ylabel('Absolute error')
    plt.ylim(1e-10, 1)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

# %% Order plot


def computeOrder(err):
    # Linear regression to compute order at each times
    y = np.log2(err)
    x = (np.arange(len(lM)) + 1.0)[None, :, None]
    xMean = x.mean(axis=1)
    yMean = y.mean(axis=1)
    sX = ((x-xMean[:, None, :])**2).sum(axis=1)
    sXY = ((x-xMean[:, None, :])*(y-yMean[:, None, :])).sum(axis=1)
    order = np.abs(sXY/sX)
    return order


if plotOrder and plotSDC:
    plt.figure(f'order-SDC&Par-{figSuffix}-lM={lM}')
    lbl = True
    for err, ls in zip([eSDC, ePar],
                       ['-', 's--']):
        order = computeOrder(err)
        for (i, o), c in zip(enumerate(order), lColors):
            label = f'sweep {i+1}' if lbl else None
            plt.plot(t, o, ls, c=c, label=label)
        lbl = False
    plt.vlines(times[1:], 0, 5, colors='gray')
    plt.title('"-" = SDC, "--s" = Gauss-Seidel MS-SDC')
    plt.xlabel('Time')
    plt.ylabel('Order')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

if plotOrder and plotPFASST:
    plt.figure(f'order-PFASST-{figSuffix}-lM={lM}')
    lbl = True
    for err, ls in zip([ePFA, ePFA_half],
                       ['-', 's--']):
        order = computeOrder(err)
        for (i, o), c in zip(enumerate(order), lColors):
            label = f'sweep {i+1}' if lbl else None
            plt.plot(t, o, ls, c=c, label=label)
        lbl = False
    plt.vlines(times[1:], 0, 10, colors='gray')
    plt.title('"-" = PFASST, "--s" = PFASST after "coarse" sweep')
    plt.xlabel('Time')
    plt.ylabel('Order')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()


# %% For those who don't use Spyder ...
plt.show()
