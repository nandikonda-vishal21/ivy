# global
import numpy
import numpy as np
from typing import Union, Optional, List, Sequence

# local
import ivy
from .data_type import as_native_dtype
from ivy.functional.ivy import default_dtype
from ivy.functional.backends.numpy.device import _to_device


# Array API Standard #
# -------------------#


def arange(
    start,
    stop=None,
    step=1,
    *,
    dtype: np.dtype = None,
    device: str,
    out: Optional[np.ndarray] = None
):
    if dtype:
        dtype = as_native_dtype(dtype)
    res = _to_device(np.arange(start, stop, step=step, dtype=dtype), device=device)
    if not dtype:
        if res.dtype == np.float64:
            return res.astype(np.float32)
        elif res.dtype == np.int64:
            return res.astype(np.int32)
    return res


def asarray(
    object_in,
    *,
    copy=None,
    dtype: np.dtype = None,
    device: str,
    out: Optional[np.ndarray] = None
):
    # If copy=none then try using existing memory buffer
    if isinstance(object_in, np.ndarray) and dtype is None:
        dtype = object_in.dtype
    elif (
        isinstance(object_in, (list, tuple, dict))
        and len(object_in) != 0
        and dtype is None
    ):
        dtype = default_dtype(item=object_in, as_native=True)
        if copy is True:
            return _to_device(
                np.copy(np.asarray(object_in, dtype=dtype)), device=device
            )
        else:
            return _to_device(np.asarray(object_in, dtype=dtype), device=device)
    else:
        dtype = default_dtype(dtype, object_in)
    if copy is True:
        return _to_device(np.copy(np.asarray(object_in, dtype=dtype)), device=device)
    else:
        return _to_device(np.asarray(object_in, dtype=dtype), device=device)


def empty(
    shape: Union[ivy.NativeShape, Sequence[int]],
    *,
    dtype: np.dtype,
    device: str,
    out: Optional[np.ndarray] = None
) -> np.ndarray:
    return _to_device(
        np.empty(shape, as_native_dtype(default_dtype(dtype))), device=device
    )


def empty_like(
    x: np.ndarray, *, dtype: np.dtype, device: str, out: Optional[np.ndarray] = None
) -> np.ndarray:
    if dtype:
        dtype = "bool_" if dtype == "bool" else dtype
        dtype = np.dtype(dtype)
    else:
        dtype = x.dtype

    return _to_device(np.empty_like(x, dtype=dtype), device=device)


def eye(
    n_rows: int,
    n_cols: Optional[int] = None,
    k: Optional[int] = 0,
    batch_shape: Optional[Union[int, Sequence[int]]] = None,
    *,
    dtype: np.dtype,
    device: str,
    out: Optional[np.ndarray] = None
) -> np.ndarray:
    dtype = as_native_dtype(default_dtype(dtype))
    if n_cols is None:
        n_cols = n_rows
    i = np.eye(n_rows, n_cols, k, dtype)
    if batch_shape is None:
        return _to_device(i, device=device)
    else:
        reshape_dims = [1] * len(batch_shape) + [n_rows, n_cols]
        tile_dims = list(batch_shape) + [1, 1]
        return_mat = np.tile(np.reshape(i, reshape_dims), tile_dims)
        return _to_device(return_mat, device=device)


# noinspection PyShadowingNames
def from_dlpack(x, *, out: Optional[np.ndarray] = None):
    # noinspection PyProtectedMember
    return np._from_dlpack(x)


def _assert_fill_value_and_dtype_are_compatible(dtype, fill_value):
    assert (
        (ivy.is_int_dtype(dtype) and isinstance(fill_value, int))
        or (ivy.is_float_dtype(dtype) and isinstance(fill_value, float))
        or (isinstance(fill_value, bool))
    ), "the fill_value and data type are not same"


