import tensorflow as tf
from tensorflow.python.keras import layers
from tensorflow.python.keras.optimizers import adam_v2
from tensorflow.python.keras import losses
import os


class SimpleModel(tf.keras.Model):
    """
    Model class. Quite simple. Complete this docstring is a #TODO
    """

    def __init__(self, input_size, hidden_size, target_size):
        super().__init__()
        """
        NN with 2 hidden layers of size 'hiden_sieze' and an output layer with
        size 'target_size' activated with a softmax function since we aim to 
        predict one of 3 possible outputs only (classification).
        """
        self.dense1 = layers.Dense(
            hidden_size, activation='relu', name='hidden1')
        self.dense2 = layers.Dense(
            hidden_size, activation='relu', name='hidden2')
        self.dense3 = layers.Dense(
            target_size, activation='softmax', name='output')  # output layer

        # TODO: Play with the idea of Dropouts and tune the model

    def call(self, input):
        """
        Will be called when predict and train.
        """
        x = self.dense1(input)
        x = self.dense2(x)
        return self.dense3(x)

    def save(self, file_name='model.pth'):
        """
        Save the entire model.
        """
        folder_path = './model'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_name = os.path.join(folder_path, file_name)
        self.save(file_name=file_name)


class Trainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = adam_v2(learning_rate=lr)
        self.loss = losses.MeanSquaredError()
