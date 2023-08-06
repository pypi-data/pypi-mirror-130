# Copyright 2021 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#      https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.
"""
Module for nodes related to optimization.
"""
from typing import (
    List,
    Optional,
    Sequence,
    Union,
)

import forge
import numpy as np

from qctrlcommons.node import node_data
from qctrlcommons.node.base import Node
from qctrlcommons.node.documentation import Category
from qctrlcommons.node.utils import validate_inputs_real_fourier_signal
from qctrlcommons.preconditions import (
    check_argument,
    check_argument_integer,
    check_duration,
    check_optimization_variable_parameters,
)


# pylint:disable=line-too-long
class OptimizationVariable(Node):
    r"""
    Creates optimization variables, which can be bounded, semi-bounded, or unbounded.

    Use this function to create a sequence of variables that can be tuned by
    the optimizer (within specified bounds) in order to minimize the cost
    function.

    Parameters
    ----------
    count : int
        The number :math:`N` of individual real-valued variables to create.
    lower_bound : float
        The lower bound :math:`v_\mathrm{min}` for generating an initial value for the variables.
        This will also be used as lower bound if the variables are lower bounded.
        The same lower bound applies to all `count` individual variables.
    upper_bound : float
        The upper bound :math:`v_\mathrm{max}` for generating an initial value for the variables.
        This will also be used as upper bound if the variables are upper bounded.
        The same upper bound applies to all `count` individual variables.
    is_lower_unbounded : bool, optional
        Defaults to False. Set this flag to `True` to define a semi-bounded variable with
        lower bound :math:`-\infty`; in this case, the `lower_bound` parameter is used only for
        generating an initial value.
    is_upper_unbounded : bool, optional
        Defaults to False. Set this flag to True to define a semi-bounded variable with
        upper bound :math:`+\infty`; in this case, the `upper_bound` parameter is used only for
        generating an initial value.
    initial_values : np.ndarray or List[np.ndarray], optional
        Initial values for optimization variable. Defaults to `None`, meaning the optimizer
        initializes these variables with random values. You can either provide a single initial
        value, or a list of them. Note that all optimization variables in a graph with non-default
        initial values must have the same length. That is, you must set them either as a single
        array or a list of arrays of the same length.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The sequence :math:`\{v_n\}` of :math:`N` optimization variables. If both
        `is_lower_unbounded` and `is_upper_unbounded` are `False`, these variables are
        bounded such that :math:`v_\mathrm{min}\leq v_n\leq v_\mathrm{max}`. If one of the
        flags is `True` (for example `is_lower_unbounded=True`), these variables are
        semi-bounded (for example :math:`-\infty \leq v_n \leq v_\mathrm{max}`).
        If both of them are `True`, then these variables are unbounded and satisfy that
        :math:`-\infty \leq v_n \leq +\infty`.

    See Also
    --------
    anchored_difference_bounded_variables : Create anchored optimization variables
        with a difference bound.
    :func:`~qctrl.dynamic.namespaces.FunctionNamespace.calculate_optimization` : Function to find
        the minimum of a generic function.

    Examples
    --------
    Create two independent optimizable variables with equal bounds.

    >>> optimization_variables = graph.optimization_variable(
    ...     count=2, lower_bound=-10, upper_bound=10
    ... )
    >>> optimization_variables
        <Tensor: name="optimization_variable_#0", operation_name="optimization_variable", shape=(2,)>
    >>> x = optimization_variables[0]
    >>> x.name = "x"
    >>> x
        <Tensor: name="x", operation_name="getitem", shape=()>
    >>> y = optimization_variables[1]
    >>> y.name = "y"
    >>> y
        <Tensor: name="y", operation_name="getitem", shape=()>

    Refer to the `How to calculate and optimize with graphs
    <https://docs.q-ctrl.com/boulder-opal/user-guides/how-to-calculate-and-optimize-with-graphs>`_
    user guide to find the example in context.
    """

    name = "optimization_variable"
    optimizable_variable = True
    args = [
        forge.arg("count", type=int),
        forge.arg("lower_bound", type=float),
        forge.arg("upper_bound", type=float),
        forge.arg("is_lower_unbounded", type=bool, default=False),
        forge.arg("is_upper_unbounded", type=bool, default=False),
        forge.arg(
            "initial_values",
            type=Optional[Union[np.ndarray, List[np.ndarray]]],
            default=None,
        ),
    ]
    rtype = node_data.Tensor
    categories = [Category.OPTIMIZATION_VARIABLES]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        count = kwargs["count"]
        lower_bound = kwargs["lower_bound"]
        upper_bound = kwargs["upper_bound"]
        initial_values = kwargs["initial_values"]
        check_optimization_variable_parameters(
            initial_values, count, lower_bound, upper_bound
        )
        return node_data.Tensor(_operation, shape=(count,))


