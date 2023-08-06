from typing import List

import tensorflow as tf
from sarus import Client
from sarus.tensorflow.data.dataset import SarusTensorflowDataset


class Model(tf.keras.Model):
    """The sarus.keras.Model class is a wrapper around the
    `tensorflow.keras.Model` class. This class differs from its parent only on
    the `fit` method. The `fit` method accepts a `target_epsilon`.

        - If the specified `target_epsilon` is equal to 0 (default value), then the `Model` class launches a standard keras training on the synthetic data.
        - If the specified `target_epsilon` is strictly greater than 0, then the`Model` class calls the API to launch a remote private training.
    """

    def __init__(self, client=None, *args, **kwargs):
        super(Model, self).__init__(self, *args, **kwargs)
        self._client = client

    def fit(
        self,
        x: SarusTensorflowDataset = None,
        target_epsilon: float = 0.0,
        epochs: int = None,
        client: Client = None,
        l2_norm_clip: float = None,
        noise_multiplier: float = None,
        num_microbatches: int = None,  # default: batch size
        verbose: bool = True,
        **kwargs,
    ):
        """Trains the model for a fixed number of epochs.

        Parameters
        ----------
        x : SarusTensorflowDataset
            Input data.

        epochs : int, default None
            Number of epochs to train the model. An epoch is an
            iteration over the entire data provided.

        target_epsilon : float, default 0.0
            Target epsilon for differentially private
            training. If `target_epsilon` is 0.0, the training is performed
            locally on the synthetic data. If If `target_epsilon` greater than
            0.0, training is performed remotely with DP-SDG.

        l2_norm_clip : float, default None

        noise_multiplier : float, default None

        num_microbatches : int, default None

        Returns
        -------
        History: History, optional


        """
        if target_epsilon < 0:
            raise ValueError(
                f"`target_epsilon` must be positive, got {target_epsilon}"
            )

        if target_epsilon == 0:
            self._fit_local(x, epochs, **kwargs)
        else:
            self._fit_remote(
                x=x,
                target_epsilon=target_epsilon,
                l2_norm_clip=l2_norm_clip,
                noise_multiplier=noise_multiplier,
                num_microbatches=num_microbatches,
                verbose=verbose,
                client=client,
            )

    def _fit_local(self, x: SarusTensorflowDataset, epochs: int, **kwargs):
        return super().fit(x=x._tensorflow(), epochs=epochs, **kwargs)

    def _fit_remote(
        self,
        x: SarusTensorflowDataset,
        target_epsilon: float,
        client: Client,
        l2_norm_clip: float = None,
        noise_multiplier: float = None,
        num_microbatches: int = None,  # default: batch size
        verbose: bool = True,
        wait_for_completion: bool = True,
        **kwargs,
    ):
        if client:
            self._client = client
        if self._client is None:
            raise ValueError(
                f"Sarus client is None: can not fit "
                f"remotely with `target_epsilon`={target_epsilon}."
            )

        batch_size, transforms = Model._refactor_transforms(
            x.dataset.transforms
        )
        transform_def = Model._make_transform_def(transforms)

        task_id = self._client._fit(
            transform_def=transform_def,
            keras_model_def=lambda: self,
            x=x.dataset,
            target_epsilon=target_epsilon,
            batch_size=batch_size,
            non_DP_training=False,
            dp_l2_norm_clip=l2_norm_clip,
            dp_noise_multiplier=noise_multiplier,
            dp_num_microbatches=num_microbatches,  # default: batch size
            seed=None,
            verbose=verbose,
            wait_for_completion=wait_for_completion,
            **kwargs,
        )

        # Set fetched weights to model
        if "error_message" not in client._training_status(id):
            trained_model: tf.keras.Model = self._client._fetch_model(task_id)
            self.set_weights(trained_model.get_weights())

    @staticmethod
    def _refactor_transforms(transforms: List) -> List:
        """Refactor the `transforms`.

        Merge consecutive `batch` and `unbatch` operations for more efficient
        processign on the API side.

        NB: this could be removed once the API does not batch by default.
        """
        if transforms[0][0] == "unbatch" and transforms[1][0] == "batch":
            batch_size = transforms[1][1]["batch_size"]
            transforms = transforms[2:]
        else:
            batch_size = 1
        return batch_size, transforms

    @staticmethod
    def _make_transform_def(transforms):
        def transform_def(ds, features=None):
            """This function should not make use of objects or functions defined
            in the Sarus module to avoid it being listed as a closure by
            cloudpickle."""
            for name, params in transforms:
                if name == "map":
                    ds = ds.map(**params)
                elif name == "unbatch":
                    ds = ds.unbatch(**params)
                elif name == "batch":
                    ds = ds.batch(**params)
                elif name == "filter":
                    ds = ds.filter(**params)
                elif name == "split":
                    size = params["end"] - params["start"]
                    ds = ds.skip(params["start"]).take(size)
            return ds

        return transform_def
