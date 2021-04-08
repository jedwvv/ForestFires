import matplotlib.pyplot as plt 
import time
import argparse
import matplotlib.animation as animation
from matplotlib import colors
from ForestFire import *

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid_size", "-g", help="Set the square gridsize. Recommended: 50-1000", type = int)
    parser.add_argument("--no_trees", "-n_t", help="Set initial fraction of trees", type = float)
    parser.add_argument("--prob_burn", "-f", help="Set probability of spontaneous burning of a tree", type = float)
    parser.add_argument("--prob_regrow", "-p", help="Set probability of an empty site regrowing a tree", type = float)
    parser.add_argument("--no_steps", "-s", help="Set probability of maximum number of steps", type = int)
    parser.add_argument("--save", help="Set to True if you want to save animation, False otherwise by default", type = bool, default=False)

    args = parser.parse_args()
    a = ForestFire( square_gridsize = args.grid_size, 
                initial_trees = args.no_trees,
                prob_burn = args.prob_burn,
                prob_regrow = args.prob_regrow
                )

    start = time.time()
    
    #Visualization tools
    colors_list = [(0.2,0,0), (0,0.5,0), (1,0,0), 'red']
    cmap = colors.ListedColormap(colors_list)
    bounds = [0,1,2,3]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    fig, ax = plt.subplots(figsize = (50,50))

    #Add text to animation
    plt.text(0, 0, 
    "no_trees={}, f={:.8f}, p={:.8f}, steps={}".format(float(args.no_trees), 
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
    
    #Initialise mpl axes
    im = ax.imshow( np.zeros(shape = (int(args.grid_size), int(args.grid_size))),
                    cmap=cmap,
                    norm=norm,
                    aspect = 'equal',
                    interpolation = 'none',
                    animated=True)

    #Define how to initialise the axes in FuncAnimation
    def init():
        print("\nInitialising...\n")
        im.set_data(np.zeros(shape = (int(args.grid_size), int(args.grid_size))))
    
    #Define how to update data in each step within FuncAnimation
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
                print("Figure closing/terminating in {} seconds...".format(int(s_t-s)))
                time.sleep(1)
            plt.close()
    
    # Declare and show FuncAnimation object
    anim = animation.FuncAnimation(fig, 
                                update,
                                init_func=init,
                                frames=max_time_step+1, 
                                interval=1, 
                                save_count = max_time_step+1, 
                                repeat = False
                                )
    plt.show()
    
    if args.save:
        f = r"animation_size={}_no_trees={}_p={:.4f}_f={:.4f}_steps={}.gif".format( int(args.grid_size),
                                                                                    float(args.no_trees), 
                                                                                    float(args.prob_burn), 
                                                                                    float(args.prob_regrow), 
                                                                                    args.no_steps)
        anim.save(f) 

                                           
    end = time.time()
    print("Time taken: {}".format(np.round(end-start)))

main()










