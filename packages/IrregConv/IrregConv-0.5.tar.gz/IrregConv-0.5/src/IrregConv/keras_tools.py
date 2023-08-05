import tensorflow as tf
from tensorflow.keras.layers import *
import numpy as np

def rand_mask(num_filters, num_channels, weights_per_kernel = 4, dtype = tf.float32):
    """
    args:
        num_filters:
        num_channels:
        weights_per_kernel:
        dtype:
    return:
        mask: a randomly generated mask for sparse conv 
    """
    choices = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]
    mask = np.zeros((3, 3, num_channels, num_filters))
    for f in range(num_filters):
        for c in range(num_channels):
            mask[1, 1, c, f] = 9./weights_per_kernel
            ks = np.random.permutation(len(choices))
            for k in ks[:weights_per_kernel-1]: 
                i, j = choices[k]
                mask[i, j, c, f] = 9./weights_per_kernel
    return tf.cast(mask, dtype)

class IrregConv2D(Conv2D):
    """
    Irregular kernel convolution
    Can significantly reduce overfitting 
    while traditional kernels look like this:
        [w00, w01, w02,
         w10, w11, w12,
         w20, w21, w22]
    irregular kernels look like this for example:
        [0  , w01, 0,
         w10, w11, w12,
         0  , 0  , 0]
    Two differently shaped kernels cannot learn to identify the same features. This 
    promotes the network to learn more feature and generalize better
    """
    def __init__(self, *args, mask_fn = rand_mask, weights_per_kernel = 4, **kwargs):
        super(IrregConv2D, self).__init__(*args, **kwargs)
        self.mask_fn = mask_fn
        self.wpk = weights_per_kernel
        
    def build(self, input_shape):
        self.mask = self.mask_fn(self.filters, input_shape[-1], weights_per_kernel = self.wpk)
        super(IregConv2D, self).build(input_shape)
        w = self.get_weights()
        w[0] = tf.multiply(w[0], self.mask)
        self.set_weights(w)

    def convolution_op(self, inputs, kernel):
        if self.padding == 'causal':
            tf_padding = 'VALID'  # Causal padding handled in `call`.
        elif isinstance(self.padding, str):
            tf_padding = self.padding.upper()
        else:
            tf_padding = self.padding
        kernel = tf.multiply(kernel, self.mask)

        return tf.nn.convolution(
            inputs,
            kernel,
            strides=list(self.strides),
            padding=tf_padding,
            dilations=list(self.dilation_rate),
            data_format=self._tf_data_format,
            name=self.__class__.__name__)