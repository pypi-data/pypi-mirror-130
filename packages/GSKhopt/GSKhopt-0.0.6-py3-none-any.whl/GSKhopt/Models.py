import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras import Model

def buildModel(parameters,input_shape,num_classes):
    inputs = keras.Input(shape=input_shape)
    #first layer should be cnn
    
    blocks = parameters["blocks"]
    cnns = [parameters["0_cnns"],parameters["1_cnns"],parameters["2_cnns"]]
    f = [parameters["0_filters"],parameters["1_filters"]]
    k = [parameters["0_kernels"],parameters["1_kernels"]]
    fcs = [parameters["0_fcs_size"],parameters["1_fcs_size"]]
    #first block connected to input
    last_layer = layers.Conv2D(f[0], kernel_size=(k[0], k[0]),activation="relu")(inputs)
    for c in range(1,cnns[0]):
        last_layer = layers.Conv2D(f[c], kernel_size=(k[c], k[c]), padding ="same",activation="relu")(last_layer)
    last_layer = layers.MaxPooling2D(pool_size=(2, 2))(last_layer)
    #we only generate models according to number of blocks and number of cnns and not to indvidual
    for i in range(1,blocks):
        for j in range(0,cnns[i]):
            last_layer = layers.Conv2D(f[j], kernel_size=(k[j], k[j]), padding ="same",activation="relu")(last_layer)
        last_layer = layers.MaxPooling2D(pool_size=(2, 2))(last_layer)
    flatten = layers.Flatten()(last_layer)
    dropout = layers.Dropout(parameters["dropout"])(flatten)
    hidden = layers.Dense(fcs[0], activation="relu")(dropout)
    for i in range(1,parameters["n_fcs"]):

        #fc layer
        hidden = layers.Dense(fcs[i], activation="relu")(hidden)

    output = layers.Dense(num_classes, activation="softmax")(hidden)
    model = Model(inputs=inputs,outputs=output)
    #model.summary()
    model.compile(loss="categorical_crossentropy", optimizer=keras.optimizers.Adam(learning_rate=parameters["lr"]), metrics=["accuracy"])
    return model