# pylint:disable=line-too-long
class AnchoredDifferenceBoundedVariables(Node):
    r"""
    Creates a sequence of variables with an anchored difference bound.

    Use this function to create a sequence of optimization variables that have
    a difference bound (each variable is constrained to be within a given
    distance of the adjacent variables) and are anchored to zero at the start
    and end (the initial and final variables are within a given distance of
    zero).

    Parameters
    ----------
    count : int
        The number :math:`N` of individual real-valued variables to create.
    lower_bound : float
        The lower bound :math:`v_\mathrm{min}` on the variables.
        The same lower bound applies to all `count` individual variables.
    upper_bound : float
        The upper bound :math:`v_\mathrm{max}` on the variables.
        The same upper bound applies to all `count` individual variables.
    difference_bound : float
        The difference bound :math:`\delta` to enforce between adjacent
        variables.
    initial_values : np.ndarray or List[np.ndarray], optional
        Initial values for optimization variable. Defaults to `None`, meaning the optimizer
        initializes these variables with random values. You can either provide a single initial
        value, or a list of them. Note that all optimization variables in a graph with non-default
        initial values must have the same length. That is, you must set them either as a single
        array or a list of arrays of the same length.
    name : str, optional
        The name of the node.

    Returns
    -------
    Tensor
        The sequence :math:`\{v_n\}` of :math:`N` anchored difference-bounded
        optimization variables, satisfying
        :math:`v_\mathrm{min}\leq v_n\leq v_\mathrm{max}`,
        :math:`|v_{n-1}-v_n|\leq\delta` for :math:`2\leq n\leq N`,
        :math:`|v_1|\leq\delta`, and :math:`|v_N|\leq\delta`.

    See Also
    --------
    bounded_optimization_variable : Create bounded optimization variables.
    :func:`~qctrl.dynamic.namespaces.FunctionNamespace.calculate_optimization` : Function to find
        the minimum of generic functions.
    unbounded_optimization_variable : Create unbounded optimization variables.

    Examples
    --------
    Create an optimizable piecewise-constant signal with anchored difference bounded segment values.

    >>> values = graph.anchored_difference_bounded_variables(
            count=250,
            lower_bound=-5e7,
            upper_bound=5e7,
            difference_bound=5e6,
        )
    >>> values
        <Tensor: name="anchored_difference_bounded_variables_#0", operation_name="anchored_difference_bounded_variables", shape=(250,)>
    >>> alpha = graph.pwc_signal(values=values, duration=400e-9, name="alpha")
    >>> alpha
        <Pwc: name="alpha", operation_name="pwc_signal", value_shape=(), batch_shape=()>

    Refer to the `How to add smoothing and band-limits to optimized controls
    <https://docs.q-ctrl.com/boulder-opal/user-guides/how-to-add-smoothing-and-band-limits-to-optimized-controls>`_
    user guide to find the example in context.
    """

    name = "anchored_difference_bounded_variables"
    optimizable_variable = True
    args = [
        forge.arg("count", type=int),
        forge.arg("lower_bound", type=float),
        forge.arg("upper_bound", type=float),
        forge.arg("difference_bound", type=float),
        forge.arg(
            "initial_values",
            type=Optional[Union[np.ndarray, List[np.ndarray]]],
            default=None,
        ),
    ]
    rtype = node_data.Tensor
    categories = [Category.OPTIMIZATION_VARIABLES]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        count = kwargs["count"]
        lower_bound = kwargs["lower_bound"]
        upper_bound = kwargs["upper_bound"]
        initial_values = kwargs["initial_values"]
        check_optimization_variable_parameters(
            initial_values, count, lower_bound, upper_bound
        )
        return node_data.Tensor(_operation, shape=(count,))


