import tensorflow as tf
from tensorflow.python.keras import layers
from tensorflow.python.keras.optimizers import adam_v2
from tensorflow.python.keras import losses
from typing import List
import os


class SimpleModel(tf.keras.Model):
    """
    Model class. Quite simple. Complete this docstring is a #TODO
    """

    def __init__(self, hidden_sizes: List, target_size: int) -> None:
        """
        Initialize a QNET with N hidden Dense layers, where N is the length of the 
        hidden_sizes list. Each layer i has n nodes, being n the value of ith
        element of the hidden_sizes list. These layers are activated with a relu
        function. The first layer is set to accept inputs of shape (1,input_dim).

        Finally a Dense layer of target_size nodes without activation is used as
        an output layer.
        """
        super().__init__()
        self.hidden_layers = []
        for count, layer_size in enumerate(hidden_sizes):
            if count == 0:
                self.hidden_layers.append(layers.Dense(
                    layer_size, activation='relu', name=f'hidden{count}'))
            else:
                self.hidden_layers.append(layers.Dense(
                    layer_size, activation='relu', name=f'hidden{count}'))

        self.output_layer = layers.Dense(
            target_size, activation=None, name='output')

        # TODO: Maybe adding Dropouts to improve the model

    def call(self, input):
        """
        Will be called when predict and train.
        """
        for layer in self.hidden_layers:
            x = layer(input)
            input = x

        return self.output_layer(x)

    def save(self, file_name='model.pth'):
        """
        Save the entire model.
        """
        folder_path = './model'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, file_name)
        self.save(file_name=file_path)


class Trainer:
    """
    Trainer class. Includes the training algorithm as well as
    the optimizer.
    """

    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = adam_v2(learning_rate=lr)
        self.loss = losses.MeanSquaredError()

    def train(self, states, actions, rewards, new_states, game_overs):
        state = tf.Tensor(states, dtype=tf.float64)
        action = tf.Tensor(actions, dtype=tf.float64)
        reward = tf.Tensor(rewards, dtype=tf.float64)
        new_state = tf.Tensor(new_states, dtype=tf.float64)
        game_over = tf.Tensor(game_overs, dtype=tf.float64)

        # ensure we have the correct dimensionality of the Tensors even when they
        # are 1D
        if len(state.shape) == 1:
            state = tf.expand_dims(state, 0)
            action = tf.expand_dims(action, 0)
            reward = tf.expand_dims(reward, 0)
            new_state = tf.expand_dims(new_state, 0)
            game_over = tf.expand_dims(game_over, 0)
