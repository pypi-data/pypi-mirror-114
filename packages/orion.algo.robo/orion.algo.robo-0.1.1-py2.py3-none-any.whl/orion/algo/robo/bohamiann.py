"""
Wrapper for RoBO with BOHAMIANN
"""
import torch
from pybnn.bohamiann import Bohamiann
from robo.models.base_model import BaseModel
from robo.models.wrapper_bohamiann import get_default_network

from orion.algo.robo.base import RoBO, build_bounds


class RoBO_BOHAMIANN(RoBO):
    """
    Wrapper for RoBO with BOHAMIANN

    For more information on the algorithm, see original paper at
    https://papers.nips.cc/paper/2016/hash/a96d3afec184766bfeca7a9f989fc7e7-Abstract.html.

    Springenberg, Jost Tobias, et al.
    "Bayesian optimization with robust Bayesian neural networks."
    Advances in neural information processing systems 29 (2016): 4134-4142.

    Parameters
    ----------
    space: ``orion.algo.space.Space``
        Optimisation space with priors for each dimension.
    seed: None, int or sequence of int
        Seed to sample initial points and candidates points.
        Default: 0.
    n_initial_points: int
        Number of initial points randomly sampled. If new points
        are requested and less than `n_initial_points` are observed,
        the next points will also be sampled randomly instead of being
        sampled from the parzen estimators.
        Default: ``20``
    maximizer: str
        The optimizer for the acquisition function.
        Can be one of ``{"random", "scipy", "differential_evolution"}``.
        Defaults to 'random'
    acquisition_func: str
        Name of the acquisition function. Can be one of ``['ei', 'log_ei', 'pi', 'lcb']``.
    normalize_input: bool
        Normalize the input based on the provided bounds (zero mean and unit standard deviation).
        Defaults to ``True``.
    normalize_output: bool
        Normalize the output based on data (zero mean and unit standard deviation).
        Defaults to ``False``.
    burnin_steps: int or None.
        The number of burnin steps before the sampling procedure starts.
        If ``None``, ``burnin_steps = n_dims * 100`` where ``n_dims`` is the dimensionality
        of the search space. Defaults to ``None``.
    sampling_method: str
        Can be one of ``['adaptive_sghmc', 'sgld', 'preconditioned_sgld', 'sghmc']``.
        Defaults to ``"adaptive_sghmc"``. See PyBNN samplers'
        `code <https://github.com/automl/pybnn/tree/master/pybnn/sampler>`_ for more information.
    use_double_precision: bool
        Use double precision if using ``bohamiann``. Note that it can run faster on GPU
        if using single precision. Defaults to ``True``.
    num_steps: int or None
        Number of sampling steps to perform after burn-in is finished.
        In total, ``num_steps // keep_every`` network weights will be sampled.
        If ``None``, ``num_steps = n_dims * 100 + 10000`` where ``n_dims`` is the
        dimensionality of the search space.
    keep_every: int
        Number of sampling steps (after burn-in) to perform before keeping a sample.
        In total, ``num_steps // keep_every`` network weights will be sampled.
    learning_rate: float
        Learning rate. Defaults to 1e-2.
    batch_size: int
        Batch size for training the neural network. Defaults to 20.
    epsilon: float
        epsilon for numerical stability. Defaults to 1e-10.
    mdecay: float
        momemtum decay. Defaults to 0.05.
    verbose: bool
        Write progress logs in stdout. Defaults to ``False``.

    """

    def __init__(
        self,
        space,
        seed=0,
        n_initial_points=20,
        maximizer="random",
        acquisition_func="log_ei",
        normalize_input=True,
        normalize_output=False,
        burnin_steps=None,
        sampling_method="adaptive_sghmc",
        use_double_precision=True,
        num_steps=None,
        keep_every=100,
        learning_rate=1e-2,
        batch_size=20,
        epsilon=1e-10,
        mdecay=0.05,
        verbose=False,
    ):

        super(RoBO_BOHAMIANN, self).__init__(
            space,
            maximizer=maximizer,
            acquisition_func=acquisition_func,
            normalize_input=normalize_input,
            normalize_output=normalize_output,
            burnin_steps=burnin_steps,
            sampling_method=sampling_method,
            use_double_precision=use_double_precision,
            num_steps=num_steps,
            keep_every=keep_every,
            learning_rate=learning_rate,
            batch_size=batch_size,
            epsilon=epsilon,
            mdecay=mdecay,
            verbose=verbose,
            n_initial_points=n_initial_points,
            seed=seed,
        )

    def _initialize_model(self):
        lower, upper = build_bounds(self.space)
        self.model = OrionBohamiannWrapper(
            normalize_input=self.normalize_input,
            normalize_output=self.normalize_output,
            burnin_steps=self.burnin_steps,
            sampling_method=self.sampling_method,
            use_double_precision=self.use_double_precision,
            num_steps=self.num_steps,
            keep_every=self.keep_every,
            learning_rate=self.learning_rate,
            batch_size=self.batch_size,
            epsilon=self.epsilon,
            mdecay=self.mdecay,
            verbose=self.verbose,
            lower=lower,
            upper=upper,
        )


