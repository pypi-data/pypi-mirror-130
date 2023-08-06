from GSKpy.BasicGSK import  BasicGSK
from GSKpy.GSKLSPR import GSKPop
import numpy as np
from Objectives.KerasCNN import KerasCNN
from CSVDataFrame import CSVDataFrame
from GSKpy.viz import Viz
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import interactive
from Experiment import create_experiment
if __name__ == '__main__':
    objective = KerasCNN()
    exp = create_experiment("config.json",objective)
    exp.run(100,1000,True)

'''
for run_id in range(runs_no):
    g,best , best_fit, errors = solver.asynrun(obj_func, dim, popsize, low_limit, up_limit,optimum=0.0, max_nfes=100,func_args=[dim,func+1],verbose=True)
    runs.append(best_fit)
    print()
    print('run {}- best fit: {}'.format(run_id+1,best_fit))
    #visualize the run
    best_hist,fitness_vals, best, middle, worst,junior_dim = solver.getstatistics()

    best_hist = np.array(best_hist)
    best_hist = np.vstack((best_hist))
    best_hist = best_hist.reshape((best_hist.shape[0],dim))

    vis.set(dim,func+1,best_hist,fitness_vals,best,middle,worst)
    vis.build_plot()
    x = np.linspace(0,g,100)
    anims = []

    y1 = np.array(errors)
    f1, ax = plt.subplots(1)
    l1, = ax.plot([], [], 'o-', label='f'+str((func+1)), markevery=[-1])
    ax.legend(loc='upper right')
    ax.set_xlim(0,g)
    ax.set_ylim(0,max(errors))



    def animate(i):
        l1.set_data(x[:i], y1[:i])
        return l1,

    ani = animation.FuncAnimation(f1, animate, frames=100, interval=10)
    anims.append(ani)
    #ani.save("movie.mp4")

    plt.show()

    y1 = np.array(junior_dim)
    y2 = dim-y1

    f2, ax1 = plt.subplots()
    l1, = ax1.plot([], [], 'o-', label='junior dimensions rate', markevery=[-1])
    l2, = ax1.plot([], [], 'o-', label='senior dimensions rate', markevery=[-1])
    ax1.legend(loc='upper right')
    ax1.set_xlim(0,g)
    ax1.set_ylim(0,max(y1))


    def animatetwo(i):
        l1.set_data(x[:i], y1[:i])
        l2.set_data(x[:i], y2[:i])
        return (l1,l2)

    ani = animation.FuncAnimation(f2, animatetwo, frames=100, interval=10)
    anims.append(ani)
    #ani.save("movie2.mp4")

    plt.show()




runs = np.array(runs)
print('Best = {}, Worst = {} mean= {},SD = {}, Median {}'.format(np.min(runs),np.max(runs),np.mean(runs), np.std(runs),np.median(runs)))
frame.append([func+1,np.min(runs),np.median(runs),np.mean(runs),np.max(runs),np.std(runs)])
resframe.PassDataFrame(frame)
resframe.save('results/results-cec-2017-{}{}.csv'.format(dim,kf))
'''
