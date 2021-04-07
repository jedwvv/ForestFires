import numpy as np
import matplotlib.pyplot as plt 
import time
import argparse
from ForestFire import *
from joblib import Parallel, delayed
from multiprocessing import cpu_count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid_size", "-g", help="Set the square gridsize. Recommended: 50-1000")
    parser.add_argument("--no_trees", "-n_t", help="Set initial fraction of trees")
    parser.add_argument("--prob_burn", "-f", help="Set probability of spontaneous burning of a tree")
    parser.add_argument("--prob_regrow", "-p", help="Set probability of an empty site regrowing a tree")
    parser.add_argument("--no_steps", "-s", help="Set probability of number of steps")
    parser.add_argument("--no_restarts", "-r", help="Set the number of restarts")

    args = parser.parse_args()
    square_gridsize = int(args.grid_size) 
    initial_trees = float(args.no_trees)
    prob_burn = float(args.prob_burn)
    prob_regrow = float(args.prob_regrow)
    time_step = int(args.no_steps)
    no_restarts = int(args.no_restarts)

    start = time.time()

    fires = Parallel(n_jobs=cpu_count())(delayed(measure_firesize)(square_gridsize, initial_trees, prob_burn, prob_regrow, time_step) for _ in range(no_restarts))
    
    end = time.time()

    print("Time taken: {}".format(np.round(end-start)))

    plt.hist(fires, bins = 100)
    plt.gca().set(title='f={}, p={}, steps={}'.format(args.prob_burn, args.prob_regrow, args.no_steps), ylabel= 'No of samples', xlabel='No of red cells after {} steps'.format(args.no_steps))
    plt.show()
    
    
    

def measure_firesize(square_gridsize, initial_trees, prob_burn, prob_regrow, time_step):

    a = ForestFire( square_gridsize = square_gridsize, 
                    initial_trees = initial_trees,
                    prob_burn = prob_burn,
                    prob_regrow = prob_regrow
                    )
    
    #Advance simulation by number of time_steps
    for i in range(time_step):
        a.step()

    #Measure number of fires
    no_fires = a.fire_size()
    return no_fires



main()