class OrionBohamiannWrapper(BaseModel):
    """
    Wrapper for PyBNN's BOHAMIANN model

    Parameters
    ----------
    normalize_input: bool
        Normalize the input based on the provided bounds (zero mean and unit standard deviation).
        Defaults to ``True``.
    normalize_output: bool
        Normalize the output based on data (zero mean and unit standard deviation).
        Defaults to ``False``.
    burnin_steps: int or None.
        The number of burnin steps before the sampling procedure starts.
        If ``None``, ``burnin_steps = n_dims * 100`` where ``n_dims`` is the dimensionality
        of the search space. Defaults to ``None``.
    sampling_method: str
        Can be one of ``['adaptive_sghmc', 'sgld', 'preconditioned_sgld', 'sghmc']``.
        Defaults to ``"adaptive_sghmc"``. See PyBNN samplers'
        `code <https://github.com/automl/pybnn/tree/master/pybnn/sampler>`_ for more information.
    use_double_precision: bool
        Use double precision if using ``bohamiann``. Note that it can run faster on GPU
        if using single precision. Defaults to ``True``.
    num_steps: int or None
        Number of sampling steps to perform after burn-in is finished.
        In total, ``num_steps // keep_every`` network weights will be sampled.
        If ``None``, ``num_steps = n_dims * 100 + 10000`` where ``n_dims`` is the
        dimensionality of the search space.
    keep_every: int
        Number of sampling steps (after burn-in) to perform before keeping a sample.
        In total, ``num_steps // keep_every`` network weights will be sampled.
    learning_rate: float
        Learning rate. Defaults to 1e-2.
    batch_size: int
        Batch size for training the neural network. Defaults to 20.
    epsilon: float
        epsilon for numerical stability. Defaults to 1e-10.
    mdecay: float
        momemtum decay. Defaults to 0.05.
    verbose: bool
        Write progress logs in stdout. Defaults to ``False``.

    """

    def __init__(
        self,
        lower,
        upper,
        sampling_method="adaptive_sghmc",
        use_double_precision=True,
        num_steps=None,
        keep_every=100,
        burnin_steps=None,
        learning_rate=1e-2,
        batch_size=20,
        epsilon=1e-10,
        mdecay=0.05,
        verbose=False,
        **kwargs
    ):

        self.num_steps = num_steps
        self.keep_every = keep_every
        self.burnin_steps = burnin_steps
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.epsilon = epsilon
        self.mdecay = mdecay
        self.verbose = verbose

        self.bnn = Bohamiann(
            get_network=get_default_network,
            sampling_method=sampling_method,
            use_double_precision=use_double_precision,
            **kwargs
        )
        self.burnin_steps = burnin_steps

        self.lower = lower
        self.upper = upper

    # pylint:disable=no-self-use
    def set_state(self, state_dict):
        """Restore the state of the optimizer"""
        torch.random.set_rng_state(state_dict["torch"])

    # pylint:disable=no-self-use
    def state_dict(self):
        """Return the current state of the optimizer so that it can be restored"""
        return {"torch": torch.random.get_rng_state()}

    def seed(self, seed):
        """Seed all internal RNGs"""
        if torch.cuda.is_available():
            torch.backends.cudnn.benchmark = False
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True

        torch.manual_seed(seed)

    def train(self, X, y, **kwargs):
        """
        Sets num_steps and burnin_steps before training with parent's train()
        """
        self.X = X
        self.y = y

        if self.num_steps:
            num_steps = self.num_steps
        else:
            num_steps = X.shape[0] * 100 + 10000

        if self.burnin_steps is None:
            burnin_steps = X.shape[0] * 100
        else:
            burnin_steps = self.burnin_steps

        self.bnn.train(
            X,
            y,
            num_steps=num_steps,
            keep_every=self.keep_every,
            num_burn_in_steps=burnin_steps,
            lr=self.learning_rate,
            batch_size=self.batch_size,
            epsilon=self.epsilon,
            mdecay=self.mdecay,
            continue_training=False,
            verbose=self.verbose,
            **kwargs
        )

    def predict(self, X_test):
        """Predict using bnn.predict()"""
        return self.bnn.predict(X_test)
