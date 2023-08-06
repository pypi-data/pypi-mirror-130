import numpy as np
import collections
def mapsol(self,sol,ranges):
    _solution_exits = False
    blocks = round(sol[0])
    cnns = [round(x) for x in sol[1:blocks+1]]
    filters = []
    kernels = []
    i = 4
    for _ in range(blocks):
        filters.append(find_nearest(ranges["filters"],round(sol[i])))
        kernels.append(find_nearest(ranges["kernels"],round(sol[i+1])))
        i+=2
    fully_connected = round(sol[16])
    i = 17
    fc = []
    for _ in range(fully_connected):
        fc.append(find_nearest(ranges["fcs"],round(sol[i])))
        i+=1
    dropout = sol[20]
    lr = sol[21]
    batch_size = find_nearest(ranges["batch size"],round(sol[22]))
    parameters = {"blocks":blocks, "cnns":cnns, "filters": filters, "kernels":kernels, "dropout":dropout,
    "num_fcs":fully_connected, "fcs": fc, "lr":lr , "batch size":batch_size}
    if parameters in self.solutions_history:
        self.solutions_history.update(parameters, self.solutions_history[parameters])
        _solution_exits = True
    else:
        self.solutions_history.update(parameters, None)
    return _solution_exits,parameters
def flattenlist(l):
    #takes a list of lists and convert it to a flat list
    #returns list and its length
    flat_list = []
    for sublist in l:
        for item in sublist:
            flat_list.append(item)
    return flat_list, len(flat_list)
def find_nearest(array, value):
    #find the find nearest element in a list
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]
import collections

class FrozenDict(collections.Mapping):
    """Don't forget the docstrings!!"""

    def __init__(self, *args, **kwargs):
        self._d = dict(*args, **kwargs)

    def __iter__(self):
        return iter(self._d)

    def __len__(self):
        return len(self._d)

    def __getitem__(self, key):
        return self._d[key]
    def __hash__(self):
        return hash(tuple(sorted(self._d.iteritems())))
