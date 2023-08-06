"""Class to forward the abstract functions required by the abstract_model class to the keras api.
Keras models can inherit the methods implemented by this class to avoid duplicating boilerplate code.
"""

from hcai_models.core.abstract_model import Model


class KerasModel(Model):
    def __init__(self, *args, input_tensor=None, **kwargs):
        self.input_tensor = input_tensor
        super().__init__(*args, **kwargs)

    def load_weights(self, *args, filepath=None, **kwargs):

        filepath = self._get_weight_file()
        self._model.load_weights(*args, filepath=filepath, **kwargs)

    # Pass-through functions to Keras Model API
    def compile(self, *args, **kwargs):
        return self._model.compile(*args, **kwargs)

    def fit(self, *args, **kwargs):
        return self._model.fit(*args, **kwargs)

    def predict(self, *args, **kwargs):
        return self._model.predict(*args, **kwargs)
