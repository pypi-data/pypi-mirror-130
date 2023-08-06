import numpy as np
from tensorflow import keras
from sklearn.model_selection import train_test_split
from GSKhopt.SolutionMapper import SolutionMapper
from GSKhopt.Models import buildModel
from GSKhopt.Objectives.eval import EvaluationFunction
class KerasCNN(EvaluationFunction):
    def __init__(self):
        EvaluationFunction.__init__(self)

    def load_data(self,val_split=0.1):
        EvaluationFunction.load_data(self)

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


    def runtrial(self,sol,trial_num):
        #run one trial of sol
        #extract sol into a dict of parameters
        parameters,value = EvaluationFunction.runtrial(self,sol,trial_num)
        if value == None:
            #model = buildModel(parameters,self.input_shape,self.num_classes)
            #train the model and get metrics
            #exp1 denotes resnet50 with large dataset
            checkpoint_filepath = 'model_checkpoints/checkpoints-minst/chkpt.final-{}'.format(trial_num)
            model_checkpoint_callback = keras.callbacks.ModelCheckpoint(filepath=checkpoint_filepath,save_weights_only=True,monitor='val_accuracy',mode='max', save_best_only=True)
            early_stop = keras.callbacks.EarlyStopping(patience=2)
            x_train, y_train = self.train_data[0], self.train_data[1]
            x_val , y_val = self.val_data[0],self.val_data[1]
            #history = model.fit(x_train, y_train, batch_size=parameters["batch_size"],epochs=1,steps_per_epoch=1,verbose=False)
            #validate
            #scores = model.evaluate(x_val,y_val,verbose=False)
            return np.random.uniform()
        else:
            return value
