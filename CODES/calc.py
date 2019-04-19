import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.figure import Figure

f =[]
g =[]
beta = 0.000000000001
for lambd in range (1, 18000):
	lambdai = np.double(np.power((1/(lambd/1000 + 0.08*beta) - 0.035/(1+beta*beta*beta)),-1))
	f.append(np.double((0.5*(116*1/lambdai - 0.4*beta - 5)*np.exp(-21/lambdai))))
	g.append(np.double(lambd))
plt.plot(g,f)
plt.show()