class RealFourierStfSignal(Node):
    r"""
    Creates a real sampleable signal constructed from Fourier components.

    Use this function to create a signal defined in terms of Fourier (sine/cosine)
    basis signals that can be optimized by varying their coefficients and, optionally,
    their frequencies.

    Parameters
    ----------
    duration : float
        The total duration :math:`\tau` of the signal.
    initial_coefficient_lower_bound : float, optional
        The lower bound :math:`c_\mathrm{min}` on the initial coefficient
        values. Defaults to -1.
    initial_coefficient_upper_bound : float, optional
        The upper bound :math:`c_\mathrm{max}` on the initial coefficient
        values. Defaults to 1.
    fixed_frequencies : list[float], optional
        The fixed non-zero frequencies :math:`\{f_m\}` to use for the Fourier
        basis. Must be non-empty if provided. Must be specified in the inverse
        units of `duration` (for example if `duration` is in seconds, these
        values must be given in Hertz).
    optimizable_frequency_count : int, optional
        The number of non-zero frequencies :math:`M` to use, if the
        frequencies can be optimized. Must be greater than zero if provided.
    randomized_frequency_count : int, optional
        The number of non-zero frequencies :math:`M` to use, if the
        frequencies are to be randomized but fixed. Must be greater than zero
        if provided.

    Returns
    -------
    Stf(1D, real)
        The optimizable, real-valued, sampleable signal built from the
        appropriate Fourier components.

    Warnings
    --------
    You must provide exactly one of `fixed_frequencies`, `optimizable_variable`,
    or `randomized_frequency_count`.

    See Also
    --------
    real_fourier_pwc_signal : Corresponding operation for `Pwc`.

    Notes
    -----
    This function sets the basis signal frequencies :math:`\{f_m\}`
    depending on the chosen mode:

    * For fixed frequencies, you provide the frequencies directly.
    * For optimizable frequencies, you provide the number of frequencies
      :math:`M`, and this function creates :math:`M` unbounded optimizable
      variables :math:`\{f_m\}`, with initial values in the ranges
      :math:`\{[(m-1)/\tau, m/\tau]\}`.
    * For randomized frequencies, you provide the number of frequencies
      :math:`M`, and this function creates :math:`M` randomized constants
      :math:`\{f_m\}` in the ranges :math:`\{[(m-1)/\tau, m/\tau]\}`.

    After this function creates the :math:`M` frequencies :math:`\{f_m\}`, it
    produces the signal

    .. math::
        \alpha^\prime(t) = v_0 +
        \sum_{m=1}^M [ v_m \cos(2\pi t f_m) + w_m \sin(2\pi t f_m) ],

    where :math:`\{v_m,w_m\}` are (unbounded) optimizable variables, with
    initial values bounded by :math:`c_\mathrm{min}` and
    :math:`c_\mathrm{max}`. This function produces the final signal :math:`\alpha(t)`.

    You can use the signals created by this function for chopped random basis
    (CRAB) optimization [1]_.

    References
    ----------
    .. [1] `P. Doria, T. Calarco, and S. Montangero, Physical Review Letters 106, 190501 (2011).
           <https://doi.org/10.1103/PhysRevLett.106.190501>`_
    """

    name = "real_fourier_stf_signal"
    optimizable_variable = True
    args = [
        forge.arg("duration", type=float),
        forge.arg("initial_coefficient_lower_bound", type=float, default=-1),
        forge.arg("initial_coefficient_upper_bound", type=float, default=1),
        forge.arg("fixed_frequencies", type=Optional[List[float]], default=None),
        forge.arg("optimizable_frequency_count", type=Optional[int], default=None),
        forge.arg("randomized_frequency_count", type=Optional[int], default=None),
    ]
    kwargs = {}  # Stfs don't accept name as an argument.
    rtype = node_data.Stf
    categories = [
        Category.BUILDING_SMOOTH_HAMILTONIANS,
        Category.OPTIMIZATION_VARIABLES,
    ]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        duration = kwargs.get("duration")
        check_duration(duration, "duration")

        fixed_frequencies = kwargs.get("fixed_frequencies")
        optimizable_frequency_count = kwargs.get("optimizable_frequency_count")
        randomized_frequency_count = kwargs.get("randomized_frequency_count")
        validate_inputs_real_fourier_signal(
            fixed_frequencies, optimizable_frequency_count, randomized_frequency_count
        )

        return node_data.Stf(_operation, value_shape=(), batch_shape=())


