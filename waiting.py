import numpy as np
import matplotlib.pyplot as plt 
import time
import argparse
from ForestFire import *

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

    time_step = int(args.no_steps)
    for i in range(time_step):
        a.step()
        a.measure_wait()
    
    print(a.fire_wait_distributions)

    end = time.time()
    print("Time taken: {}".format(np.round(end-start)))

main()