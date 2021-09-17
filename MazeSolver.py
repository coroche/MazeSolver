import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mc
import pylab as pl
from celluloid import Camera
import math
from os import startfile


#output_type
#0 - none
#1 - mp4 animation
#2 - plot solution
#3 - plot steps
#4 - gif animation




def SolveMaze(Height,Width,output_type,hp,vp,console_print):
	def rand_bin_array(p, N):
		#generates a random binary array of length N and probability p of and element being 0
		arr = np.zeros(N)
		arr[:round((1-p)*N)] = 1
		np.random.shuffle(arr)
		return arr

	def check_walls(point):
		#for a given point in the maze checks for walls above, below, left and right
		x=point[1]
		y=point[0]
		walls=np.zeros(4)
		walls[0]=HWallsBin[(y+1)*Width+x] #up
		walls[1]=HWallsBin[y*Width+x] #down
		walls[2]=VWallsBin[x*Height+y] #left
		walls[3]=VWallsBin[(x+1)*Height+y] #right
		walls=1-walls
		return walls

	def step(a,b,X,front,newfronts):
		#updates X matrix and stores new fronts when a new step is taken through maze
		X[front[0]+a,front[1]+b]=i
		if newfronts.size==0:
			newfronts=np.array([[front[0]+a,front[1]+b]])
		else:
			newfronts=np.append(newfronts,[[front[0]+a,front[1]+b]], axis=0)
		return newfronts

	if output_type in [1,2,3,4]:
		border=max(Height,Width)*.1 								#border for output
		fig, ax = plt.subplots(figsize=(6, (Height+2*border)/(Width+2*border)*6))		#figure to plot maze
		camera = Camera(fig)									#camera to snap plot for animation
		fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)		#remove whitespace around plot
		ax.axis('off')										#remove axis
		plt.xlim([-border,Width+border])							#set axis limits
		plt.ylim([-border,Height+border])

	#generates new mazes until one is solved
	solved=0
	tries=0
	while solved==0:
		HWallsBin=rand_bin_array(hp,Width*(Height+1)).astype(int) 	#binary array of which walls are to be deleted
		HWalls=np.nonzero(HWallsBin) 					#indexes of all horizontal walls for deletion


		VWallsBin=rand_bin_array(vp,Height*(Width+1)).astype(int)
		VWalls=np.nonzero(VWallsBin)

		HLine = np.zeros([Width*(Height+1),2,2])
		VLine = np.zeros([Height*(Width+1),2,2])
		#creates arrays of all walls, start point and end point
		for i in range(Height+1):
			for j in range(Width):
				HLine[Width*i+j,:,:]=[[(Width*i+j)%Width,math.floor((Width*i+j)/Width)],[(Width*i+j)%Width+1,math.floor((Width*i+j)/Width)]]

		for i in range(Width+1):
			for j in range(Height):
				VLine[Height*i+j,:,:]=[[math.floor((Height*i+j)/Height),(Height*i+j)%Height],[math.floor((Height*i+j)/Height),(Height*i+j)%Height+1]]

		#removes walls marked for deletion
		HLine=np.delete(HLine,HWalls,0)
		VLine=np.delete(VLine,VWalls,0)

		#for plotting
		lc1 = mc.LineCollection(VLine, colors='black', linewidths=2)
		lc2 = mc.LineCollection(HLine, colors='black', linewidths=2)

		#matrix to fill with step indices
		X=np.zeros([Height,Width], dtype=int)
		start=round((Width-1)/2)
		X[-1,start]=1
		fronts=np.array([[Height-1,start]]) #stores the position of each front

		i=2
		
		while fronts.size!=0 and solved==0: #while the bottom has yet to be reached and there are still active fronts
			newfronts=np.array([])
			for front in fronts:
				#up
				#if the is no wall above and the is space above and the above position hasn't been stepped into already add new front above
				if check_walls(front)[0]==0 and front[0]!=Height-1 and X[front[0]+1,front[1]]==0: 
					newfronts=step(1,0,X,front,newfronts)
				
				#down
				if check_walls(front)[1]==0:		#if there is no wall below
					if front[0]==0:			#if on the bottom row then the maze is solved
						solved=1
						finish=front[1] 	#x coordinate of final position
						break
					elif X[front[0]-1,front[1]]==0:	#if not on the bottom row and the below position hasn't been stepped into new front below
						newfronts=step(-1,0,X,front,newfronts)
				
				#left
				if check_walls(front)[2]==0 and front[1]!=0 and X[front[0],front[1]-1]==0:
					newfronts=step(0,-1,X,front,newfronts)
				
				#right
				if check_walls(front)[3]==0 and front[1]!=Width-1 and X[front[0],front[1]+1]==0:
					newfronts=step(0,1,X,front,newfronts)

			fronts=newfronts
			i+=1

			if output_type in [1,4] and solved==0: #exclude the last frame. This will be added with the solution
				ax.add_collection(lc1) #add maze walls
				ax.add_collection(lc2)
				ax.imshow(X, cmap='hot_r', interpolation='nearest', extent =[0, Width, 0, Height], origin='lower', vmin=0, vmax=3*i) #plot steps
				camera.snap() #snap plot for animation

		if solved==0:
			if console_print:
				print("This maze is unsolvable. Generating new maze.")
			if output_type in [1,4]:
				camera = Camera(fig) #clears frames
			tries+=1
		else:
			if console_print: 
				print("Solved!")

	imax=i-1
	#back track along shortest solution to find path
	i-=2
	Solution=np.zeros([Height,Width]) #Stores the solution path
	Solution[0,finish]=1
	Solution[-1,start]=1
	position=np.array([0,finish])
	while position[0]!=Height-1 or position[1]!=start:
		previous_step=np.array([np.where(X==i)[0],np.where(X==i)[1]])
		previous_step=np.transpose(previous_step)	
		prev_index=np.where(np.sum(abs(position-previous_step), axis=1)==1)
		#if there's only one other possible previous step use that one
		if previous_step[prev_index].shape[0]==1:
			position=previous_step[prev_index][0]
		#if there are multiple look for one that doesn't go through a wall
		else:
			for j,step in enumerate(previous_step[prev_index]):
				#works out the direction of the step and looks for a wall in that direction
				#up
				if np.array_equal(step-position,np.array([1,0])) and check_walls(position)[0]!=1:
					#if there is no wall use that step
					position=previous_step[prev_index][j]
					break

				#down
				elif np.array_equal(step-position,np.array([-1,0])) and check_walls(position)[1]!=1:
					position=previous_step[prev_index][j]
					break

				#left
				elif np.array_equal(step-position,np.array([0,-1])) and check_walls(position)[2]!=1:
					position=previous_step[prev_index][j]
					break

				#right
				elif np.array_equal(step-position,np.array([0,1])) and check_walls(position)[3]!=1:
					position=previous_step[prev_index][j]
					break
		
		Solution[position[0],position[1]]=1 #store step in solution matrix
		i-=1

	if output_type in [1,4]:
		display=np.maximum(X,2*imax*Solution) #overlay solution on step matrix
		for n in range(20):
			ax.add_collection(lc1)
			ax.add_collection(lc2)
			ax.imshow(display, cmap='hot_r', interpolation='nearest', extent =[0, Width, 0, Height], origin='lower', vmin=0, vmax=3*imax)
			camera.snap() #snap plot for animation 20 frames (2 secs)

		animation = camera.animate(interval=.1) #animate
		if output_type==1:
			if console_print:
				print("Creating mp4 file...")
			animation.save('Maze.mp4', fps=10, extra_args=['-vcodec', 'libx264']) 	#save mp4 animation
			startfile('Maze.mp4')
		else:
			if console_print:
				print("Creating gif file...")
			animation.save('Maze.gif', fps=10, writer = 'imagemagick')		#save gif animation (more expensive)
			startfile('Maze.gif')

	#plot results
	if output_type in [2,3]:
		Solution[0,finish]=2 #highlights start and end points
		Solution[-1,start]=2
		ax.add_collection(lc1)
		ax.add_collection(lc2)
		if output_type==2:
			ax.imshow(Solution, cmap='Greens', interpolation='nearest', extent =[0, Width, 0, Height], origin='lower', vmin=0)
		if output_type==3:
			ax.imshow(X, cmap='Reds', interpolation='nearest', extent =[0, Width, 0, Height], origin='lower', vmin=0)
		plt.show()

	return X, Solution, tries	#returns step matrix, solution path and the number of attempts at generating a solvable maze
