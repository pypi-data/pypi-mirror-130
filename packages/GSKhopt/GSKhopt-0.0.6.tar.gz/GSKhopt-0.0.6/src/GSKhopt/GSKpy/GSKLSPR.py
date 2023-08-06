import numpy as np
import copy
import sys
from GSKpy.Gained_Shared_Junior_R1R2R3 import Gained_Shared_Junior_R1R2R3
from GSKpy.Gained_Shared_Senior_R1R2R3 import Gained_Shared_Senior_R1R2R3
from GSKpy.Gained_Shared_Middle_R1R2R3 import Gained_Shared_Middle_R1R2R3
from GSKpy.boundConstraint import boundConstraint
from GSKpy.GSK import GSK

class GSKPop(GSK):
    def __init__(self,k=10,kf=0.5,kr=0.9,p=0.1):
        GSK.__init__(self,k,kf,kr,p)
        self.best_hist=[]
        self.pop_hist=[]
        self.best_pop_hist = []
        self.middle_pop_hist = []
        self.worst_pop_hist = []
        self.errors = []
        self.junior_dim = []
        self.fitness_vals = []
        self.input = []
        self.output = []
    def reset(self,k=10,kf=0.5,kr=0.9,p=0.1):
        GSK.__init__(self,k,kf,kr,p)
    def getstatistics(self):
        return self.best_hist,self.fitness_vals, self.best_pop_hist, self.middle_pop_hist, self.worst_pop_hist, self.junior_dim
    def getdata(self):
        return self.input,self.output

    def asynrun(self,evaluation_func, problem_size, pop_size, low, high,optimum=100.0,val_2_reach=10 ** (- 8),func_args=None,max_nfes=1000,verbose= False):
        max_nfes= max_nfes
        #max_nfes =0
        max_pop_size = pop_size
        min_pop_size = 50
        popold = np.concatenate([np.random.uniform(low[i], high[i], size=(pop_size,1)) for i in range(problem_size)], axis=1)
        pop = popold
        max_diversity = 10000
        stag_count = 0
        best_found = False



        fitness = evaluation_func(pop,func_args)

        nfes = 0

        bsf_fit_var = 1e+300
        bsf_solution = popold[0]
        val_2_reach=10 ** (- 8)
        for i in range(pop_size):
            nfes = nfes + 1

            if nfes > max_nfes:
                break
            if fitness[i] < bsf_fit_var:
                bsf_fit_var = fitness[i]
        self.pop_hist = [pop]
        self.best_hist = [bsf_solution]

        K = np.full((pop_size, 1), self.K, dtype=int)
        Kf = np.array([self.Kf]*pop_size).reshape(pop_size,1)
        Kr = np.array([self.Kr]*pop_size).reshape(pop_size,1)
        g = 0
        while nfes < max_nfes:


            g = g + 1
            D_Gained_Shared_Junior = np.ceil(problem_size*((1 - nfes/max_nfes)**K))
            self.junior_dim.append(D_Gained_Shared_Junior[0])
            pop = popold

            indBest = np.argsort(fitness)
            best_idx = indBest[0]	# if fitness not np array use x = np.array([3, 1, 2]) to convert it

            Rg1,Rg2,Rg3 = Gained_Shared_Junior_R1R2R3(indBest)

            R1,R2,R3 = Gained_Shared_Senior_R1R2R3(indBest,self.p)

            R01 = range(pop_size)

            Gained_Shared_Junior = np.zeros((pop_size,problem_size))


            ind1 = fitness[R01] > fitness[Rg3] # fitness must be np.array
            if np.sum(ind1) > 0:
                Gained_Shared_Junior[ind1,:] = pop[ind1,:] + Kf[ind1,:] * np.ones((np.sum(ind1),problem_size)) * (pop[Rg1[ind1],:] - pop[Rg2[ind1],:] + pop[Rg3[ind1],:] - pop[ind1,:])

            ind1 = np.invert(ind1)
            if np.sum(ind1) > 0:
                Gained_Shared_Junior[ind1,:] = pop[ind1,:] + Kf[ind1,:] * np.ones((np.sum(ind1),problem_size)) * (pop[Rg1[ind1],:] - pop[Rg2[ind1],:] + pop[ind1,:] - pop[Rg3[ind1],:])
            R0 = range(pop_size)

            Gained_Shared_Senior = np.zeros((pop_size,problem_size))

            ind = fitness[R0] > fitness[R2]
            if np.sum(ind) > 0:
                Gained_Shared_Senior[ind,:] = pop[ind,:] + Kf[ind,:] * np.ones((np.sum(ind),problem_size)) * (pop[R1[ind],:] - pop[ind,:] + pop[R2[ind],:] - pop[R3[ind],:])

            ind = np.invert(ind)
            if np.sum(ind) > 0:
                Gained_Shared_Senior[ind,:] = pop[ind,:] + Kf[ind,:] * np.ones((np.sum(ind),problem_size)) * (pop[R1[ind],:] - pop[R2[ind],:] + pop[ind,:] - pop[R3[ind],:])

            boundConstraint(Gained_Shared_Junior,pop,low,high)
            boundConstraint(Gained_Shared_Senior,pop,low,high)

            D_Gained_Shared_Junior_mask = np.random.rand(pop_size,problem_size) <= (D_Gained_Shared_Junior[:] / problem_size)
            D_Gained_Shared_Senior_mask = np.invert(D_Gained_Shared_Junior_mask)
            D_Gained_Shared_Junior_rand_mask = np.random.rand(pop_size,problem_size) <= Kr
            D_Gained_Shared_Junior_mask = np.logical_and(D_Gained_Shared_Junior_mask,D_Gained_Shared_Junior_rand_mask)
            D_Gained_Shared_Senior_rand_mask = np.random.rand(pop_size,problem_size) <= Kr
            D_Gained_Shared_Senior_mask = np.logical_and(D_Gained_Shared_Senior_mask,D_Gained_Shared_Senior_rand_mask)

            ui = copy.deepcopy(pop)

            ui[D_Gained_Shared_Junior_mask] = Gained_Shared_Junior[D_Gained_Shared_Junior_mask]
            ui[D_Gained_Shared_Senior_mask] = Gained_Shared_Senior[D_Gained_Shared_Senior_mask]

            children_fitness = evaluation_func(ui,func_args)

            for i in range(pop_size):
                nfes = nfes + 1
                if nfes > max_nfes:
                    break
                if children_fitness[i] < bsf_fit_var:
                    bsf_fit_var = children_fitness[i]
                    bsf_solution = ui[i,:]
                    best_found = True

            bsf_error_val=bsf_fit_var - optimum


            conc = np.concatenate((fitness.reshape(-1,1),children_fitness.reshape(-1,1)), axis=1)
            Child_is_better_index = conc.argmin(axis=1)

            fitness = conc[range(conc.shape[0]),Child_is_better_index]#.reshape(-1, 1)
            popold = pop
            popold[Child_is_better_index == 1,:] = ui[Child_is_better_index == 1,:]

            self.best_pop_hist.append(pop[R1])
            self.middle_pop_hist.append(pop[R2])
            self.worst_pop_hist.append(pop[R3])
            self.fitness_vals.append([fitness[R1],fitness[R2],fitness[R3]])
            self.errors.append(bsf_error_val)

            if best_found:
                stag_count =0
            else:
                stag_count +=1
            diversity = (1/pop_size)*np.sqrt(np.sum(np.abs(fitness-(1/pop_size)*sum(fitness))))
            success_rate = np.sum(Child_is_better_index == 1)/pop_size
            plan_pop_size = round(min_pop_size+max_pop_size*((1-diversity)+(success_rate)))
            '''
            if success_rate > 0 and diversity > 0:
                plan_pop_size = pop_size-1
            elif success_rate ==0 and diversity ==0:
                plan_pop_size = pop_size+1
            elif success_rate==0 and diversity > 0:
                plan_pop_size = pop_size+1
            '''


            max_diversity = max(diversity,max_diversity)
            self.input.append([(max_nfes-nfes)/max_nfes,diversity/max_diversity,success_rate,pop_size/max_pop_size])

            if pop_size > plan_pop_size:
                #decrease the pop size
                inc = [0,1]
                reduction_ind_num = pop_size - plan_pop_size
                if plan_pop_size < min_pop_size:
                    reduction_ind_num = pop_size - min_pop_size
                    pop_size = min_pop_size
                else:
                    pop_size = plan_pop_size

                for r in range(reduction_ind_num):
                    indBest = np.argsort(fitness)
                    worst_ind = indBest[-1]
                    popold = np.delete(popold, worst_ind, 0)
                    pop = np.delete(pop, worst_ind, 0)
                    fitness = np.delete(fitness, worst_ind, 0)
                    K = np.delete(K, worst_ind, 0)
                    Kf = np.delete(Kf,worst_ind,0)
                    Kr = np.delete(Kr,worst_ind,0)
                best_idx = np.argsort(fitness)[0]
            elif pop_size < plan_pop_size:
                #increase pop size
                inc = [1,0]

                '''
                if plan_pop_size > max_pop_size:
                    plan_pop_size = max_pop_size
                    increase_ind_num = 0
                    pop_size = plan_pop_size
                else:
                    increase_ind_num = plan_pop_size - pop_size
                    pop_size = plan_pop_size
                '''
                increase_ind_num = plan_pop_size - pop_size
                pop_size = plan_pop_size
                #print(g,inc,plan_pop_size,pop_size,increase_ind_num)


                #R1,R2,R3 = Gained_Shared_Senior_R1R2R3(indBest,self.p)
                for r in range(increase_ind_num):
                    indBest = np.argsort(fitness)
                    best_ind = indBest[0]
                    new = np.concatenate([np.random.uniform(low[i], high[i], size=(1,1)) for i in range(problem_size)], axis=1)
                    f = evaluation_func(new.reshape(1,problem_size),func_args)
                    nfes+=1
                    popold = np.append(popold, new.reshape(1,problem_size), 0)
                    pop = np.append(pop, new.reshape(1,problem_size), 0)
                    fitness = np.append(fitness, f.reshape(1,), 0)
                    K = np.append(K, K[0].reshape(1,1), 0)
                    Kf = np.append(Kf,Kf[0].reshape(1,1),0)
                    Kr = np.append(Kr,Kr[0].reshape(1,1),0)
                best_idx = np.argsort(fitness)[0]

            if verbose:
                sys.stdout.write('{} {} - generation {} - pop_size {} - var {} -fittness {}- nfes {}\r'.format(diversity,success_rate,g,pop_size,np.var(pop),bsf_error_val,nfes))
                sys.stdout.flush()

            self.output.append([pop_size/max_pop_size,inc])
            new_pop = copy.deepcopy(pop)
            new_best = copy.deepcopy(bsf_solution)
            self.pop_hist.append(new_pop)
            self.best_hist.append(new_best)

            if bsf_error_val < val_2_reach:
                bsf_error_val=0
                break

        return g,bsf_solution,bsf_error_val,self.errors
