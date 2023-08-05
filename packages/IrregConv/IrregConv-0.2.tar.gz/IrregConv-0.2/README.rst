Providing an easy way for devoloper to include irregular convolution in there models. 

irregularly shaped kernels can reduce over fitting significantly. Although this has been 
known for years, there is not an easy way for devolopers to include irregular convolution in
their models. This package aims to change that. 

NOTE: at the moment, the only supported kernel size is (3, 3)

Use:

for keras:
    from IrregConv.keras_tools import IrregConv2D

you can use "IrregConv2D" in your keras model in the same way as normal keras layer. It takes all
of the same inputs as keras.layers.Conv2D so the two can be easily interchanged. The two layers
behave in the same way except "IrregConv2D" irregularly shaped kernels.

for PyTorch:
    from IrregConv.torch_tools import IrregConv2D