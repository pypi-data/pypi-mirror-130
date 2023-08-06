from GSKhopt.config import parse_config
from GSKhopt.GSKpy.GSKHpot import  GSKHpot
from GSKhopt.Logger import Logger
class Experiment():
    def __init__(self,name="default"):
        self.solver = None
        self.name = name
        self.obj_func = None
        self.upper_limit = None
        self.lower_limit = None
    def create_experiment_logger(self):
        self.logger = Logger(self.name+".csv",False)

    def run(self,popsize,nfes,verbose=True):
        g,best , best_fit, errors = self.solver.asynrun(self.obj_func, len(self.lower_limit), popsize, self.lower_limit, self.upper_limit,max_nfes=nfes,verbose=verbose,track=False,func_args=[0.1],logger=self.logger)
        return g,best,best_fit,errors
def create_experiment(config_file,eval):
    exp = Experiment()
    parameters_names,lower_limit,upper_limit,ranges = parse_config(config_file)
    print(parameters_names)
    print(lower_limit,len(lower_limit))
    #define a solver
    exp.solver = GSKHpot(k=10,kf=0.5,kr=0.9,p=0.1)
    eval.setParas(parameters_names,ranges)
    exp.obj_func = eval
    exp.upper_limit = upper_limit
    exp.lower_limit = lower_limit
    exp.create_experiment_logger()
    return exp
