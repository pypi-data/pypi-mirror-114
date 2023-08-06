"""Class to forward the abstract functions required by the abstract_model class to the keras api.
Keras models can inherit the methods implemented by this class to avoid duplicating boilerplate code.
"""

import tensorflow.keras as keras
from hcai_models.core.abstract_model import Model
from tensorflow.python.keras.layers import VersionAwareLayers

layers = VersionAwareLayers()


class KerasModel(Model):
    def __init__(self, *args, input_tensor=None, **kwargs):
        self.input_tensor = input_tensor
        super().__init__(*args, **kwargs)

    def load_weights(self, *args, filepath=None, **kwargs):
        if not filepath:
            filepath = self._get_weight_file()
        self._model.load_weights(*args, filepath=filepath, **kwargs)

    def _add_top_layers(self, model=None, model_heads=None, outputs_as_list=False):

        if not model:
            print("Error adding top layer. Model not provided.")

        x = model.output
        outputs = {}

        if model_heads is None:
            if self.dropout_rate > 0:
                x = layers.Dropout(self.dropout_rate, name="top_dropout")(x)

            if not len(self.output_shape) == 1:
                raise ValueError("Outputshape should have exactly one dimension.")
            x = layers.Dense(
                self.output_shape[0],
                activation=self.output_activation_function,
                name="predictions",
            )(x)

            outputs["prediction"] = x
        else:
            for name, layer_list in model_heads.items():
                # Connect the first layer of the new head
                h = layer_list[0](x)
                for layer in layer_list[1:]:
                    h = layer(h)
                outputs[name] = h

        if not outputs_as_list:
            outputs = list(outputs.values())

        return keras.Model(inputs=model.inputs, outputs=outputs, name=self.name)

    # Pass-through functions to Keras Model API
    def compile(self, *args, **kwargs):
        return self._model.compile(*args, **kwargs)

    def fit(self, *args, **kwargs):
        return self._model.fit(*args, **kwargs)

    def predict(self, *args, **kwargs):
        return self._model.predict(*args, **kwargs)
