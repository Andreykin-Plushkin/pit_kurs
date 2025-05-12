import numpy as np 

from keras import layers
from keras import backend
from keras import activations

from keras.datasets import mnist

from keras.models import Sequential
from keras.optimizers import Adam ,RMSprop
from keras.utils import to_categorical, plot_model
from keras.layers import Dense , Activation, Dropout

import matplotlib.pyplot as plt

class Network:


    def __init__(self):

        backend.clear_session(free_memory=True)

        self.input_size = 28 * 28

        self.x_train = []
        self.y_train = []

        self.x_test = []
        self.y_test = []

        self.hidden_units = 256
        self.num_labels = 10

        self.model = Sequential(
            [
                layers.Dense(self.hidden_units, input_dim=self.input_size, activation="relu", name="layer_1"),
                layers.Dense(self.hidden_units, activation="relu", name="layer_2"),
                layers.Dense(self.num_labels, activation="softmax", name="layer_3")
            ]
        )

        self.history = None

        self.model.summary()

        self.model.compile(loss='categorical_crossentropy', 
                      optimizer='adam',
                      metrics=['accuracy'])

        plot_model(self.model, to_file="static/images/model.png", show_shapes=True)

        self.load_dataset()



    def load_dataset(self):
        (self.x_train, self.y_train), (self.x_test, self.y_test) = mnist.load_data()

        self.unique_train, self.counts_train = np.unique(self.y_train, return_counts=True)
        self.unique_test, self.counts_test = np.unique(self.y_test, return_counts=True)

        self.x_train = np.reshape(self.x_train, [-1, self.input_size]).astype('float32') / 255
        self.x_test = np.reshape(self.x_test, [-1, self.input_size]).astype('float32') / 255

        self.y_train = to_categorical(self.y_train)
        self.y_test = to_categorical(self.y_test)


    def get_info_about_dataset(self):
        return dict(zip(self.unique_train, self.counts_train)), dict(zip(self.unique_test, self.counts_test))


    def learn(self, epochs, batch_size):
        self.history = self.model.fit(self.x_train, self.y_train, epochs=epochs, batch_size=batch_size)
        self.make_graph()


    def predict(self, data):
        prediction = self.model(data)
        answer = np.argmax(prediction)
        return str(answer)


    def make_graph(self):
        plt.plot(self.history.history['accuracy'])
        plt.title('точность классификации')
        plt.ylabel('точность')
        plt.xlabel('эпоха')
        plt.legend(['тестовые данные'], loc='upper left')
        plt.savefig('static/images/learning_graph.png')

        plt.clf()
        plt.cla()
        plt.close()