def full(
    shape: Union[ivy.NativeShape, Sequence[int]],
    fill_value: Union[int, float, bool],
    *,
    dtype: Optional[Union[ivy.Dtype, np.dtype]] = None,
    device: str,
    out: Optional[np.ndarray] = None
) -> np.ndarray:
    dtype = ivy.default_dtype(dtype, item=fill_value, as_native=True)
    _assert_fill_value_and_dtype_are_compatible(dtype, fill_value)
    return _to_device(
        np.full(shape, fill_value, dtype),
        device=device,
    )


def full_like(
    x: np.ndarray,
    fill_value: Union[int, float],
    *,
    dtype: Optional[Union[ivy.Dtype, np.dtype]] = None,
    device: str,
    out: Optional[np.ndarray] = None
) -> np.ndarray:
    dtype = ivy.default_dtype(dtype, item=fill_value, as_native=True)
    _assert_fill_value_and_dtype_are_compatible(dtype, fill_value)
    if dtype:
        dtype = "bool_" if dtype == "bool" else dtype
    else:
        dtype = x.dtype
    return _to_device(np.full_like(x, fill_value, dtype=dtype), device=device)


def linspace(
    start,
    stop,
    num,
    axis=None,
    endpoint=True,
    *,
    dtype: np.dtype,
    device: str,
    out: Optional[np.ndarray] = None
):
    if axis is None:
        axis = -1
    ans = np.linspace(start, stop, num, endpoint, dtype=dtype, axis=axis)
    if dtype is None:
        ans = np.float32(ans)
    # Waiting for fix when start is -0.0: https://github.com/numpy/numpy/issues/21513
    if (
        ans.shape[0] >= 1
        and (not isinstance(start, numpy.ndarray))
        and (not isinstance(stop, numpy.ndarray))
    ):
        ans[0] = start
    return _to_device(ans, device=device)


def meshgrid(*arrays: np.ndarray, indexing: str = "xy") -> List[np.ndarray]:
    return np.meshgrid(*arrays, indexing=indexing)


def ones(
    shape: Union[ivy.NativeShape, Sequence[int]],
    *,
    dtype: np.dtype,
    device: str,
    out: Optional[np.ndarray] = None
) -> np.ndarray:
    dtype = as_native_dtype(default_dtype(dtype))
    return _to_device(np.ones(shape, dtype), device=device)


def ones_like(
    x: np.ndarray, *, dtype: np.dtype, device: str, out: Optional[np.ndarray] = None
) -> np.ndarray:
    if dtype:
        dtype = "bool_" if dtype == "bool" else dtype
        dtype = np.dtype(dtype)
    else:
        dtype = x.dtype

    return _to_device(np.ones_like(x, dtype=dtype), device=device)


def tril(x: np.ndarray, k: int = 0, *, out: Optional[np.ndarray] = None) -> np.ndarray:
    return np.tril(x, k)


def triu(x: np.ndarray, k: int = 0, *, out: Optional[np.ndarray] = None) -> np.ndarray:
    return np.triu(x, k)


def zeros(
    shape: Union[ivy.NativeShape, Sequence[int]],
    *,
    dtype: np.dtype,
    device: str,
    out: Optional[np.ndarray] = None
) -> np.ndarray:
    return _to_device(np.zeros(shape, dtype), device=device)


def zeros_like(
    x: np.ndarray, *, dtype: np.dtype, device: str, out: Optional[np.ndarray] = None
) -> np.ndarray:
    if dtype:
        dtype = "bool_" if dtype == "bool" else dtype
    else:
        dtype = x.dtype
    return _to_device(np.zeros_like(x, dtype=dtype), device=device)


# Extra #
# ------#


array = asarray


def logspace(
    start,
    stop,
    num,
    base=10.0,
    axis=None,
    *,
    device: str,
    out: Optional[np.ndarray] = None
):
    if axis is None:
        axis = -1
    return _to_device(
        np.logspace(start, stop, num, base=base, axis=axis), device=device
    )
