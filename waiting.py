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
    weights = np.ones_like(a.fire_wait_distributions)/len(a.fire_wait_distributions)
    plt.hist(a.fire_wait_distributions, bins = 50, weights = weights)
    plt.legend(
        labels = ["f={}, p={}, steps={}, samples=50 cells".format(args.prob_burn, args.prob_regrow, args.no_steps)] ,
        fontsize= 'medium',
        loc = "upper right"
        )
    ax = plt.gca()
    ax.set_title(label='Fraction of samples vs waiting times'.format(len(a.fire_wait_distributions)), fontsize = 'x-large')
    ax.set_ylabel(ylabel = 'Fraction of samples', fontsize = 'large')
    ax.set_xlabel(xlabel='Waiting times between fires', fontsize = 'large' )
    plt.show()


main()