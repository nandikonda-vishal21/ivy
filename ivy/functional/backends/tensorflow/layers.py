"""Collection of TensorFlow network layers, wrapped to fit Ivy syntax and signature."""

# global
import tensorflow as tf
from typing import Optional, Tuple, Union, List, Sequence
from tensorflow.python.types.core import Tensor

# local
import ivy


def conv1d(
    x: Union[tf.Tensor, tf.Variable],
    filters: Union[tf.Tensor, tf.Variable],
    strides: int,
    padding: str,
    data_format: str = "NWC",
    dilations: int = 1,
) -> Union[tf.Tensor, tf.Variable]:
    if data_format == "NCW":
        x = tf.transpose(x, (0, 2, 1))
    res = tf.nn.conv1d(x, filters, strides, padding, "NWC", dilations)
    if data_format == "NCW":
        res = tf.transpose(res, (0, 2, 1))
    return res


def conv1d_transpose(
    x,
    filters,
    strides,
    padding,
    output_shape: Optional[Union[ivy.NativeShape, Sequence[int]]] = None,
    data_format="NWC",
    dilations=1,
):
    return tf.nn.conv1d_transpose(
        x, filters, output_shape, strides, padding, data_format, dilations
    )


def conv2d(
    x: Union[tf.Tensor, tf.Variable],
    filters: Union[tf.Tensor, tf.Variable],
    strides: Union[int, Tuple[int, int]],
    padding: str,
    data_format: str = "NHWC",
    dilations: int = 1,
) -> Union[tf.Tensor, tf.Variable]:
    if data_format == "NCHW":
        x = tf.transpose(x, (0, 2, 3, 1))
    res = tf.nn.conv2d(x, filters, strides, padding, "NHWC", dilations)
    if data_format == "NCHW":
        return tf.transpose(res, (0, 3, 1, 2))
    return res


def conv2d_transpose(
    x,
    filters,
    strides,
    padding,
    output_shape: Optional[Union[ivy.NativeShape, Sequence[int]]] = None,
    data_format="NHWC",
    dilations=1,
):
    return tf.nn.conv2d_transpose(
        x, filters, output_shape, strides, padding, data_format, dilations
    )


def depthwise_conv2d(
    x: Union[tf.Tensor, tf.Variable],
    filters: Union[tf.Tensor, tf.Variable],
    strides: int,
    padding: Union[str, List[int]],
    data_format: str = "NHWC",
    dilations: int = 1,
) -> Union[tf.Tensor, tf.Variable]:
    filters = tf.expand_dims(filters, -1)
    strides = [1, strides, strides, 1]
    dilations = [dilations, dilations]
    return tf.nn.depthwise_conv2d(x, filters, strides, padding, data_format, dilations)


# noinspection PyDefaultArgument
def conv3d(x, filters, strides, padding, data_format="NDHWC", dilations=1):
    strides = [1] * 2 + ([strides] * 3 if isinstance(strides, int) else strides)
    dilations = [1] * 2 + ([dilations] * 3 if isinstance(dilations, int) else dilations)
    if data_format == "NCDHW":
        x = tf.transpose(x, (0, 2, 3, 4, 1))
    res = tf.nn.conv3d(x, filters, strides, padding, 'NDHWC', dilations)
    if data_format == "NCDHW":
        return tf.transpose(res, (0, 4, 1, 2, 3))
    return res


def conv3d_transpose(
    x: Tensor,
    filters: Tensor,
    strides: Union[int, Tuple[int], Tuple[int, int], Tuple[int, int, int]],
    padding: str,
    output_shape: Optional[Union[ivy.NativeShape, Sequence[int]]] = None,
    data_format: str = "NDHWC",
    dilations: int = 1,
) -> Tensor:
    return tf.nn.conv3d_transpose(
        x, filters, output_shape, strides, padding, data_format, dilations
    )
