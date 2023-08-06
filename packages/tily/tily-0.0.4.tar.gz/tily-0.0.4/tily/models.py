"""Contains tensorflow code for prediction models usage."""
import sys

from pathlib import Path

import tensorflow as tf
import tensorflow.contrib.slim as slim    # pylint: disable=E0401,W0611,R0402

from absl import logging


class Models:
    """Handles 'vgg-mix' and 'incep-mix' models predictions.

       Attributes:
          model_type: str, the type of graph to be used.
          models_root_path: str, path to model files.
    """

    def __init__(self, model_type: str, models_root_path: str):
        """Initializes session state."""
        model_path = Path(models_root_path).joinpath(model_type)
        model_graph = model_path.joinpath(model_type + ".ckpt.meta")
        self.session_config = tf.ConfigProto()
        self.session_config.gpu_options.allow_growth = True
        self.session = tf.Session(config=self.session_config)
        try:
            loader = tf.train.import_meta_graph(str(model_graph))
            loader.restore(self.session,
                           tf.train.latest_checkpoint(str(model_path)))
        except ValueError as err:
            logging.error("Missing models files - %s", err)
            sys.exit(1)
        self.image_tensor = self.session.graph.get_tensor_by_name(
            "Placeholder:0")
        self.isTest = self.session.graph.get_tensor_by_name("Placeholder_2:0")    # pylint: disable=C0103
        if model_type == "vgg-mix":
            self.scores = self.session.graph.get_tensor_by_name(
                "vgg_16/fc8/squeezed:0")
        elif model_type == "incep-mix":
            self.scores = self.session.graph.get_tensor_by_name(
                "InceptionV4/Logits/Logits/BiasAdd:0")
        else:
            logging.error("Unknown model type - %s", model_type)
            sys.exit(1)
        self.image_size = self.image_tensor.get_shape().as_list()[1:3]

    def get_size(self):
        """Finds out model's input tensor size.

        Returns:
            image_size: tuple, width and heigth of imput array.
        """
        return self.image_size

    def predict(self, inputs):
        """Runs prediction on input array.

        Returns:
            prediction: np.array, prediction results.
        """
        with self.session.as_default():
            prediction = self.session.run(self.scores, {
                self.image_tensor: inputs,
                self.isTest: True
            })
            return prediction
