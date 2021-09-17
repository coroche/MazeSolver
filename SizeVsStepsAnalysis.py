import matplotlib.pyplot as plt
from MazeSolver import SolveMaze
import numpy as np

Lower=5			#lower limit of maze sizes
Upper=150		#upper limit of maze sizes
Increment=10	#increment of maze sizes
Sample = 20		#how many mazes to solve of each size
poly = 3		#order of line of best fit


def strsign(x):
	#returns the sing symbol of a number. For creating equation string to add to plot.
	if x>=0:
		return "+"
	else:
		return "-"

SizeRange = range(Lower,Upper,Increment)
StepCount=np.zeros([len(SizeRange),Sample], dtype=int) #array to store all solution lengths for each maze size

for i,size in enumerate(SizeRange):								#loop over each maze size
	for j in range(Sample):										#get a sample of solution lengths for each size
		X, Solution, tries = SolveMaze(size,size,0,.4,.6,False) #solves maze
		StepCount[i,j] = np.max(X) 								#gets the solution length
AverageSteps = np.average(StepCount, axis=1) 					#gets the average solution length for each size
STDSteps = np.std(StepCount, axis=1) 							#gets the standard deviation of solution lengths for each size

x = np.flip(np.polyfit(SizeRange, AverageSteps, poly))	#Line of best fit. Flip the returned array so lowest order of n is first

plt.errorbar(SizeRange, AverageSteps, yerr=STDSteps, fmt='o') #scatter plot average solution length with error bars

#create array and plot line of best fit
y=np.zeros([Upper])
for i in range(poly+1):
	y+=x[i]*np.array(range(Upper))**i
plt.plot(range(Upper), y)

ax = plt.gca() #name axes

#write line of best fit equation to string
x=np.around(x, decimals=3)
eq=str(x[0])+" "+strsign(x[1])+" "+str(abs(x[1]))+"n"
for i in range(2,poly+1):
	eq=eq+" "+strsign(x[i])+" "+str(abs(x[i]))+"$n^"+str(i)+"$"

#add equation to plot
tx=ax.get_xlim()[0]+0.05*(ax.get_xlim()[1]-ax.get_xlim()[0]) #x position of text
tx=ax.get_ylim()[0]+0.05*(ax.get_ylim()[1]-ax.get_ylim()[0]) #y position of text
plt.text(ax.get_xlim()[0]+0.1*(ax.get_xlim()[1]-ax.get_xlim()[0]),0.9*ax.get_ylim()[1],"Steps = "+eq)

#plot labels
ax.set_title("Steps Needed to Solve n*n Maze")
ax.set_xlabel("n")
ax.set_ylabel("No. of steps")
plt.show()