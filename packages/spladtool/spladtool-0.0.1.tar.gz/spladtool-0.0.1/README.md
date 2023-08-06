## Introduction

With the rapid development of deep learning, auto differentiation has become an indispensable part of multiple optimization algorithms like gradient descent. Numerical means such as Newton's Method and finite-difference method is useful in some situations, we desire to compute the analytical solutions by applying chain rules with our automatic differentiation SPLADTool (**S**imple **P**ytorch-**L**ike **A**uto **D**ifferentiation **Tool**kit), which will be faster and more accurate than numerical methods.

## Usage

1. Create a virtual environment: Conda
    ```bash
    conda create --name spladtool_env python
    ```
    
   Activate the environment:
   ```bash
   conda activate spladtool_env
   ```
   
   Deactivate the envrionment after use:
   ```bash
   conda deactivate
   ```

2. Install numpy 
    ```bash
    pip install numpy
    ```
    Install spladtool
    ```bash
    pip install -i https://test.pypi.org/simple/ spladtool
    ``` 

3. Try out an example from `test.py` on arithmetic functions:

   ```python
   import spladtool.spladtool_forward as st

   x = st.tensor([[1., 2.], [3., 4.]])
           
   # Define output functions y(x) and z(x)
   y = 2 * x + 1
   z = - y / (x ** 3)
   w = st.cos((st.exp(z) + st.exp(-z)) / 2)
   
   # Print out the values calculated by our forward mode automatic differentiation SPLADTool
   print('x : ', x)
   print('y : ', y)
   print('y.grad : ', y.grad)
   print('z: ', z)
   print('z.grad: ', z.grad)
   print('w: ', w)
   print('w.grad: ', w.grad)
   ```

## Implementation

### Data Structures

#### Tensor

The core data structure here is the `spladtool.Tensor`, which contains the value vector (that will be represented by a `numpy.ndarray`) and corresponding gradient. 

In the reverse mode, we need two more attributes or member variables to keep record of the graph dependency: `Tensor.dependency` tracks the dependent tensor and `Tensor.layer` will store the layer or the operation used to attain this tensor. We will explain further how they are used. In the reverse mode, we also add a member function called `Tensor.backward()`, which will automatically call the `backward` method of `Tensor.layer` with arguments being `Tensor.dependency` to achieve reverse propagation.

#### Layer

A layer is defined as a basic operations, i.e. sum, product, division, sine function, etc.

All layer classes inherit from a base class called `Layer`. For the forward mode, the member function `Layer.forward()` computes the evaluation and gradients altogether. In the reverse mode, `Layer.forward()` will only handle the evaluation, while `Layer.reverse()` will handle the gradients computation.

### Functional APIs

We wrap up our implementations of operations in functional APIs which can be found in `spladtool_forward/spladtool_forward.py`.

We also add dunders or magic functions to `Tensor` class so that basic operators can be used on them.

### Supported Operations(**New**)
- Basic Operations: Add, Substract, Power, Negation, Product, Division
- Analytical functions: trignomical, exponential, logarithm

### Python Typing

To make sure the type is  correct, we add python typing to each of the operation classes and functional APIs to make sure the library will raise proper exceptions when encountered with unsupported operations.

## Broader Impact and Inclusivity Statement

### Broader Impact

- Our implementation of automatic differentiation provides a fast and accurate way of calculating derivatives. Our SPLAD Tool package is handy and straightforward to apply in many fields. When handling large-scale computation, utilizing our package will relieve calculation workload and avoid computational errors. Besides, the package is also helpful in dealing with a wide range of mathematical problems. For example, by adding the implementation of loss functions, we were able to apply our spladtool_reverse to construct a simple data classifier, which is demonstrated in detailed under the exmaple directory. Furthermore, our package can also be used to construct root-finding algorithms based on Newton's method. 


- While our automatic differentiation package provides many conveniences and can be applied widely in many fields, it might also be misused in some conditions. As a convenient tool for calculating derivatives automatically, our package might hinder students or beginners from thoroughly learning and understanding the basic theory behind the mechanism. This misuse contradicts our original intentions of helping people study and work more efficiently.


### Software Inclusivity

- In order to make our package to be as inclusive as possible, we intend to publish our package as an open-source resource online. By distributing over Github and PyPI, we allow people from all kinds of backgrounds to be able to download, use and coordinate with us. Furthermore, we also encourage other developers from all communities to contribute to our codebase by enabling people to create new pull requests, leave comments in our repository on Github. All of our group members will continue monitoring new comments and pull requests and schedule meetings at any time to discuss further improvement and optimization if needed.


- Furthermore, to eliminate the barrier to underrepresented groups, we expect to implement new features in the future concerning different communities respectively. For example, to help eliminate the language barrier to non-native English speakers, we expect to provide detailed instructions in multiple languages other than English. Besides, if possible, we may build a GUI that can visualize the trace of automatic differentiation to help users better understand the working flow of automatic differentiation.


## Future Features

For our possible future features, we intend to add data structures and new methods in our implmentation to support matrix multiplication. Besides, we may apply our package to solve more complex problems, like neural network with mutiple layers.


## Licensing

This project will be licensed using the traditional MIT license due to several factors. 

- We will be using code from the NumPy library which the MIT license coincides with. 
- As of now, we do not foresee having to deal with any patents or any other dependencies. 
- Since this project won’t contain an abundance of novel code (and, therefore, could be duplicated quite easily), we don’t mind letting others use it as they please. 
- Due to the small scale of the project, we are hoping to use a license which is similarly simple. The MIT license is the best match for our interests outlined above. 