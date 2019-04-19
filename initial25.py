import numpy as np
Ka = 50.000
Kf = 0.0100
If = 2.000
Rf = 1.000
Ra = 3.000

def Pow(r,w):
	Ea=np.float(Kf*Ka*If*w)
	V=np.float(Ea*r/(Ra+r))
	I=np.float(Ea/(Ra+r))
	P=np.float(V*I)

	return(np.float(P))
	
def pando(r,w):
	P1 = Pow(r,w)
	
	while(1):
		if(Pow(r+0.01,w)>P1):
			r=r+0.01
			P1=Pow(r,w)
		elif(Pow(r-0.01,w)>P1):
			r=r-0.01
			P1=Pow(r,w)
		else:	
			break
	return np.float(P1)			
l = []
k = []
l1 = []
k1 = []
for r in range (1,1300):
	o = Pow(np.float(r/100),np.float(600))
	k.append(np.float(o))
	
	l.append(np.float(r/100))

for r in range (1,1300):
	o = Pow(np.float(r/100),np.float(1000))
	k1.append(np.float(o))
	
	l1.append(np.float(r/100))
import matplotlib.pyplot as plt
plt.title("Power Vs Load at Constant RPM")
plt.ylabel("Power ( Watts ) ")
plt.xlabel("Load Impedance")
l = np.array(l)	
k = np.array(k)
plt.plot(l,k)
plt.plot(l1,k1)

plt.show()