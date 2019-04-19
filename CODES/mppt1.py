import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt 
from sklearn.tree import DecisionTreeRegressor
from sklearn import tree
import collections
from scipy.signal import argrelextrema
import math 
from matplotlib.figure import Figure
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import sys
import subprocess
import datetime
#constants 
Ka = 50
Kf = 0.01
If = 2
Rf = 1
Ra = 3
#Functions for power calculations etc.
def convert(wss):
	x = []
	for y in wss:
		z = []
		z.append(y)
		x.append(z)
	return x

def findr(P,W):
	Ea = Ka*Kf*If*W
	a = 1
	b = (2*Ra - (Ea*Ea /P))
	c = Ra*Ra
	
	d = b*b-4*a*c
	
	if d < 0:
		return math.sqrt(-1*d)
	elif d == 0:
		x = (-b+math.sqrt(b*b-4*a*c))/2*a
		return np.float(x)
	else:
		x1 = (-b+math.sqrt(b*b-4*a*c))/2*a
		return np.float(x1)
	

def findV(w,r):
	Ea=Kf*Ka*If*w
	V=Ea*r/(Ra+r)
	return V

def findVP(P,r):
	m = P * (Ra + r)* ( Ra + r) * 1 /(r)
	return float(np.sqrt(m))

def findI(w,r):
	Ea=Kf*Ka*If*w
	return float(Ea/(Ra + r))

def findIP(P,r):
	e = findVP(P,r)
	return float(e/(Ra + r))
	
def Pow(r,w):
	Ea=Kf*Ka*If*w
	V=Ea*r/(Ra+r)
	I=Ea/(Ra+r)
	P=V*I
	
	return(np.float(P))
	
def pando(r,w):
	P1 = Pow(r,w)
	
	while(1):
		if(Pow(r+0.001,w)>P1):
			r=r+0.001
			P1=Pow(r,w)
		elif(Pow(r-0.001,w)>P1):
			r=r-0.001
			P1=Pow(r,w)
		else:	
			break
	return np.float(P1)			
	

#Variables 
P =list() #power
L =list() #Load
V =list() #Voltage
I =list() #Current 

#Train dats 
with open('windspeed_20.txt') as w:
	k = np.asarray(w.readlines(),np.float)
ws = [x * 360 for x in k]


with open('pressure.txt') as p:
	pr = np.asarray(p.readlines(),np.float)

with open('temp.txt') as t:
	te = np.asarray(t.readlines(),np.float)

with open('loaddata.txt') as load:
	ld = np.asarray(load.readlines(),np.float)

#FOR PLOTTING THE GRAPH AT W RPM
'''
for rl in range (0,5000):
	p = np.power((Ka*Kf*If*w[i]/(Ra+(rl/100))),2) * (rl/100)
	k.append(p)
	l.append(rl/100)
	
for rl in range (0,5000):
	v = Ka*Kf*If*w[i]/(Ra+(rl/100)) * (rl/100)
	i = Ka*Kf*If*w[i]/(Ra+(rl/100))
	V.append(v)
	I.append(i)
	
plt.figure(1)
plt.subplot(311)
plt.title("MPPT at Windspeed "+ str(w))
plt.ylabel("Power")
plt.xlabel("Load")
plt.plot(l,k)
plt.subplot(313)
plt.title("Voltage VS Current at "+ str(w))
plt.ylabel("Voltage")
plt.xlabel("Load")
plt.plot(I,V)
plt.show()
'''

#machine learning part 
#DATA WILL BE TRAINED CONTINUOUSLY TAKING THE DATA SET OF EVERY 2 HOUR DATA
#data containing the present trainset from 1st 125 minutes = 2 hour dataset

traindata = convert(ws)
loaddata =convert(ld)

import time 
jtag = time.time()

regr_1 = DecisionTreeRegressor(max_depth=1000)
regr_1.fit(traindata, loaddata)

timelapse = time.time() - jtag 

predict= []
freeinput = []
simulate = []

#plotting real time with 4 different wind sets 

import random
for i in range (1, 100):
	freeinput.append(i)
	temp = random.randint(400,440)
	predict.append(np.float(regr_1.predict([temp])))
	simulate.append(pando(0,temp))

'''
#for calculation of current vs time 
import random
for i in range (1,20):
	freeinput.append(i)
	temp = random.randint(400,410)
	p = np.float(regr_1.predict([temp]))
	load = findr(p,temp)
	predict.append(np.float(findIP(p,load)))
	simulate.append(np.float(findVP(p,load)))
'''


#plotting Power vs Load 

'''
for i in range(1,270000,1):
	freeinput.append(i/100)
	p= regr_1.predict([i/100])
	predict.append(p)
'''

#error calculation code
"""

for i in range(2,2000,1):
	freeinput.append(i)
	p= regr_1.predict([i])
	
	var = findr(np.float(p),i)
	var2 = pando(var,i)
	error = var2 - np.float(p)
	predict.append(error/var2)
"""

# calculation of time for P&O and ML P&O for same data 

'''
ktag = time.time() 
for i in range(0,100):	
	pando(0,600)
	pando(0,700)
	pando(0,800)
	pando(0,500)
	pando(0,400)
ktag = time.time() - ktag 
print "Time for normal P&O " + str(ktag) 
jtag =  time.time()
for i in range(0,100):
	pando(float(findr(float(regr_1.predict([600])),600)),600)
	pando(float(findr(float(regr_1.predict([700])),700)),700)
	pando(float(findr(float(regr_1.predict([800])),800)),800)
	pando(float(findr(float(regr_1.predict([500])),500)),500)
	pando(float(findr(float(regr_1.predict([400])),400)),400)
jtag = time.time() - jtag 
print "Time Using Modified P&O " + str(jtag + timelapse)
'''


plt.title(" Power Vs. time (s)")
plt.ylabel("Power ( Watts ) ")
plt.xlabel("Time in ( seconds )")
plt.plot(freeinput,predict,"r")
plt.plot(freeinput,simulate,"b")
plt.show()
