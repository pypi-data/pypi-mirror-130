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

2. 
    Install spladtool
    ```bash
    pip install spladtool
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

4.  Try out an example training a linear classifier on a dataset
    ```python
    import spladtool.spladtool_reverse as str
    from spladtool.utils import SGD
    import numpy as np


    # We chose a simple classification model with decision boundary being 4x1 - 3x2 > 0
    x = np.random.randn(200, 2)
    y = ((x[:, 0] - 3 * x[:, 1]) > 0).astype(float)

    # define a linear regression module

    np.random.seed(42)

    class MyModel(str.Module):
        def __init__(self):
            super().__init__()
            self.register_param(w1=str.tensor(np.random.randn()))
            self.register_param(w2=str.tensor(np.random.randn()))
            self.register_param(b=str.tensor(np.random.randn()))

        def forward(self, x):
            w1 = self.params['w1'].repeat(x.shape[0])
            w2 = self.params['w2'].repeat(x.shape[0])
            b = self.params['b'].repeat(x.shape[0])
            y = w1 * str.tensor(x[:, 0]) + w2 * str.tensor(x[:, 1]) + b
            return y

    # define loss function and optimizer
    model = MyModel()
    criterion = str.BCELoss()
    opt = SGD(model.parameters(), lr=0.1, momentum=0.9)

    # training
    for epoch in range(100):
        outputs = model(x)
        targets = str.tensor(y)
        loss = criterion(targets, outputs)
        opt.zero_grad()
        loss.backward()
        opt.step()
        print(loss.data)
    ```
