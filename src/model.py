import tensorflow as tf
import numpy as np
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

    def __init__(self, model: SimpleModel, lr: float, gamma: float) -> None:
        self.lr = lr  # learning rate
        self.gamma = gamma  # discount rate
        self.model = model
        self.optimizer = adam_v2.Adam(learning_rate=lr)
        self.loss_object = losses.MeanSquaredError()

    def train(self, states, actions, rewards, new_states, game_overs):
        """
        Custom training algorithm to apply a single train step.
        """
        state = tf.convert_to_tensor(states, dtype=tf.float64)
        action = tf.convert_to_tensor(actions, dtype=tf.float64)
        reward = tf.convert_to_tensor(rewards, dtype=tf.float64)
        new_state = tf.convert_to_tensor(new_states, dtype=tf.float64)
        game_over = tf.convert_to_tensor(game_overs, dtype=tf.float64)

        # ensure we have the correct dimensionality of the Tensors even when they
        # are 1D
        if len(state.shape) == 1:
            state = tf.expand_dims(state, 0)
            action = tf.expand_dims(action, 0)
            reward = tf.expand_dims(reward, 0)
            new_state = tf.expand_dims(new_state, 0)
            # game_over = tf.expand_dims(game_over, 0)
            game_over = (game_overs, )

        # implementation of Bellman's equation
        with tf.GradientTape() as tape:
            # get Q for current state
            predictions = self.model(state)  # 3 values

            target = np.copy(predictions)
            for i in range(state.shape[0]):
                if not game_over[i]:
                    Q_new = reward[i] + self.gamma * \
                        tf.math.reduce_max(
                            self.model(tf.expand_dims(new_state[i], 0))).numpy()
                else:
                    Q_new = reward[i]

                target[i][int(action[i])] = Q_new

        # with tf.GradientTape() as tape:
            # calculate the loss function for the step
            l = self.loss_object(y_true=target, y_pred=predictions)
            grads = tape.gradient(l, self.model.trainable_variables)

        self.optimizer.apply_gradients(
            zip(grads, self.model.trainable_variables))