# pylint:disable=line-too-long
class RealFourierPwcSignal(Node):
    r"""
    Creates a piecewise-constant signal constructed from Fourier components.

    Use this function to create a signal defined in terms of Fourier
    (sine/cosine) basis signals that can be optimized by varying their
    coefficients and, optionally, their frequencies.

    Parameters
    ----------
    duration : float
        The total duration :math:`\tau` of the signal.
    segment_count : int
        The number of segments :math:`N` to use for the piecewise-constant
        approximation.
    initial_coefficient_lower_bound : float, optional
        The lower bound :math:`c_\mathrm{min}` on the initial coefficient
        values. Defaults to -1.
    initial_coefficient_upper_bound : float, optional
        The upper bound :math:`c_\mathrm{max}` on the initial coefficient
        values. Defaults to 1.
    fixed_frequencies : list[float], optional
        The fixed non-zero frequencies :math:`\{f_m\}` to use for the Fourier
        basis. Must be non-empty if provided. Must be specified in the inverse
        units of `duration` (for example if `duration` is in seconds, these
        values must be given in Hertz).
    optimizable_frequency_count : int, optional
        The number of non-zero frequencies :math:`M` to use, if the
        frequencies can be optimized. Must be greater than zero if provided.
    randomized_frequency_count : int, optional
        The number of non-zero frequencies :math:`M` to use, if the
        frequencies are to be randomized but fixed. Must be greater than zero
        if provided.
    name : str, optional
        The name of the node.

    Returns
    -------
    Pwc(1D, real)
        The optimizable, real-valued, piecewise-constant signal built from the
        appropriate Fourier components.

    Warnings
    --------
    You must provide exactly one of `fixed_frequencies`, `optimizable_variable`,
    or `randomized_frequency_count`.

    See Also
    --------
    real_fourier_stf_signal : Corresponding operation for `Stf`.

    Notes
    -----
    This function sets the basis signal frequencies :math:`\{f_m\}`
    depending on the chosen mode:

    * For fixed frequencies, you provide the frequencies directly.
    * For optimizable frequencies, you provide the number of frequencies
      :math:`M`, and this function creates :math:`M` unbounded optimizable
      variables :math:`\{f_m\}`, with initial values in the ranges
      :math:`\{[(m-1)/\tau, m/\tau]\}`.
    * For randomized frequencies, you provide the number of frequencies
      :math:`M`, and this function creates :math:`M` randomized constants
      :math:`\{f_m\}` in the ranges :math:`\{[(m-1)/\tau, m/\tau]\}`.

    After this function creates the :math:`M` frequencies :math:`\{f_m\}`, it
    produces the signal

    .. math::
        \alpha^\prime(t) = v_0 +
        \sum_{m=1}^M [ v_m \cos(2\pi t f_m) + w_m \sin(2\pi t f_m) ],

    where :math:`\{v_m,w_m\}` are (unbounded) optimizable variables, with
    initial values bounded by :math:`c_\mathrm{min}` and
    :math:`c_\mathrm{max}`. This function produces the final
    piecewise-constant signal :math:`\alpha(t)` by sampling
    :math:`\alpha^\prime(t)` at :math:`N` equally spaced points along the
    duration :math:`\tau`, and using those sampled values as the constant
    segment values.

    You can use the signals created by this function for chopped random basis
    (CRAB) optimization [1]_.

    References
    ----------
    .. [1] `P. Doria, T. Calarco, and S. Montangero, Physical Review Letters 106, 190501 (2011).
           <https://doi.org/10.1103/PhysRevLett.106.190501>`_

    Examples
    --------
    Create an optimizable piecewise-constant signal with 10 Fourier components.

    >>> alpha = graph.real_fourier_pwc_signal(
            duration=100e-9,
            segment_count=200,
            initial_coefficient_lower_bound=-30e6,
            initial_coefficient_upper_bound=30e6,
            optimizable_frequency_count=10,
            name="alpha",
        )
    >>> alpha
        <Pwc: name="alpha", operation_name="real_fourier_pwc_signal", value_shape=(), batch_shape=()>

    Refer to the `How to perform model-based optimization using a Fourier basis
    <https://docs.q-ctrl.com/boulder-opal/user-guides/how-to-perform-model-based-optimization-using-a-fourier-basis>`_
    user guide to find the example in context.
    """

    name = "real_fourier_pwc_signal"
    optimizable_variable = True
    args = [
        forge.arg("duration", type=float),
        forge.arg("segment_count", type=int),
        forge.arg("initial_coefficient_lower_bound", type=float, default=-1),
        forge.arg("initial_coefficient_upper_bound", type=float, default=1),
        forge.arg("fixed_frequencies", type=Optional[List[float]], default=None),
        forge.arg("optimizable_frequency_count", type=Optional[int], default=None),
        forge.arg("randomized_frequency_count", type=Optional[int], default=None),
    ]
    rtype = node_data.Pwc
    categories = [
        Category.BUILDING_PIECEWISE_CONSTANT_HAMILTONIANS,
        Category.OPTIMIZATION_VARIABLES,
    ]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        duration = kwargs.get("duration")
        segment_count = kwargs.get("segment_count")
        check_duration(duration, "duration")

        check_argument_integer(segment_count, "segment_count")
        check_argument(
            segment_count > 0,
            "The number of segments must be greater than zero.",
            {"segment_count": segment_count},
        )

        fixed_frequencies = kwargs.get("fixed_frequencies")
        optimizable_frequency_count = kwargs.get("optimizable_frequency_count")
        randomized_frequency_count = kwargs.get("randomized_frequency_count")
        validate_inputs_real_fourier_signal(
            fixed_frequencies, optimizable_frequency_count, randomized_frequency_count
        )

        durations = duration / segment_count * np.ones(segment_count)

        return node_data.Pwc(
            _operation, value_shape=(), durations=durations, batch_shape=()
        )


