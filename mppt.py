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
		if(Pow(r+0.0001,w)>P1): 
			r=r+0.0001
			P1=Pow(r,w)
		elif(Pow(r-0.0001,w)>P1):
			r=r-0.0001
			P1=Pow(r,w)
		else:	
			break
	return np.float(P1)			
	

#Variables 
P =list() #power
L =list() #Load
V =list() #Voltage
I =list() #Current 

#Train datas 

predict = [0]
freeinput = [0]
for count in range (1,3000):
	
	with open('windspeed_20.txt') as w:
		k = np.asarray(w.readlines()[:count],np.float)
	
			
	ws = [x * 360 for x in k]
	
	with open('loaddata.txt') as load:
		ld = np.asarray(load.readlines()[:count],np.float)
		
	traindata = convert(ws)
	loaddata =convert(ld)
	regr_1 = DecisionTreeRegressor(max_depth=1000)
	regr_1.fit(traindata, loaddata)	
	lua = 300
	p= regr_1.predict([lua])
	var = findr(np.float(p),lua)
	var2 = np.float(pando(var,lua))
	error = var2 - np.float(p)
	if error < 0:
		error = -error
	
	predict.append(error/var2)
	freeinput.append(count)

T = freeinput
power = predict

from scipy.interpolate import spline
xnew = np.linspace(1,140,10000)
power_smooth = spline(T,power,xnew)

plt.title(" Mean Error Vs. Iteration(s)")
plt.ylabel("Error")
plt.xlabel("Iteration")
plt.plot(xnew,power_smooth,"r")
plt.plot(freeinput,predict,"b")
plt.show()
