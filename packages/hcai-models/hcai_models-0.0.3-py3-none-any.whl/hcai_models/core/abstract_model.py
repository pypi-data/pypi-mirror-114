import csv
import pathlib
import sys
import ast
from abc import ABC, abstractmethod

import hcai_models.utils.data_utils as data_utils
from hcai_models.core.registered_model import RegisteredModel
from hcai_models.core.ssi_compat import SSIModel, SSIBridgeModel
from hcai_models.core.weights import Weights


class Model(ABC, RegisteredModel):
    """
    Abstract base class for all models.
    Specifies general functionality of the models and ensures compatibility with the interface for external calls.
    """

    def __init__(
        self,
        *args,
        model_name=None,
        input_shape=None,
        output_shape=None,
        include_top=False,
        dropout_rate=0.2,
        weights=None,
        output_activation_function="softmax",
        optimizer="adam",
        loss="categorical_crossentropy",
        pooling="avg",
        **kwargs
    ):

        self._available_weights = self._init_weights()
        self.info = self._info()
        self._model = None

        self.model_name = model_name if model_name else self.__class__.__name__
        self.input_shape = input_shape
        self.include_top = include_top
        self.dropout_rate = dropout_rate
        self.weights = weights
        self.output_shape = (
            output_shape if output_shape else self._determine_output_shape()
        )
        self.output_activation_function = output_activation_function
        self.pooling = pooling
        self.optimizer = optimizer
        self.loss = loss

    # Public
    def build_model(self):
        self._model = self._build_model()

    def is_ssi_model(self):
        return issubclass(self.__class__, SSIModel)

    def is_ssi_bridge_model(self):
        return issubclass(self.__class__, SSIBridgeModel)

    # Private
    def _init_weights(self):
        # Loading entries from the weights.csv file from the directory of the model module
        module_path = sys.modules[self.__module__].__file__
        weights_path = pathlib.Path(module_path).parent / "weights.csv"
        weight_dict = {}
        if not weights_path.exists():
            return weight_dict
        with open(weights_path, encoding="UTF-8") as csv_file:
            csv_dict = csv.DictReader(csv_file, delimiter=";")
            list_of_rows = [dict_row for dict_row in csv_dict]

        for row in list_of_rows:
            if row["ModelClass"].lower() == self.__class__.__name__.lower():
                name = row["Name"]
                shape = ast.literal_eval(row["OutputShape"])
                url = row["Download URL"]
                hash = row["Hash"]
                url_no_top = row["Download URL without top"]
                hash_no_top = row["Hash without top"]
                weight_dict[name] = Weights(
                    download_url=url,
                    hash=hash,
                    output_shape=shape,
                    download_url_no_top=url_no_top,
                    hash_no_top=hash_no_top,
                )

        return weight_dict

    def _get_weight_file(self):
        """
        Retrieves the weights for pretrained models. The weights will be loaded from the url specified in the _available_weights for the respective weights of the model.
        Once downloaded the data will be cached at `~/.hcai_models/weights` unless specified otherwise.
        :return: Path to the downloaded weights
        """
        if not self.weights:
            print("No weigths have been specified")
            return None
        if not self.weights in self._available_weights.keys():
            raise ValueError("Specified weights not found in available weights")
        weights = self._available_weights[self.weights]

        if self.include_top:
            file_name = self.model_name + "_" + self.weights + ".h5"
            hash = weights.hash
            url = weights.download_url
        else:
            file_name = self.model_name + "_" + self.weights + "_notop.h5"
            hash = weights.hash_no_top
            url = weights.download_url_no_top
        return data_utils.get_file(
            fname=file_name, origin=url, file_hash=hash, extract=not url.endswith(".h5")
        )

    def _determine_output_shape(self):
        if not self.weights:
            return None
        else:
            if self.weights not in self._available_weights.keys():
                print(
                    "Cannot automatically infer shape.{} not found in available weights.".format(
                        self.weights
                    )
                )
                return None
            else:
                return self._available_weights[self.weights].output_shape

    # Public Abstract
    @abstractmethod
    def preprocess_input(self, ds):
        """
        Preprocesses the input data. Only use for static preprocessing that should be replicated once the model is fully trained (e.g input normalization)
        :return:
        """
        raise NotImplemented()

    @abstractmethod
    def compile(self, optimizer, loss, metrics):
        """
        Fixes the models training parameter: loss, metrics and optimizer
        :return:
        """
        raise NotImplemented()

    @abstractmethod
    def load_weights(self, filepath):
        """
        Loads weights.csv the weights.csv of a model
        :return:
        """
        raise NotImplemented()

    @abstractmethod
    def predict(self, sample):
        """
        Predict the given sample
        Args:
            sample:
        """
        raise NotImplementedError()

    @abstractmethod
    def fit(
        self,
        *args,
        x=None,
        y=None,
        batch_size=None,
        epochs=1,
        validation_split=0.0,
        validation_data=None,
        **kwargs
    ):
        """
        Fits the model on the provided data. The parameter
        :return:
        """
        raise NotImplemented()

    # Private Abstract Methods
    @abstractmethod
    def _build_model(self):
        """
        Builds the model as specified by the set class parameters and set self.model
        :return:
        """
        raise NotImplemented()

    @abstractmethod
    def _info(self):
        """
        Returns additional information for the model
        :return:
        """
        raise NotImplemented()
