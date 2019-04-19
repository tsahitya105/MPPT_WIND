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
		return 0
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
	m = P * (Ra + r)* ( Ra + r) * 1 / r 
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
f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)

traindata = convert(ws)
loaddata =convert(ld)
regr_1 = DecisionTreeRegressor(max_depth=1000)
regr_1.fit(traindata, loaddata)
predict= []
freeinput = []

def animate():
	i1=d1.stdout.readline().strip()
	freeinput.append(float())
	predict.append(regr_1.predict([windspeed]))
	a.clear()
	a.title("Power Vs. RPM ")
	a.ylabel("Power ( Watts ) ")
	a.xlabel("RPM - (Generator) ")
	a.plot(freeinput,list(map(fat,predict)))
	
	

#fetching subprocesses time.pyplot

d1 = subprocess.Popen(['python', 'time.py'], stdout=subprocess.PIPE)
i1=d1.stdout.readline().strip()
predict=collections.deque(25*[float(i1)],maxlen=25)
ani = animation.FuncAnimation(f,animate, interval=999) 


