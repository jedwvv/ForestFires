import numpy as np
import matplotlib.pyplot as plt 
import time
import argparse
from ForestFire import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid_size", "-g", help="Set the square gridsize. Recommended: 50-1000", type = int)
    parser.add_argument("--no_trees", "-n_t", help="Set initial fraction of trees", type = float)
    parser.add_argument("--prob_burn", "-f", help="Set probability of spontaneous burning of a tree", type = float)
    parser.add_argument("--prob_regrow", "-p", help="Set probability of an empty site regrowing a tree", type = float)
    parser.add_argument("--no_steps", "-s", help="Set probability of number of steps", type = int)

    args = parser.parse_args()
    a = ForestFire( square_gridsize = args.grid_size, 
                initial_trees = args.no_trees,
                prob_burn = args.prob_burn,
                prob_regrow = args.prob_regrow
                )

    start = time.time()

    time_step = args.no_steps
    for i in range(time_step):
        a.step()
        a.measure_wait()

    end = time.time()
    print("Time taken: {}".format(np.round(end-start)))
    plt.hist(a.fire_wait_distributions, bins = 50)
    plt.show()


main()