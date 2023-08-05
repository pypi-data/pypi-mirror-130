# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['high_order_layers_torch']

package_data = \
{'': ['*']}

install_requires = \
['pytorch-lightning', 'torch']

setup_kwargs = {
    'name': 'high-order-layers-torch',
    'version': '1.1.0',
    'description': 'High order layers in pytorch',
    'long_description': '[![Build Status](https://travis-ci.org/jloveric/high-order-layers-torch.svg?branch=master)](https://travis-ci.org/jloveric/high-order-layers-torch)\n\n# Functional Layers in PyTorch\n\nThis is a PyTorch implementation of my tensorflow [repository](https://github.com/jloveric/high-order-layers) and is more complete due to the flexibility of PyTorch.\n\nLagrange Polynomial, Piecewise Lagrange Polynomial, Discontinuous Piecewise Lagrange Polynomial, Fourier Series, sum and product layers in PyTorch.  The sparsity of using piecewise polynomial layers means that by adding new segments the representational power of your network increases, but the time to complete a forward step remains constant.  Implementation includes simple fully connected layers and convolution layers using these models.  More details to come.  This is a PyTorch implementation of this [paper](https://www.researchgate.net/publication/276923198_Discontinuous_Piecewise_Polynomial_Neural_Networks) including extension to Fourier Series and convolutional neural networks.\n\nThe layers used here do not require additional activation functions and use a simple sum or product in place of the activation.  Product is performed in this manner\n\n<img src="https://render.githubusercontent.com/render/math?math=product=-1%2B\\prod_{i}(1 %2B f_{i})%2B(1-\\alpha)\\sum_{i}f_{i}">\n\nThe 1 is added to each function output to as each of the sub products is also computed.  The linear part is controlled by\nthe alpha parameter.\n\n# Fully Connected Layer Types\nAll polynomials are Lagrange polynomials with Chebyshev interpolation points.\n\nA helper function is provided in selecting and switching between these layers\n\n```python\nfrom high_order_layers_torch.layers import *\nlayer1 = high_order_fc_layers(\n    layer_type=layer_type,\n    n=n, \n    in_features=784,\n    out_features=100,\n    segments=segments,\n    alpha=linear_part\n)\n```\n\nwhere `layer_type` is one of\n| layer_type          | representation\n|--------------------|-------------------------|\n|continuous         |  piecewise polynomial using sum at the neuron |\n|continuous_prod    |  piecewise polynomial using products at the neuron |\n|discontinuous      |  discontinuous piecewise polynomial with sum at the neuron|\n|discontinuous_prod | discontinous piecewise polynomial with product at the neuron|\n|polynomial | single polynomial (non piecewise) with sum at the neuron|\n|polynomial_prod | single polynomial (non piecewise) with product at the neuron|\n|product | Product |\n|fourier | fourier series with sum at the neuron |\n\n\n\n`n` is the number of interpolation points per segment for polynomials or the number of frequencies for fourier series, `segments` is the number of segments for piecewise polynomials, `alpha` is used in product layers and when set to 1 keeps the linear part of the product, when set to 0 it subtracts the linear part from the product.\n\n## Product Layers\n\nProduct layers\n\n# Convolutional Layer Types\n\n```python\nconv_layer = high_order_convolution_layers(layer_type=layer_type, n=n, in_channels=3, out_channels=6, kernel_size=5, segments=segments, rescale_output=rescale_output, periodicity=periodicity)\n```         \n\nAll polynomials are Lagrange polynomials with Chebyshev interpolation points.\n| layer_type   | representation       |\n|--------------|----------------------|\n|continuous(1d,2d)   | piecewise continuous polynomial\n|discontinuous(1d,2d) | piecewise discontinuous polynomial\n|polynomial(1d,2d) | single polynomial\n|fourier(1d,2d) | fourier series convolution\n\n# Installing\n\n## Installing locally\n\nThis repo uses poetry, so run\n\n```\npoetry install\n```\n\nand then\n\n```\npoetry shell\n```\n\n## Installing from pypi\n\n```bash\npip install high-order-layers-torch\n```\n\nor\n\n```\npoetry add high-order-layers-torch\n```\n\n# Examples\n\n## Simple function approximation\n\nApproximating a simple function using a single input and single output (single layer) with no hidden layers\nto approximate a function using continuous and discontinuous piecewise polynomials (with 5 pieces) and simple\npolynomials and fourier series.  The standard approach using ReLU is non competitive.  To see more complex see\nthe implicit representation page [here](https://github.com/jloveric/high-order-implicit-representation).\n\n![piecewise continuous polynomial](plots/piecewise_continuous.png)\n![piecewise discontinuous polynomial](plots/piecewise_discontinuous.png)\n![polynomial](plots/polynomial.png)\n![fourier series](plots/fourier_series.png)\n\n## XOR : 0.5 for x*y > 0 else -0.5\nSimple XOR problem, the function is discontinuous along the axis and we try and fit that function\n![piecewise discontinuous polynomial](plots/xor_discontinuous.png)\n![piecewise continuous polynomial](plots/xor_continuous.png)\n![polynomial](plots/xor_polynomial.png)\n\n## mnist (convolutional)\n\n```python\npython mnist.py max_epochs=1 train_fraction=0.1 layer_type=continuous n=4 segments=2\n```\n\n## cifar100 (convolutional)\n\n```\npython cifar100.py -m max_epochs=20 train_fraction=1.0 layer_type=polynomial segments=2 n=7 nonlinearity=False rescale_output=False periodicity=2.0 lr=0.001 linear_output=False\n```\n\n## invariant mnist (fully connected)\nWithout polynomial refinement\n```python\npython invariant_mnist.py max_epochs=100 train_fraction=1 layer_type=polynomial n=5 p_refine=False\n```\nwith polynomial refinement (p-refinement)\n```\npython invariant_mnist.py max_epochs=100 train_fraction=1 layer_type=continuous n=2 p_refine=False target_n=5 p_refine=True\n```\n\n## Implicit Representation\n\nAn example of implicit representation can be found [here](https://github.com/jloveric/high-order-implicit-representation)\n\n## Test\nAfter installing and running\n```\npoetry shell\n```\nrun\n```\npytest \n```\n## Reference\n```\n@misc{Loverich2020,\n  author = {Loverich, John},\n  title = {High Order Layers Torch},\n  year = {2020},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{https://github.com/jloveric/high-order-layers-torch}},\n}\n```',
    'author': 'jloverich',
    'author_email': 'john.loverich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
