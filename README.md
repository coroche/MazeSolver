# MazeSolver
_Generate, solve and animate solution to a random maze_

This project was inspired by a Numberphile video feat. Matt Henderson.  
[The Lightning Algorithm - Numberphile](https://youtu.be/akZ8JJ4gGLs)  
In the video he makes a comparison to lightning trying to find the path of least resistance to ground. I prefer to think of the maze solving algorithm as Nicolas Cage searching a factory in [this scene](https://youtu.be/lufECeWtN34) from the movie Next (2007). If an analogy can be made using Nic Cage I believe that it should.

### Generating a random maze
The first challenge was to figure out a data structure to store which walls were going to be present in the maze. For an `m*n` grid maze each cell has for walls so an `m*n*4` array would seem like the obvious choice. However, as neighbouring cells share walls, this would lead to a lot of redundant data and would introduce the possibility of contradicting data. In the end I opted to index horizontal and vertical walls separately and store them in binary lists. I then created an array of the start and end points for every wall in the grid and used the binary lists to delete a certain proportion of them at random.

### Solving the maze
Solving the maze ended up being more straightforward than generating the maze. I was able to make a function that used the binary lists of walls to return a 4 vector for each cell in the maze. This 4 vector would tell me what walls, if any, surrounded this cell. From the start point at the centre top of the grid I could then step through the maze assigning a step count to cells as I went, splitting the fronts if more than one step was possible. For simplicity, the fronts were stored in an array for save having to locate them on each step. Once a step exited the bottom of the maze I could then step back through the grid to find the shortest solution. If no solution is possible, i.e. all fronts lead to dead ends, then a new maze is generated.

### Animating the solution
I liked the idea of the step fronts pouring through the maze like liquid. Simply plotting the step indexes at each step achieved this pretty well so I used this to create the animation. Once a step front exits the bottom of the maze the path is then overlaid on the matrix of step indexes to highlight the solution.

![Maze64x64](https://user-images.githubusercontent.com/49063400/132883041-cff3159d-d90d-4964-b7ae-052c4406be1f.gif)

