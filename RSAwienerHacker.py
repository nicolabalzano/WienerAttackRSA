'''
Created on Dec 14, 2011

@author: pablocelayes
'''
import sys
sys.path.append('/home/alocin/Documents/hacking/util/WienerAttackRSA')
import ContinuedFractions, Arithmetic

def wiener_attack(e, N, max_k=2**20):
    d=hack_RSA(e, N)
    return get_factor(N, e, d, max_k)

def get_small_e_and_factors(d, N):
    '''Cerca e piccolo avendo d grande'''
    _, convergents = ContinuedFractions.rational_to_contfrac(d, N)
    
    for (k, e) in convergents:
        if k != 0 and (e * d - 1) % k == 0:
            phi = (e * d - 1) // k
            s = N - phi + 1
            discr = s * s - 4 * N
            if discr >= 0:
                t = Arithmetic.is_perfect_square(discr)
                if t != -1 and (s + t) % 2 == 0:
                    p = (s + t) // 2
                    q = (s - t) // 2
                    if p * q == N:
                        return e, p, q
    return None, None, None


def get_small_d(e,n):
    '''
    Finds d knowing (e,n)
    applying the Wiener continued fraction attack
    '''
    _, convergents = ContinuedFractions.rational_to_contfrac(e, n)
    
    for (k,d) in convergents:
        
        #check if d is actually the key
        if k!=0 and (e*d-1)%k == 0:
            phi = (e*d-1)//k
            s = n - phi + 1
            # check if the equation x^2 - s*x + n = 0
            # has integer roots
            discr = s*s - 4*n
            if(discr>=0):
                t = Arithmetic.is_perfect_square(discr)
                if t!=-1 and (s+t)%2==0:
                    return d

# Ora che hai e e d, puoi calcolare φ(N)
from math import isqrt

def get_factor(N, e, d, max_k=1000):
    for k in range(1, max_k):
        # e * d = k * φ(N) + 1
        if (e * d - 1) % k != 0:
            continue
        
        phiN = (e * d - 1) // k
        
        # φ(N) = (p-1)(q-1) = N - p - q + 1
        # Quindi: p + q = N - φ(N) + 1
        s = N - phiN + 1  # somma p + q
        
        # p e q sono radici di: x^2 - sx + N = 0
        # discriminante: s^2 - 4N
        discr = s * s - 4 * N
        
        if discr < 0:
            continue
        
        sqrt_discr = isqrt(discr)
        if sqrt_discr * sqrt_discr != discr:
            continue
        
        p = (s + sqrt_discr) // 2
        q = (s - sqrt_discr) // 2
        
        if p * q == N:
            return p, q
    
    return None, None
