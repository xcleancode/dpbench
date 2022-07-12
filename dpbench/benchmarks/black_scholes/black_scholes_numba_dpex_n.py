# Copyright 2022 Intel Corporation
#
# SPDX-License-Identifier: Apache 2.0


from math import erf

from numpy import exp, log, sqrt

import numba as nb


@nb.vectorize(nopython=True)
def nberf(x):
    return erf(x)


# blackscholes implemented using numpy function calls
@nb.njit(parallel=True, fastmath=True)
def black_scholes_kernel(price, strike, t, rate, vol, call, put):
    mr = -rate
    sig_sig_two = vol * vol * 2

    P = price
    S = strike
    T = t

    a = log(P / S)
    b = T * mr

    z = T * sig_sig_two
    c = 0.25 * z
    y = 1.0 / sqrt(z)

    w1 = (a - b + c) * y
    w2 = (a - b - c) * y

    d1 = 0.5 + 0.5 * nberf(w1)
    d2 = 0.5 + 0.5 * nberf(w2)

    Se = exp(b) * S

    r = P * d1 - Se * d2
    call[:] = r  # temporary `r` is necessary for faster `put` computation
    put[:] = r - P + Se


def black_scholes(nopt, price, strike, t, rate, vol, call, put):
    black_scholes_kernel(price, strike, t, rate, vol, call, put)
