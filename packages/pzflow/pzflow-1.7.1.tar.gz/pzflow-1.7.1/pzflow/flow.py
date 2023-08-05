import itertools
from typing import Any, Callable, Sequence, Tuple

import dill as pickle
import jax.numpy as np
import numpy as onp
import pandas as pd
from jax import grad, jit, ops, random, vmap
from jax.experimental.optimizers import Optimizer, adam

from pzflow import distributions
from pzflow.bijectors import Bijector_Info, InitFunction, Pytree
from pzflow.utils import build_bijector_from_info


class Flow:
    """A normalizing flow that models tabular data.

    Attributes
    ----------
    data_columns : tuple
        List of DataFrame columns that the flow expects/produces.
    conditional_columns : tuple
        List of DataFrame columns on which the flow is conditioned.
    info : Any
        Object containing any kind of info included with the flow.
        Often describes the data the flow is trained on.
    latent
        The latent distribution of the normalizing flow.
        Has it's own sample and log_prob methods.
    """

    def __init__(
        self,
        data_columns: Sequence[str] = None,
        bijector: Tuple[InitFunction, Bijector_Info] = None,
        conditional_columns: Sequence[str] = None,
        latent=None,
        seed: int = 0,
        info: Any = None,
        file: str = None,
        _dictionary: dict = None,
    ):
        """Instantiate a normalizing flow.

        Note that while all of the init parameters are technically optional,
        you must provide either data_columns and bijector OR file.
        In addition, if a file is provided, all other parameters must be None.

        Parameters
        ----------
        data_columns : Sequence[str], optional
            Tuple, list, or other container of column names.
            These are the columns the flow expects/produces in DataFrames.
        bijector : Bijector Call, optional
            A Bijector call that consists of the bijector InitFunction that
            initializes the bijector and the tuple of Bijector Info.
            Can be the output of any Bijector, e.g. Reverse(), Chain(...), etc.
        conditional_columns : Sequence[str], optional
            Names of columns on which to condition the normalizing flow.
        latent : distribution, optional
            The latent distribution for the normalizing flow. Can be any of
            the distributions from pzflow.distributions. If not provided,
            a normal distribution is used with the number of dimensions
            inferred.
        seed : int, default=0
            The random seed for initial parameters
        info : Any, optional
            An object to attach to the info attribute.
        file : str, optional
            Path to file from which to load a pretrained flow.
            If a file is provided, all other parameters must be None.
        """

        # validate parameters
        if (
            data_columns is None
            and bijector is None
            and file is None
            and _dictionary is None
        ):
            raise ValueError("You must provide data_columns and bijector OR file.")
        if data_columns is not None and bijector is None:
            raise ValueError("Please also provide a bijector.")
        if data_columns is None and bijector is not None:
            raise ValueError("Please also provide data_columns.")
        if any(
            (
                data_columns is not None,
                bijector is not None,
                conditional_columns is not None,
                latent is not None,
                info is not None,
            )
        ):
            if file is not None:
                raise ValueError(
                    "If providing a file, please do not provide any other parameters."
                )
            if _dictionary is not None:
                raise ValueError(
                    "If providing a dictionary, please do not provide any other parameters."
                )
        if file is not None and _dictionary is not None:
            raise ValueError("Only provide file or _dictionary, not both.")

        # if file or dictionary is provided, load everything from it
        if file is not None or _dictionary is not None:

            save_dict = self._save_dict()
            if file is not None:
                with open(file, "rb") as handle:
                    save_dict.update(pickle.load(handle))
            else:
                save_dict.update(_dictionary)

            if save_dict["class"] != self.__class__.__name__:
                raise TypeError(
                    f"This save file isn't a {self.__class__.__name__}."
                    + f"It is a {save_dict['class']}"
                )

            # load columns and dimensions
            self.data_columns = save_dict["data_columns"]
            self.conditional_columns = save_dict["conditional_columns"]
            self._input_dim = len(self.data_columns)
            self.info = save_dict["info"]

            # load the latent distribution
            self._latent_info = save_dict["latent_info"]
            self.latent = getattr(distributions, self._latent_info[0])(
                *self._latent_info[1]
            )

            # load the bijector
            self._bijector_info = save_dict["bijector_info"]
            init_fun, _ = build_bijector_from_info(self._bijector_info)
            _, self._forward, self._inverse = init_fun(
                random.PRNGKey(0), self._input_dim
            )
            self._params = save_dict["params"]

            # load the conditional means and stds
            self._condition_means = save_dict["condition_means"]
            self._condition_stds = save_dict["condition_stds"]

        # if no file is provided, use provided parameters
        else:
            self.data_columns = tuple(data_columns)
            self._input_dim = len(self.data_columns)
            self.info = info

            if conditional_columns is None:
                self.conditional_columns = None
                self._condition_means = None
                self._condition_stds = None
            else:
                self.conditional_columns = tuple(conditional_columns)
                self._condition_means = np.zeros(len(self.conditional_columns))
                self._condition_stds = np.ones(len(self.conditional_columns))

            # set up the latent distribution
            if latent is None:
                self.latent = distributions.Normal(self._input_dim)
            else:
                self.latent = latent
            self._latent_info = self.latent.info

            # set up the bijector with random params
            init_fun, self._bijector_info = bijector
            bijector_params, self._forward, self._inverse = init_fun(
                random.PRNGKey(seed), self._input_dim
            )
            self._params = (self.latent._params, bijector_params)

    def _get_conditions(self, inputs: pd.DataFrame) -> np.ndarray:
        """Return an array of the bijector conditions."""

        # if this isn't a conditional flow, just return empty conditions
        if self.conditional_columns is None:
            conditions = np.zeros((inputs.shape[0], 1))
        # if this a conditional flow, return an array of the conditions
        else:
            columns = list(self.conditional_columns)
            conditions = np.array(inputs[columns].values)
            conditions = (conditions - self._condition_means) / self._condition_stds
        return conditions

    def _get_samples(
        self,
        rng,
        inputs: pd.DataFrame,
        nsamples: int,
        type: str = "data",
        skip: str = None,
    ) -> np.ndarray:
        """Draw Gaussian samples for each row of inputs. """

        X = inputs.copy()

        # get list of columns
        if type == "data":
            columns = list(self.data_columns)
        elif type == "conditions":
            if self.conditional_columns is None:
                return np.zeros((nsamples * X.shape[0], 1))
            else:
                columns = list(self.conditional_columns)
        else:
            raise ValueError("type must be `data` or `conditions`.")

        # make sure all relevant variables have error columns
        for col in columns:
            # if errors not provided for the column, fill in zeros
            if f"{col}_err" not in inputs.columns and col != skip:
                X[f"{col}_err"] = np.zeros(X.shape[0])

        # pull out relevant columns
        if skip is not None:
            columns.remove(skip)
        err_columns = [col + "_err" for col in columns]
        X, Xerr = np.array(X[columns].values), np.array(X[err_columns].values)

        # lower bound on Xerr to avoid singular matrix
        Xerr = np.clip(Xerr, 1e-8, None)
        # generate samples
        Xsamples = random.multivariate_normal(
            rng, X, vmap(np.diag)(Xerr ** 2), shape=(nsamples, X.shape[0])
        )
        Xsamples = Xsamples.reshape(-1, X.shape[1], order="F")

        # if these are samples of conditions, standard scale them!
        if type == "conditions":
            Xsamples = (Xsamples - self._condition_means) / self._condition_stds

        return Xsamples

    def _log_prob(
        self, params: Pytree, inputs: np.ndarray, conditions: np.ndarray
    ) -> np.ndarray:
        """Log prob for arrays."""
        # calculate log_prob
        u, log_det = self._forward(params[1], inputs, conditions=conditions)
        log_prob = self.latent.log_prob(params[0], u) + log_det
        # set NaN's to negative infinity (i.e. zero probability)
        log_prob = np.nan_to_num(log_prob, nan=np.NINF)
        return log_prob

    def _save_dict(self):
        """Returns the dictionary of all flow params to be saved."""
        save_dict = {"class": "Flow"}
        keys = [
            "data_columns",
            "conditional_columns",
            "condition_means",
            "condition_stds",
            "info",
            "latent_info",
            "bijector_info",
            "params",
        ]
        for key in keys:
            try:
                save_dict[key] = getattr(self, key)
            except AttributeError:
                try:
                    save_dict[key] = getattr(self, "_" + key)
                except AttributeError:
                    save_dict[key] = None

        return save_dict

    def log_prob(
        self, inputs: pd.DataFrame, nsamples: int = None, seed: int = None
    ) -> np.ndarray:
        """Calculates log probability density of inputs.

        Parameters
        ----------
        inputs : pd.DataFrame
            Input data for which log probability density is calculated.
            Every column in self.data_columns must be present.
            If self.conditional_columns is not None, those must be present
            as well. If other columns are present, they are ignored.
        nsamples : int, default=None
            Number of samples to average over for the log_prob calculation.
            If provided, then Gaussian errors are assumed, and method will
            look for error columns in `inputs`. Error columns must end in
            `_err`. E.g. the error column for the variable `u` must be `u_err`.
            Zero error assumed for any missing error columns.
        seed : int, default=None
            Random seed for drawing the samples with Gaussian errors.

        Returns
        -------
        np.ndarray
            Device array of shape (inputs.shape[0],).
        """

        if nsamples is None:
            # convert data to an array with columns ordered
            columns = list(self.data_columns)
            X = np.array(inputs[columns].values)
            # get conditions
            conditions = self._get_conditions(inputs)
            # calculate log_prob
            return self._log_prob(self._params, X, conditions)

        else:
            # validate nsamples
            assert isinstance(nsamples, int), "nsamples must be a positive integer."
            assert nsamples > 0, "nsamples must be a positive integer."
            # get Gaussian samples
            seed = onp.random.randint(1e18) if seed is None else seed
            rng = random.PRNGKey(seed)
            X = self._get_samples(rng, inputs, nsamples, type="data")
            C = self._get_samples(rng, inputs, nsamples, type="conditions")
            # calculate log_probs
            log_probs = self._log_prob(self._params, X, C)
            probs = np.exp(log_probs.reshape(-1, nsamples))
            return np.log(probs.mean(axis=1))

    def posterior(
        self,
        inputs: pd.DataFrame,
        column: str,
        grid: np.ndarray,
        normalize: bool = True,
        nsamples: int = None,
        seed: int = None,
        batch_size: int = None,
    ) -> np.ndarray:
        """Calculates posterior distributions for the provided column.

        Calculates the conditional posterior distribution, assuming the
        data values in the other columns of the DataFrame.

        Parameters
        ----------
        inputs : pd.DataFrame
            Data on which the posterior distributions are conditioned.
            Must have columns matching self.data_columns, *except*
            for the column specified for the posterior (see below).
        column : str
            Name of the column for which the posterior distribution
            is calculated. Must be one of the columns in self.data_columns.
            However, whether or not this column is one of the columns in
            `inputs` is irrelevant.
        grid : np.ndarray
            Grid on which to calculate the posterior.
        normalize : boolean, default=True
            Whether to normalize the posterior so that it integrates to 1.
        nsamples : int, default=None
            Number of samples to average over for the posterior calculation.
            If provided, then Gaussian errors are assumed, and method will
            look for error columns in `inputs`. Error columns must end in
            `_err`. E.g. the error column for the variable `u` must be `u_err`.
            Zero error assumed for any missing error columns.
        seed : int, default=None
            Random seed for drawing the samples with Gaussian errors.
        batch_size : int, default=None
            Size of batches in which to calculate posteriors. If None, all
            posteriors are calculated simultaneously. Simultaneous calculation
            is faster, but memory intensive for large data sets.

        Returns
        -------
        np.ndarray
            Device array of shape (inputs.shape[0], grid.size).
        """

        # get the index of the provided column, and remove it from the list
        columns = list(self.data_columns)
        idx = columns.index(column)
        columns.remove(column)

        nrows = inputs.shape[0]
        batch_size = nrows if batch_size is None else batch_size

        if nsamples is not None:
            # validate nsamples
            assert isinstance(nsamples, int), "nsamples must be a positive integer."
            assert nsamples > 0, "nsamples must be a positive integer."
            # set the seed
            seed = onp.random.randint(1e18) if seed is None else seed
            rng = random.PRNGKey(seed)

        # empty array to hold pdfs
        pdfs = np.zeros((nrows, len(grid)))

        # loop through batches
        for batch_idx in range(0, nrows, batch_size):

            # get the data batch
            # and, if this is a conditional flow, the correpsonding conditions
            batch = inputs.iloc[batch_idx : batch_idx + batch_size]

            # if not drawing samples, just grab batch and conditions
            if nsamples is None:
                conditions = self._get_conditions(batch)
                batch = np.array(batch[columns].values)
            # if only drawing condition samples...
            elif len(self.data_columns) == 1:
                conditions = self._get_samples(rng, batch, nsamples, type="conditions")
                batch = np.repeat(batch[columns].values, nsamples, axis=0)
            # if drawing data and condition samples...
            else:
                conditions = self._get_samples(rng, batch, nsamples, type="conditions")
                batch = self._get_samples(
                    rng, batch, nsamples, skip=column, type="data"
                )

            # make a new copy of each row for each value of the column
            # for which we are calculating the posterior
            batch = np.hstack(
                (
                    np.repeat(
                        batch[:, :idx],
                        len(grid),
                        axis=0,
                    ),
                    np.tile(grid, len(batch))[:, None],
                    np.repeat(
                        batch[:, idx:],
                        len(grid),
                        axis=0,
                    ),
                )
            )

            # make similar copies of the conditions
            conditions = np.repeat(conditions, len(grid), axis=0)

            # calculate probability densities
            log_prob = self._log_prob(self._params, batch, conditions).reshape(
                (-1, len(grid))
            )
            prob = np.exp(log_prob)
            # if we were Gaussian sampling, average over the samples
            if nsamples is not None:
                prob = prob.reshape(-1, nsamples, len(grid))
                prob = prob.mean(axis=1)
            # add the pdfs to the bigger list
            pdfs = ops.index_update(
                pdfs,
                ops.index[batch_idx : batch_idx + batch_size, :],
                prob,
                indices_are_sorted=True,
                unique_indices=True,
            )

        if normalize:
            # normalize so they integrate to one
            pdfs = pdfs / np.trapz(y=pdfs, x=grid).reshape(-1, 1)
        # set NaN's equal to zero probability
        pdfs = np.nan_to_num(pdfs, nan=0.0)
        return pdfs

    def sample(
        self,
        nsamples: int = 1,
        conditions: pd.DataFrame = None,
        save_conditions: bool = True,
        seed: int = None,
    ) -> pd.DataFrame:
        """Returns samples from the normalizing flow.

        Parameters
        ----------
        nsamples : int, default=1
            The number of samples to be returned.
        conditions : pd.DataFrame, optional
            If this is a conditional flow, you must pass conditions for
            each sample. nsamples will be drawn for each row in conditions.
        save_conditions : bool, default=True
            If true, conditions will be saved in the DataFrame of samples
            that is returned.
        seed : int, optional
            Sets the random seed for the samples.

        Returns
        -------
        pd.DataFrame
            Pandas DataFrame of samples.
        """

        # validate nsamples
        assert isinstance(nsamples, int), "nsamples must be a positive integer."
        assert nsamples > 0, "nsamples must be a positive integer."

        if self.conditional_columns is not None and conditions is None:
            raise ValueError(
                f"Must provide the following conditions\n{self.conditional_columns}"
            )

        # if this isn't a conditional flow, get empty conditions
        if self.conditional_columns is None:
            conditions = np.zeros((nsamples, 1))
        # otherwise get conditions and make `nsamples` copies of each
        else:
            conditions = self._get_conditions(conditions)
            conditions = np.repeat(conditions, nsamples, axis=0)

        # draw from latent distribution
        u = self.latent.sample(self._params[0], conditions.shape[0], seed)
        # take the inverse back to the data distribution
        x = self._inverse(self._params[1], u, conditions=conditions)[0]
        # if not conditional, or save_conditions is False, this is all we need
        if self.conditional_columns is None or save_conditions is False:
            x = pd.DataFrame(x, columns=self.data_columns)
        # but if conditional and save_conditions is True,
        # save conditions with samples
        else:
            # unscale the conditons
            conditions = conditions * self._condition_stds + self._condition_means
            x = pd.DataFrame(
                np.hstack((x, conditions)),
                columns=self.data_columns + self.conditional_columns,
            )

        # return the samples!
        return x

    def save(self, file: str):
        """Saves the flow to a file.

        Pickles the flow and saves it to a file that can be passed as
        the `file` argument during flow instantiation.

        WARNING: Currently, this method only works for bijectors that are
        implemented in the `bijectors` module. If you want to save a flow
        with a custom bijector, you either need to add the bijector to that
        module, or handle the saving and loading on your end.

        Parameters
        ----------
        file : str
            Path to where the flow will be saved.
            Extension `.pkl` will be appended if not already present.
        """
        save_dict = self._save_dict()

        if not file.endswith(".pkl"):
            file += ".pkl"
        with open(file, "wb") as handle:
            pickle.dump(save_dict, handle, recurse=True)

    def train(
        self,
        inputs: pd.DataFrame,
        epochs: int = 50,
        batch_size: int = 1024,
        optimizer: Optimizer = None,
        loss_fn: Callable = None,
        sample_errs: bool = False,
        seed: int = 0,
        verbose: bool = False,
    ) -> list:
        """Trains the normalizing flow on the provided inputs.

        Parameters
        ----------
        inputs : pd.DataFrame
            Data on which to train the normalizing flow.
            Must have columns matching self.data_columns.
        epochs : int, default=50
            Number of epochs to train.
        batch_size : int, default=1024
            Batch size for training.
        optimizer : jax Optimizer, default=adam(step_size=1e-3)
            An optimizer from jax.experimental.optimizers.
        loss_fn : Callable, optional
            A function to calculate the loss: loss = loss_fn(params, x).
            If not provided, will be -mean(log_prob).
        sample_errs : bool, default=False
            Whether to draw new data from the error distributions during
            each epoch of training. Assumes errors are Gaussian, and method
            will look for error columns in `inputs`. Error columns must end
            in `_err`. E.g. the error column for the variable `u` must be
            `u_err`. Zero error assumed for any missing error columns.
        seed : int, default=0
            A random seed to control the batching and the (optional)
            error sampling.
        verbose : bool, default=False
            If true, print the training loss every 5% of epochs.

        Returns
        -------
        list
            List of training losses from every epoch.
        """

        # validate epochs
        if not isinstance(epochs, int) or epochs <= 0:
            raise ValueError("epochs must be a positive integer.")

        # if no loss_fn is provided, use the default loss function
        if loss_fn is None:

            @jit
            def loss_fn(params, x, c):
                return -np.mean(self._log_prob(params, x, c))

        # initialize the optimizer
        optimizer = adam(step_size=1e-3) if optimizer is None else optimizer
        opt_init, opt_update, get_params = optimizer
        opt_state = opt_init(self._params)

        # define the training step function
        @jit
        def step(i, opt_state, x, c):
            params = get_params(opt_state)
            gradients = grad(loss_fn)(params, x, c)
            return opt_update(i, gradients, opt_state)

        # get list of data columns
        columns = list(self.data_columns)

        # if this is a conditional flow, save the means and stds of the conditional columns
        if self.conditional_columns is not None:
            self._condition_means = np.array(
                inputs[list(self.conditional_columns)].values.mean(axis=0)
            )
            self._condition_stds = np.array(
                inputs[list(self.conditional_columns)].values.std(axis=0)
            )

        # define a function to return batches
        if sample_errs:

            def get_batch(sample_rng, x, type):
                return self._get_samples(sample_rng, x, 1, type=type)

        else:

            def get_batch(sample_rng, x, type):
                if type == "conditions":
                    return self._get_conditions(x)
                else:
                    return np.array(x[columns].values)

        # get random seed for training loop
        rng = random.PRNGKey(seed)

        if verbose:
            print(f"Training {epochs} epochs \nLoss:")

        # save the initial loss
        X = np.array(inputs[columns].values)
        C = self._get_conditions(inputs)
        losses = [loss_fn(self._params, X, C)]
        if verbose:
            print(f"(0) {losses[-1]:.4f}")

        # loop through training
        itercount = itertools.count()
        for epoch in range(epochs):
            # new permutation of batches
            permute_rng, sample_rng, rng = random.split(rng, num=3)
            idx = random.permutation(permute_rng, inputs.shape[0])
            X = inputs.iloc[idx]

            # loop through batches and step optimizer
            for batch_idx in range(0, len(X), batch_size):

                # if sampling from the error distribution, this returns a
                # Gaussian sample of the batch. Else just returns batch as a
                # jax array
                batch = get_batch(
                    sample_rng, X.iloc[batch_idx : batch_idx + batch_size], type="data"
                )
                batch_conditions = get_batch(
                    sample_rng,
                    X.iloc[batch_idx : batch_idx + batch_size],
                    type="conditions",
                )

                opt_state = step(
                    next(itercount),
                    opt_state,
                    batch,
                    batch_conditions,
                )

            # save end-of-epoch training loss
            params = get_params(opt_state)
            losses.append(
                loss_fn(
                    params,
                    np.array(X[columns].values),
                    self._get_conditions(X),
                )
            )

            if verbose and (
                epoch % max(int(0.05 * epochs), 1) == 0 or (epoch + 1) == epochs
            ):
                print(f"({epoch+1}) {losses[-1]:.4f}")

        # update the flow parameters with the final training state
        self._params = get_params(opt_state)

        return losses
