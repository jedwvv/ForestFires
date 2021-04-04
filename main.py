import numpy as np
import matplotlib.pyplot as plt 
import time
import argparse
import matplotlib.animation as animation
from matplotlib import colors

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
        self.fire_wait_times = np.zeros(shape = (10,))
        self.fire_wait_points = np.random.randint(1, int(self.gridsize/10), size = (10, ))
        self.fire_wait_distributions = np.array([])

    def step(self):
        """Method to spread existing FIRE, extinguish, and regrow, and randomly burn, and keep track of those numbers
        """
        self.no_fires.append(self.fire_size())
        self.no_trees.append(self.measure_trees())

        grids = [self.grid.copy() for _ in range(4)]
        # print(self.grid)

        #Rule to randomly burn
        grid_lightning = self.random_fire(grids[0])
        # print("\n random burn: \n", grid_lightning)
        
        #Rule to regrow
        grid_regrow = self.regrow(grids[1])
        # print("\n regrow: \n", grid_regrow)

        #Rule to spread
        grid_spread = self.spread_fire(grids[2])
        # print("\n spread: \n", grid_spread)

        #Combine burning rules
        burn_grid = np.array((grids[3]+1 == grid_spread)|(grids[3]+1 == grid_lightning), dtype = int)
        # print("\n Combined burn: \n", burn_grid)

        #Combine rules
        self.grid = burn_grid + grid_regrow
        # print("\n New grid: \n", self.grid)

        self.measure_wait()

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
        on_fire = self.grid.copy()
        on_fire[on_fire != FIRE] = 0
        fire_size = np.sum(on_fire)/2
        del(on_fire)
        return int(fire_size)
    
    def measure_trees(self):
        trees = self.grid.copy()
        trees[trees != TREE] = 0
        no_trees = np.sum(trees)
        del(trees)
        return int(no_trees)

    def measure_wait(self):

        for i in range(10):
            if self.grid[self.fire_wait_points[i], self.fire_wait_points[i]] != FIRE:
                self.fire_wait_times[i] += 1
            else:
                self.fire_wait_distributions = np.append(self.fire_wait_distributions, self.fire_wait_times[i])
                self.fire_wait_times[i] = 0


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--grid_size", "-g", help="Set the square gridsize. Recommended: 50-1000")
    parser.add_argument("--no_trees", "-n_t", help="Set initial fraction of trees")
    parser.add_argument("--prob_burn", "-f", help="Set probability of spontaneous burning of a tree")
    parser.add_argument("--prob_regrow", "-p", help="Set probability of an empty site regrowing a tree")
    parser.add_argument("--no_steps", "-s", help="Set probability of maximum number of steps")

    args = parser.parse_args()
    a = ForestFire( square_gridsize = int(args.grid_size), 
                initial_trees = float(args.no_trees),
                prob_burn = float(args.prob_burn),
                prob_regrow = float(args.prob_regrow)
                )

    start = time.time()

    colors_list = [(0.2,0,0), (0,0.5,0), (1,0,0), 'red']
    cmap = colors.ListedColormap(colors_list)
    bounds = [0,1,2,3]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    fig, ax = plt.subplots(figsize = (50,50))

    plt.text(0, 0, 
    "no_trees={}, p={:.4f}, f={:.4f}, steps={}".format(float(args.no_trees), 
                                                        float(args.prob_burn), 
                                                        float(args.prob_regrow), 
                                                        args.no_steps), 
    size=10,
    ha="left", va="bottom",
    bbox=dict(boxstyle="square",
                ec=(1., 0.5, 0.5),
                fc=(1., 0.8, 0.8),
                )
    )
    
    im = ax.imshow( np.zeros(shape = (int(args.grid_size), int(args.grid_size))),
                    cmap=cmap,
                    norm=norm,
                    aspect = 'equal',
                    interpolation = 'none',
                    animated=True)

    def init():
        print("\nInitialising...\n")
        im.set_data(np.zeros(shape = (int(args.grid_size), int(args.grid_size))))
        
    max_time_step = int(args.no_steps)
    def update(time_step):
        if time_step != max_time_step:
            print("Step No: ", time_step)
            a.step()
            im.set_data(a.grid)
            return im
        else:
            s_t = 3
            for s in range(s_t):
                print("Figure closing in {} seconds...".format(int(s_t-s)))
                time.sleep(1)
            plt.close()
    
    
    anim = animation.FuncAnimation(fig, 
                                update,
                                init_func=init, 
                                frames=max_time_step+1, 
                                interval=1, 
                                # save_count = max_time_step+1, 
                                repeat = False
                                )
    plt.show()

    f = r"animation_no_trees={}_p={:.4f}_f={:.4f}_steps={}.gif".format(float(args.no_trees), 
                                                                float(args.prob_burn), 
                                                                float(args.prob_regrow), 
                                                                args.no_steps)

    anim.save(f)

    # print("\n waits: \n", a.fire_wait_distributions)
    # print("\n no trees: \n", a.no_trees)
    # print("\n no_fires: \n", a.no_fires)
    
    end = time.time()
    print("Time taken: {}".format(np.round(end-start)))

main()










