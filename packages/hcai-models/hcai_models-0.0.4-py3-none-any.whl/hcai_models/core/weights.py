import numpy as np


class Weights:

    # Overwrite to include a description of the weights.csv in the documentation
    _DESCRIPTION = ""

    def __init__(
        self,
        download_url,
        hash,
        output_shape=None,
        download_url_no_top=None,
        hash_no_top=None,
    ):
        """
        Initialize the weigth datastructure
        :param download_url: The url from where to download the weights.csv
        :param hash: The sha256 hash of the weight file
        :param output_shape: Shape of the outputs of the network. Only necessary if the model is build with the original top
        :param download_url_no_top: Download path for the weightfile with no model top
        :param hash_no_top: The sha256 hash of the weight file with no model top
        """
        self.download_url = download_url
        self.hash = hash
        self.download_url_no_top = download_url_no_top
        self.hash_no_top = hash_no_top
        self.output_shape = (
            (output_shape,) if np.isscalar(output_shape) else output_shape
        )
