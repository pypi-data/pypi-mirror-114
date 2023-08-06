import tensorflow as tf
import tensorflow.keras as keras
from hcai_models.core.abstract_image_model import ImageModel
from hcai_models.core.keras_model import KerasModel
from tensorflow.python.keras.layers import VersionAwareLayers

layers = VersionAwareLayers()

_DESCRIPTION = """
Convolutional networks are at the core of most state-of-the-art computer vision solutions for a wide variety of tasks. 
Since 2014 very deep convolutional networks started to become mainstream, yielding substantial gains in various benchmarks. 
Although increased model size and computational cost tend to translate to immediate quality gains for most tasks (as long as enough labeled data is provided for training), 
computational efficiency and low parameter count are still enabling factors for various use cases such as mobile vision and big-data scenarios. 
Here we explore ways to scale up networks in ways that aim at utilizing the added computation as efficiently as possible by suitably factorized convolutions and aggressive regularization. 
We benchmark our methods on the ILSVRC 2012 classification challenge validation set demonstrate substantial gains over the state of the art: 
21.2% top-1 and 5.6% top-5 error for single frame evaluation using a network with a computational cost of 5 billion multiply-adds per inference and with using less than 25 million parameters.
With an ensemble of 4 models and multi-crop evaluation, we report 3.5% top-5 error on the validation set (3.6% error on the tests set) and 17.3% top-1 error on the validation set.
"""

_CITATION = """
@inproceedings{szegedy2016rethinking,
  title={Rethinking the inception architecture for computer vision},
  author={Szegedy, Christian and Vanhoucke, Vincent and Ioffe, Sergey and Shlens, Jon and Wojna, Zbigniew},
  booktitle={Proceedings of the IEEE conference on computer vision and pattern recognition},
  pages={2818--2826},
  year={2016}
}
"""


class InceptionV3(ImageModel, KerasModel):
    def __init__(self, *args, **kwargs):
        # Overwriting default parameters
        kwargs.setdefault("input_height", 299)
        kwargs.setdefault("input_width", 299)
        kwargs.setdefault("input_channels", 3)

        # Init parents
        super().__init__(
            *args,
            keras_build_func=keras.applications.inception_v3.InceptionV3,
            **kwargs
        )

    def _build_model(self):
        # Adding preprocessing layer
        inputs = tf.keras.Input((None, None, self.n_channels))
        x = layers.Resizing(self.in_height, self.in_width)(inputs)
        x = layers.Rescaling(1.0 / 127.0, offset=-1)(x)

        # Getting base model
        x = keras.applications.InceptionV3(input_tensor=x, include_top=False, weights=None).output

        # Apply pooling
        if self.pooling == "avg":
            x = layers.GlobalAveragePooling2D()(x)
        elif self.pooling == "max":
            x = layers.GlobalMaxPooling2D()(x)

        # Adding top
        if self.include_top:
            if self.dropout_rate > 0:
                x = layers.Dropout(self.dropout_rate, name="top_dropout")(x)

            if not len(self.output_shape) == 1:
                raise ValueError('Got output shape with multiple dimensions, but only classification / regression tops are supported for InceptionV3')
            x = layers.Dense(
                self.output_shape[0],
                activation=self.output_activation_function,
                name="predictions",
            )(x)

        return keras.Model(inputs=inputs, outputs=x, name=self.name)

    def _info(self):
        return ""

    def preprocess_input(self, ds):
        """
        All preprocessing is done in the layers of the model itself
        :param ds:
        :return:
        """
        # Resizing the input data
        # size = (self.input_shape[0], self.input_shape[1])
        # ds = ds.map(lambda image, label: (tf.image.resize(image, size), label))

        from tensorflow.python.keras.applications.inception_v3 import preprocess_input

        return ds
