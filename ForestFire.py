import numpy as np
import copy 

class ForestFire:
    global EMPTY
    global TREE
    global FIRE

    EMPTY, TREE, FIRE = 0, 1, 2

    def __init__(self, square_gridsize, initial_trees = 0, prob_burn = 0, prob_regrow = 0):
        """Make a ForestFire object that represents a grid, each cell can be empty, tree, or burning at any given timestep

        Args:
            square_gridsize ([int]): [The size of the square grid, given as one integer]
            initial_trees (double, optional): [Percentage of initial trees]. Defaults to 0.
            prob_burn (double, optional): [Probability of a tree randomly catching fire (e.g. from a lightning strike)]. Defaults to 0.
            prob_regrow (double, optional): [Probability of an empty cell becoming green]. Defaults to 0.
        """
        self.gridsize = square_gridsize
        self.initial_trees = initial_trees
        self.prob_burn = prob_burn
        self.prob_regrow = prob_regrow
        self.grid = np.random.choice([EMPTY, TREE], size = (self.gridsize, self.gridsize), p = [1-self.initial_trees, self.initial_trees])
        self.no_fires = []
        self.no_trees = []
        self.fire_wait_times = np.zeros(shape = (20,))
        self.fire_wait_points = np.random.randint(1, int(self.gridsize/10), size = (20, ))
        self.fire_wait_distributions = np.array([])
        self.grid_copy = copy.deepcopy(self.grid)


    def step(self):
        """Method to spread existing FIRE, extinguish, and regrow, and randomly burn, and keep track of those numbers
        """
        self.no_fires.append(self.fire_size())
        self.no_trees.append(self.measure_trees())

        grids = [self.grid.copy() for _ in range(4)]
        
        #Rule to spontaneously burn
        grid_lightning = self.random_fire(grids[0])
        
        #Rule to regrow
        grid_regrow = self.regrow(grids[1])

        #Rule to spread
        grid_spread = self.spread_fire(grids[2])

        #Combine burning rules, where now it is a 1 if it is burning. 
        burn_grid = np.array((grids[3]+1 == grid_spread)|(grids[3]+1 == grid_lightning), dtype = int)

        #Combine burning + regrow rules
        self.grid = burn_grid + grid_regrow

        del(grids, grid_lightning, grid_regrow, grid_spread, burn_grid)
    
    def spread_fire(self, grid):
        #Make a grid of where the fire is, then spread it and 
        fire_grid = grid.copy()
        fire_grid[fire_grid != 2] = 0
        fire_up = np.roll(fire_grid, 1, axis=0) #Fire moves up
        fire_down = np.roll(fire_grid, -1, axis=0) #Fire moves down
        fire_left = np.roll(fire_grid, 1, axis=1)#Fire moves left
        fire_right = np.roll(fire_grid, -1, axis=1)#Fire moves right
        fire_spread = fire_up + fire_down + fire_left + fire_right
        fire_spread[fire_spread >= 2] = 2 #If more than one fire neighbour, make it only act as one
        grid[grid == FIRE] = EMPTY #Extinguish
        fire_grid = np.array( grid+1 == fire_spread, dtype = int )
        grid += fire_grid
        del(fire_grid, fire_up, fire_down, fire_left, fire_right, fire_spread)
        return grid

    def random_fire(self, grid):
        #Adds 1 to where its 1 with probability. 1>2 (TREE>FIRE)
        fire_grid = np.random.choice([3, 1], size = grid.shape, p = [1-self.prob_burn, self.prob_burn])
        fire_grid = np.array(fire_grid == grid, dtype=int)
        grid += fire_grid
        del(fire_grid)
        return grid

    def regrow(self, grid):
        #Adds 1 to where its 0 with probability. 0>1 (EMPTY>TREE)
        regrow_grid = np.random.choice([3, 0], size = grid.shape, p = [1-self.prob_regrow, self.prob_regrow])
        regrow_grid = np.array(regrow_grid == grid, dtype=int)
        grid += regrow_grid
        grid[grid == 2] = 0 #Don't affect burning
        del(regrow_grid)
        return grid

    def fire_size(self):
        #Returns number of FIRE cells
        on_fire = self.grid.copy()
        on_fire[on_fire != FIRE] = 0
        fire_size = np.sum(on_fire)/2
        del(on_fire)
        return int(fire_size)
    
    def measure_trees(self):
        #Returns number of TREE cells
        trees = self.grid.copy()
        trees[trees != TREE] = 0
        no_trees = np.sum(trees)
        del(trees)
        return int(no_trees)

    def measure_wait(self):
        #Updates waiting times data
        for i in range(20):
            if self.grid[self.fire_wait_points[i], self.fire_wait_points[i]] != FIRE:
                self.fire_wait_times[i] += 1
            else:
                self.fire_wait_distributions = np.append(self.fire_wait_distributions, self.fire_wait_times[i])
                self.fire_wait_times[i] = 0
