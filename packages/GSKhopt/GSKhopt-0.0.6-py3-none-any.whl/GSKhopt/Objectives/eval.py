import numpy as np
from tensorflow import keras
from sklearn.model_selection import train_test_split
from GSKhopt.utils import mapsol
from GSKhopt.SolutionMapper import SolutionMapper
from GSKhopt.Models import buildModel
import multiprocessing
import sys
import scipy

def euclid_dist(t1, t2):
    return np.sqrt(((t1-t2)**2).sum(axis = 1))
def get_nearest_solution(sol,pop):
    return np.argmin(euclid_dist(sol,pop))
def assign(pop,pop_p,scores):
    new_scores = np.zeros(scores.shape[0],)
    for i,score in enumerate(scores):
        if score == 0:
            #assign
            index = get_nearest_solution(pop[i],pop_p)
            new_scores[i] = scores[index]
        else:
            new_scores[i]= scores[i]
    return new_scores

class EvaluationFunction(object):
    def __init__(self):
        self.train_data = None
        self.val_data = None
        self._data_loaded = False
        self.input_shape = None
        self.num_classes = 1

    def setParas(self,names,ranges):
        self.ranges = ranges
        self.names = names
        self.mapper = SolutionMapper(names,ranges)
    def evaluation_func_single_core(self,pop,func_args=None):
        if not self._data_loaded:
            self.load_data()
        #wrap function
        if len(func_args) >0:
            portion = int(func_args[0]*pop.shape[0])
        else:
            portion = pop.shape[0]
        def runtrials(pop,index):
            scores = np.zeros(pop.shape[0],)
            for i,sol in enumerate(pop):
                if i > portion:
                    break
                scores[index]=self.runtrial(sol,i)
                sys.stdout.write('trial {} - score {}\n'.format(index,scores[index]))
                sys.stdout.flush()
                index+=1
            return scores
        scores = runtrials(pop,0)
        scores = assign(pop,pop[0:portion],scores)
        print(scores)
        return np.array(scores)

    def evaluation_func(self,pop,func_args=None):
        if len(func_args) > 0:
            #run only a portion of indviduals and assing the rest according to sort-assign-algorithm
            portion = func_args[0]
            cpu_cores = multiprocessing.cpu_count()
            n_trials = int((pop.shape[0]*portion/cpu_cores))
        else:
            cpu_cores = multiprocessing.cpu_count()
            n_trials = int(pop.shape[0]/cpu_cores)

        #divide each candidate sol anmong threads
        if not self._data_loaded:
            self.load_data()
        #implement multiprocessing
        #wrap function
        def runtrials(pop,scores,index):
            for i,sol in enumerate(pop):
                scores[index]=self.runtrial(sol,i)
                index+=1
                sys.stdout.write('trial {} - score {}\n'.format(index,scores[index]))
                sys.stdout.flush()

        start_index = 0
        new_shape = (n_trials,pop.shape[1])
        scores = multiprocessing.Array('f', range(pop.shape[0]))
        processes = []
        for i in range(cpu_cores):
            _end = (start_index+n_trials)
            _pop_p = pop[start_index:_end].reshape(new_shape)
            p = multiprocessing.Process(target=runtrials, args=(_pop_p,scores, start_index,))
            processes.append(p)
            p.start()
            start_index = _end
        for p in processes:
            p.join()
        scores = np.array(scores)
        scores = assign(pop,pop[0:portion],scores)
        return scores

    def load_data(self,val_split=0.1):
        #loads data in train_data and val_data
        '''
        example:

        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        self.num_classes = 10
        self.input_shape = (28, 28, 1)

        #Scale images to the [0, 1] range
        x_train = x_train.astype("float32") / 255
        x_test = x_test.astype("float32") / 255
        # Make sure images have shape (28, 28, 1)
        x_train = np.expand_dims(x_train, -1)
        x_test = np.expand_dims(x_test, -1)
        # convert class vectors to binary class matrices
        y_train = keras.utils.to_categorical(y_train, self.num_classes)
        y_test = keras.utils.to_categorical(y_test, self.num_classes)
        #split data
        x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=val_split, random_state=42)
        #assign
        self.train_data = [x_train,y_train]
        self.val_data = [x_val,y_val]
        '''
        self._data_loaded = True
    def runtrial(self,sol,trial_num):
        #run one trial of sol
        #extract sol into a dict of parameters
        _exits,parameters = self.mapper.mapsol(sol)
        if(_exits):
            return parameters,self.mapper.getsolutionvalue(parameters)
        else:
            return parameters,None

        '''
        model = buildModel(parameters,self.input_shape,self.num_classes)
        #train the model and get metrics
        #exp1 denotes resnet50 with large dataset
        checkpoint_filepath = 'model_checkpoints/checkpoints-minst/chkpt.final-{}'.format(trial_num)
        model_checkpoint_callback = keras.callbacks.ModelCheckpoint(filepath=checkpoint_filepath,save_weights_only=True,monitor='val_accuracy',mode='max', save_best_only=True)
        x_train, y_train = self.train_data[0], self.train_data[1]
        x_val , y_val = self.val_data[0],self.val_data[1]
        history = model.fit(x_train, y_train, batch_size=parameters["batch size"], callbacks =[model_checkpoint_callback],epochs=50, validation_split=0.1)
        #validate
        scores = model.evaluate(x_val,y_val)
        return scores[1]
        '''
