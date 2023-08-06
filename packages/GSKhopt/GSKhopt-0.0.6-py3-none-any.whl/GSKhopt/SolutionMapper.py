from GSKhopt.utils import find_nearest, FrozenDict
class SolutionMapper():
    def __init__(self,names,ranges,keep_for="ever"):
        self.solutions_history = dict()
        self.solutions_tracker = dict()
        self.ranges = ranges
        self.names = names
        print(self.ranges,self.names)
    def mapsol(self,sol):
        _solution_exits = False
        parameters = {}
        for i,name in enumerate(self.names):
            if name in self.ranges:
                #cat values
                parameters[name]= find_nearest(self.ranges[name],round(sol[i]))
            else:
                parameters[name]= sol[i]
        arch_str = str(parameters)
        if arch_str in self.solutions_history.keys():
            self.solutions_history.update({arch_str: self.solutions_history[arch_str]})
            _solution_exits = True
        else:
            self.solutions_history.update({arch_str: None})



        return _solution_exits,parameters
    def getsolutionvalue(self,parameters):
        #get the last score value for this parameters setting
        try:
            value = self.solutions_history[str(parameters)]
        except KeyError:
            print("This parameter setting never existed or may be deleted by solution tracking")
