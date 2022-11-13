#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 20:22:02 2022

@author: anders
"""

import numpy as np
import matplotlib.pyplot as plt

d = np.loadtxt('ada4898_vnoise.txt',delimiter=',')
dd = np.loadtxt('ada4898_inoise.txt',delimiter=',')

vf=d[:,0]
vn=d[:,1]
inf=dd[:,0]
inn=dd[:,1]

def vnoise(f):
    return 1e-9*(0.88 + 3/f)

def inoise(f):
    return 1e-12*(2.4 + 8/pow(f,0.7))


def n_vnoise(n,f):
    """
    voltage noise of N parallell amplifiers
    """
    return vnoise(f)/np.sqrt(n)

def johnson_noise(R):
    """
    voltage noise of resistor at room temperature
    """
    T=300 # temperature
    kB = 1.380649e-23 # Boltzmann constant
    vj = 4*kB*T*R
    return np.sqrt(vj)

def n_onoise(n, f, R):
    """
    total input-referred amplifier noise with source-resistance R
    """
    vn = n_vnoise(n,f)
    vi = np.sqrt(n)*inoise(f)*R
    T=300 # temperature
    kB = 1.380649e-23 # Boltzmann constant
    vj = 4*kB*T*R
    return np.sqrt( pow(vn,2) + pow(vi,2) + vj)

f = np.logspace(0,5,200)
plt.figure()
plt.subplot(2,2,1)
plt.loglog(vf,vn,'bo',label='voltage noise')
plt.loglog(f, 1e9*vnoise(f),'b-')

plt.loglog(inf,inn,'r*',label='current noise')
plt.loglog(f, 1e12*inoise(f),'r-')

plt.loglog(f, 1e9*n_vnoise(16,f),'k-',label='Voltage noise, N=16 AD4898 in parallell')
plt.ylabel('Voltage, Current noise / nV/sqrt(Hz), pA/sqrt(Hz)')
plt.xlabel('Frequency / Hz')

plt.grid()
plt.legend()
plt.title('ADA4898 op-amp noise')

plt.subplot(2,2,2)
def dBV(vn):
   return 20*np.log10(vn) 

plt.semilogx(f,  n_onoise(16,f,0) ,'-',label='N=16, output shorted')
plt.semilogx(f,  n_onoise(16,f,50) ,'-',label='N=16, 50 Ohm')
plt.semilogx([min(f), max(f)],  np.array([johnson_noise(50), johnson_noise(50)]) ,'--',label='50 Ohm Johnson noise 0.9 nV/sqrt(Hz)')

#plt.semilogx(f, dBV( n_onoise(16,f,500) ),'-',label='N=16, 500 Ohm')
#plt.semilogx([min(f), max(f)], dBV( np.array([johnson_noise(500), johnson_noise(500)]) ),'--',label='500 Ohm Johnson noise')
#plt.semilogx(f, dBV( n_onoise(16,f,1000) ),'-',label='N=16, 1000 Ohm')

plt.ylabel('input-referred voltage noise / V/sqrt(Hz)')
plt.xlabel('Frequency / Hz')
plt.title('N=16 ADA4898 op-amps in parallell')

plt.grid()
plt.legend()


plt.subplot(2,2,3)
rs=np.linspace(0,300,500)
plt.plot(rs, johnson_noise(rs),'k-',label='Rs johnson noise')
plt.plot(rs, np.sqrt(1)*inoise(1e3)*rs,'--',label='In*Rs, noise from amplifier current-noise through Rs, at 1 kHz')
plt.plot(rs, n_onoise(1, 1e3, rs),'-',label='total ADA4898 noise, at 1 kHz')

plt.ylabel('input-referred voltage noise / V/sqrt(Hz)')
plt.xlabel('Source Resistance / Ohm')
plt.title('N=1, one ADA4898 op-amp')

plt.grid()
plt.legend()
plt.ylim((0,4e-9))


plt.subplot(2,2,4)
rs=np.linspace(0,300,500)
plt.plot(rs, johnson_noise(rs),'k-',label='Rs johnson noise')
plt.plot(rs, np.sqrt(16)*inoise(1e3)*rs,'--',label='sqrt(16)*In*Rs, noise from amplifier current-noise through Rs, at 1 kHz')
plt.plot(rs, n_onoise(16, 1e3, rs),'-',label='N=16 total LNA noise, at 1 kHz')
plt.plot(rs, n_onoise(1, 1e3, rs),'-.',label='N=1, one op-amp noise, at 1 kHz')

plt.ylabel('input-referred voltage noise / V/sqrt(Hz)')
plt.xlabel('Source Resistance / Ohm')
plt.title('N=16 op-amps in parallell')
plt.ylim((0,4e-9))
plt.grid()
plt.legend()