class RandomChoices(Node):
    r"""
    Creates random samples from the data that you provide.

    You can provide the data as a list and each element of that list represents one component
    of the full data. For example, considering a single variable linear regression problem
    that is described by the input :math:`x` and output :math:`y`, the data you provide would
    be :math:`[x, y]`. The first dimension of the data component in this list is the size of
    the data and therefore must be same for all components. However, all these components can
    have different value shapes, meaning the other dimensions can vary.

    This node effectively chooses a random batch of `sample_count` indices :math:`\{s_i\}`,
    and extracts the corresponding slices :math:`\{c[s_i]\}` of each data component.
    For example, in the case of linear regression, you can use this node to extract a random
    subset of your full data set.

    If this node is evaluated multiple times (for example during an optimization), it samples
    indices without replacement until all indices have been seen, at which point it starts sampling
    from the full set of indices again. You can therefore use this node to create minibatches that
    iterate over your data set in a series of epochs.

    Parameters
    ----------
    data : list[np.ndarray or Tensor]
        A list of data components. The first dimensions of the elements in this
        list denote the total amount of the data, and therefore must be the same.
    sample_count : int
        Number of samples in the returned batch.
    seed : int, optional
        Seed for random number generator. Defaults to ``None``. If set, it ensures the
        random samples are generated in a reproducible sequence.
    name : str, optional
        The name of the node.

    Returns
    -------
    Sequence[Tensor]
        A sequence representing a batch of random samples from `data`.
        You can access the elements of the sequence using integer indices.
        The number of elements of the sequence is the same as the size of `data`.
        Each element of the sequence has the length (along its first dimension)
        as defined by `sample_count`.

    See Also
    --------
    :func:`~qctrl.dynamic.namespaces.FunctionNamespace.calculate_stochastic_optimization` : Function
        to perform gradient-based stochastic optimization of generic real-valued functions.

    Examples
    --------
    Create batches of size 100 from two datasets of size 5000.

    >>> omega_dataset.shape
        (5000, 10)
    >>> measurement_dataset.shape
        (5000,)
    >>> (omega_values_batch, measurement_batch) = graph.random_choices(
    ...     data=[omega_dataset, measurement_dataset], sample_count=100
    ... )
    >>> omega_values_batch
        <Tensor: name="getitem_#1", operation_name="getitem", shape=(100, 10)>
    >>> measurement_batch
        <Tensor: name="getitem_#2", operation_name="getitem", shape=(100,)>
    >>> omega_signal = graph.pwc_signal(values=omega_values_batch, duration=1e-5)
    >>> omega_signal
        <Pwc: name="pwc_signal_#9", operation_name="pwc_signal", value_shape=(), batch_shape=(100,)>

    Refer to the `How to perform Hamiltonian parameter estimation using a large amount of measured data
    <https://docs.q-ctrl.com/boulder-opal/user-guides/how-to-perform-hamiltonian-parameter-estimation-using-a-large-amount-of-measured-data>`_
    user guide to find the example in context.
    """

    name = "random_choices"
    args = [
        forge.arg("data", type=List[Union[np.ndarray, node_data.Tensor]]),
        forge.arg("sample_count", type=int),
        forge.arg("seed", type=Optional[int], default=None),
    ]
    rtype = Sequence[node_data.Tensor]
    categories = [Category.RANDOM_OPERATIONS]

    @classmethod
    def create_node_data(cls, _operation, **kwargs):
        data = kwargs.get("data")
        sample_count = kwargs.get("sample_count")
        seed = kwargs.get("seed")

        data_size = data[0].shape[0]
        check_argument(
            all((value.shape[0] == data_size for value in data)),
            "The first dimension of the elements in `data` must be the same.",
            arguments={"data": data},
        )
        check_argument(
            0 < sample_count <= data_size,
            "`sample_count` must be positive and not greater than the size of the "
            "data you provide.",
            arguments={"sample_count": sample_count},
            extras={"data size": data_size},
        )
        if seed is not None:
            check_argument_integer(seed, "seed")

        return_tensor_shapes = [(sample_count,) + value.shape[1:] for value in data]
        node_constructor = lambda operation, index: node_data.Tensor(
            operation, return_tensor_shapes[index]
        )
        return node_data.Sequence(_operation).create_sequence(
            node_constructor, size=len(data)
        )
