import numpy as np
from collections import defaultdict
from numpy.lib.arraysetops import isin


class ReverseAD:

    node_dict = {}  # Dictionary to store the variables' labels

    def __init__(self, value, local_gradients=[], label=None):
        """

        -- Parameters
        value : the value of the variable
            type: int or float
        local_gradients: the variable's children and corresponding local derivatives
            type: list
        label : variable name
            type: string
        """
        if isinstance(value, float) or isinstance(value, int):
            self.value = value
        else:
            raise TypeError(
                f'Value should be int or float and not {type(value)}')

        if len(local_gradients) == 0:
            self.local_gradients = [(None, 1)]
        else:
            self.local_gradients = local_gradients

        if label is not None:

            ReverseAD.node_dict[self] = label

    def __add__(self, other):
        """
        Perform addition

        -- Parameters
        other : values to be added
            type: int or float or ReverseAD

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(2,label='x')
        >>> y = ReverseAD(3,label='y')
        >>> z = ReverseAD(4,label='z')
        >>> f = ReverseFunctions([x + y, y + z], [x, y, z])
        >>> f.vals
        [5, 7]
        >>> f.ders
        [[1 1 0]
         [0 1 1]]
        >>> f.vars
        ['x', 'y', 'z']
        """
        if isinstance(other, int) or isinstance(other, float):
            return ReverseAD(self.value + other, [(self, 1)])
        elif isinstance(other, ReverseAD):
            value = self.value + other.value
            local_gradients = (
                (self, 1),
                (other, 1)
            )
            return ReverseAD(value, local_gradients)

    def __radd__(self, other):
        """
        Perform reverse addition

        -- Parameters
        other : values to be added
            type: int or float or ReverseAD

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(2,label='x')
        >>> y = ReverseAD(3,label='y')
        >>> f = ReverseFunctions([3.0 + x, x + y], [x, y])
        >>> f.vals
        [5.0, 5]
        >>> f.ders
        [[1 0]
         [1 1]]
        >>> f.vars
        ['x', 'y']
        """
        return self.__add__(other)

    def __mul__(self, other):
        """
        Perform multiplication

        -- Parameters
        other : values to be multiplied to self
            type: int or float or ReverseAD

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(2,label='x')
        >>> y = ReverseAD(3,label='y')
        >>> f = ReverseFunctions([x * 3, x * y, y * x], [x, y])
        >>> f.vals
        [6, 6, 6]
        >>> f.ders
        [[3 0]
         [3 2]
         [3 2]]
        >>> f.vars
        ['x', 'y']
        """
        if isinstance(other, int) or isinstance(other, float):
            return ReverseAD(self.value * other, [(self, other)])
        elif isinstance(other, ReverseAD):
            value = self.value * other.value
            local_gradients = (
                (self, other.value),
                (other, self.value)
            )
            return ReverseAD(value, local_gradients)

    def __rmul__(self, other):
        """
        Perform reverse multiplication

        -- Parameters
        other : values to be multiplied to self
            type: int or float or ReverseAD

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(2,label='x')
        >>> y = ReverseAD(3,label='y')
        >>> f = ReverseFunctions([x * 3, x * y, y * x], [x, y])
        >>> f.vals
        [6, 6, 6]
        >>> f.ders
        [[3 0]
         [3 2]
         [3 2]]
        >>> f.vars
        ['x', 'y']
        """
        return self.__mul__(other)

    def __neg__(self):
        """
        Perform negation

        -- Parameters
        other : values to be divided by self

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(2,label='x')
        >>> z = ReverseAD(2,label='z')
        >>> f = ReverseFunctions([-x / z, x / z], [x, z])
        >>> f.vals
        [-1.0, 1.0]
        >>> f.ders
        [[-0.5  0.5]
         [ 0.5 -0.5]]
        >>> f.vars
        ['x', 'z']
        """
        value = -1 * self.value
        local_gradients = (
            (self, -1),
        )
        return ReverseAD(value, local_gradients)

    def inv(self):
        """
        Perform inversion(Helper Function)
        -- Parameters
        -- Return
        An ReverseAD object with calculated values, variable’s children and local derivatives.
        -- Demo
        >>> x = ReverseAD(2, label='x')
        >>> f = ReverseFunctions([1 / x], [x])
        >>> f.vals
        [0.5]
        >>> f.ders
        [[-0.25]]
        >>> f.vars
        [‘x’]
        """
        value = 1. / self.value
        local_gradients = (
            (self, -1 / self.value**2),
        )
        return ReverseAD(value, local_gradients)

    def __sub__(self, other):
        """
        Perform subtraction

        -- Parameters
        other : values to be subtracted from self
            type: int or float or ReverseAD

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(2,label='x')
        >>> y = ReverseAD(3,label='y')
        >>> f = ReverseFunctions([x - 3.0, x + y], [x, y])
        >>> f.vals
        [-1.0, 5]
        >>> f.ders
        [[1 0]
         [1 1]]
        >>> f.vars
        ['x', 'y']
        """
        return self.__add__(-other)

    def __rsub__(self, other):
        """
        Perform reverse subtraction

        -- Parameters
        other : values from which self is substracted
            type: int or float or ReverseAD

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(2,label='x')
        >>> y = ReverseAD(3,label='y')
        >>> f = ReverseFunctions([3.0 - x, x - y, y - x], [x, y])
        >>> f.vals
        [1.0, -1, 1]
        >>> f.ders
        [[-1  0]
         [ 1 -1]
         [-1  1]]
        >>> f.vars
        ['x', 'y']
        """
        if isinstance(other, int) or isinstance(other, float):
            return ReverseAD(other - self.value, [(self, -1)])
        elif isinstance(other, ReverseAD):
            value = other.value - self.value
            local_gradients = (
                (self, -1),
                (other, 1)
            )
            return ReverseAD(value, local_gradients)

    def __truediv__(self, other):
        """
        Perform true division

        -- Parameters
        other : values to divide self
            type: int or float or ReverseAD

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(2,label='x')
        >>> z = ReverseAD(4,label='z')
        >>> f = ReverseFunctions([x / 2, x / z], [x, z])
        >>> f.vals
        [1.0, 0.5]
        >>> f.ders
        [[ 0.5    0.   ]
         [ 0.25  -0.125]]
        >>> f.vars
        ['x', 'z']
        """
        if isinstance(other, int) or isinstance(other, float):

            return self.__mul__(1/other)
        elif isinstance(other, ReverseAD):
            return self.__mul__(other.inv())

    def __rtruediv__(self, other):
        """
        Perform reverse true division

        -- Parameters
        other : values to be divided by self
            type: int or float or ReverseAD

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(2,label='x')
        >>> z = ReverseAD(4,label='z')
        >>> f = ReverseFunctions([x / 2, x / z, z / x], [x, z])
        >>> f.vals
        [1.0, 0.5, 2.0]
        >>> f.ders
        [[ 0.5    0.   ]
         [ 0.25  -0.125]
         [-1.     0.5  ]]
        >>> f.vars
        ['x', 'z']
        """
        if isinstance(other, int) or isinstance(other, float):
            value = other / self.value
            local_gradients = (
                (self, -other/(self.value ** 2)),
            )
            return ReverseAD(value, local_gradients)
        else:
            return self.__truediv__(other)

    def __pow__(self, other):
        """
        Perform the power of n

        -- Parameters
        other: exponent to which self is raised
            type: int or float or ReverseAD

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(2,label='x')
        >>> z = ReverseAD(2,label='z')
        >>> f = ReverseFunctions([x ** 2, (x + y) ** 2], [x, y])
        >>> f.vals
        [4, 25]
        >>> f.ders
        [[ 4  0]
         [10 10]]
        >>> f.vars
        ['x', 'y']
        """
        if isinstance(other, int) or isinstance(other, float):
            return ReverseAD(self.value ** other, [(self, other * self.value ** (other - 1))])
        elif isinstance(other, ReverseAD):
            value = self.value ** other.value
            local_gradients = (
                (self, other.value * self.value ** (other.value - 1)),
                (other, value * np.log(self.value))
            )
            return ReverseAD(value, local_gradients)

    def __rpow__(self, other):
        """
        Raise a number to the power of self

        -- Parameters
        other : number to be raised
            type: int or float or ReverseAD

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(2,label='x')
        >>> y = ReverseAD(3,label='y')
        >>> f = ReverseFunctions([2 ** x, 2 ** (x + y)], [x, y])
        >>> f.vals
        [4, 32]
        >>> f.ders
        [[2.773, 0]
         [22.181, 22.181]]
        >>> f.vars
        ['x', 'y']
        """
        if isinstance(other, int) or isinstance(other, float):
            value = other ** self.value
            local_gradients = (
                (self, value * np.log(other)),
            )
            return ReverseAD(value, local_gradients)
        else:
            return self.__pow__(other)

    def sin(self):
        """
        Perform the sine

        -- Parameters

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(np.pi / 2,label='x')
        >>> y = ReverseAD(np.pi / 2,label='y')
        >>> f = ReverseFunctions([x.sin(), (x + y).sin()], [x, y])
        >>> f.vals
        [1.0, 0]
        >>> f.ders
        [[0, 0]
         [-1.0, -1.0]]
        >>> f.vars
        ['x', 'y']
        """

        value = np.sin(self.value)
        local_gradients = (
            (self, np.cos(self.value)),
        )
        return ReverseAD(value, local_gradients)

    def cos(self):
        """
        Perform the cosine

        -- Parameters

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(np.pi / 2,label='x')
        >>> y = ReverseAD(np.pi / 2,label='y')
        >>> f = ReverseFunctions([x.cos(), (x + y).cos()], [x, y])
        >>> f.vals
        [0, -1.0]
        >>> f.ders
        [[-1.0, 0]
         [0, 0]]
        >>> f.vars
        ['x', 'y']
        """
        value = np.cos(self.value)
        local_gradients = (
            (self, -np.sin(self.value)),
        )
        return ReverseAD(value, local_gradients)

    def tan(self):
        """
        Perform the tangent

        -- Parameters

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(np.pi,label='x')
        >>> y = ReverseAD(np.pi,label='y')
        >>> f = ReverseFunctions([x.tan(), (x + y).tan()], [x, y])
        >>> f.vals
        [0, 0]
        >>> f.ders
        [[1.0, 0]
         [1.0, 1.0]]
        >>> f.vars
        ['x', 'y']
        """
        if (self.value / np.pi - 0.5) % 1 == 0.00:
            raise ValueError("Tangent cannot be applied to this value")
        value = np.tan(self.value)
        local_gradients = (
            (self, 1 / np.power(np.cos(self.value), 2)),
        )
        return ReverseAD(value, local_gradients)

    def exp(self):
        """
        Perform the exponential

        -- Parameters

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(2,label='x')
        >>> y = ReverseAD(3,label='y')
        >>> f = ReverseFunctions([x.exp(), y.exp()], [x, y])
        >>> f.vals
        [7.389, 20.086] 
        >>> f.ders
        [[7.389, 0]
         [0, 20.1]] 
        >>> f.vars
        ['x', 'y']
        """

        value = np.exp(self.value)
        local_gradients = (
            (self, np.exp(self.value)),
        )
        return ReverseAD(value, local_gradients)

    def ln(self):
        """
        Perform the natural logarithm 

        -- Parameters

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(2,label='x')
        >>> y = ReverseAD(np.exp(1),label='y')
        >>> f = ReverseFunctions([x.ln(), y.ln()], [x, y])
        >>> f.vals
        [0.693, 1.0]]
        >>> f.ders
        [[0.5, 0]
         [0, 0.368]] 
        >>> f.vars
        ['x', 'y']
        """
        if self.value <= 0:
            raise ValueError("Natural log cannot be applied to this value")
        value = np.log(self.value)
        local_gradients = (
            (self, 1. / self.value),
        )
        return ReverseAD(value, local_gradients)

    def ln_base(self, base):
        """
        Perform the logarithm with a specific base

        -- Parameters
        base: number to be raised
            type: int

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(8,label='x')
        >>> y = ReverseAD(np.exp(1), label='y')
        >>> f = ReverseFunctions([x.ln_base(2), y.ln_base(np.exp(1))], [x, y])
        >>> f.vals
        [3.0, 1.0]]
        >>> f.ders
        [[0.180, 0]
         [0, 0.368]] 
        >>> f.vars
        ['x', 'y']
        """
        if base == 0 or base == 1:
            raise ValueError("Base cannot be this value")
        return self.ln() / np.log(base)

    def sinh(self):
        """
        Perform the hyperbolic sine

        -- Parameters

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(2,label='x')
        >>> y = ReverseAD(3,label='y')
        >>> f = ReverseFunctions([x.sinh(), y.sinh()], [x, y])
        >>> f.vals
        [[3.627], [10.018]] 
        >>> f.ders
        [[3.762, 0]
         [0, 10.068]]
        >>> f.vars
        ['x', 'y']
        """
        value = np.sinh(self.value)
        local_gradients = (
            (self, np.cosh(self.value)),
        )
        return ReverseAD(value, local_gradients)

    def cosh(self):
        """
        Perform the hyperbolic cosine

        -- Parameters

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(2,label='x')
        >>> y = ReverseAD(3,label='y')
        >>> f = ReverseFunctions([x.cosh(), y.cosh()], [x, y])
        >>> f.vals
        [[3.627], [10.018]] 
        >>> f.ders
        [[3.627, 0]
         [0, 10.018]]
        >>> f.vars
        ['x', 'y']
        """
        value = np.cosh(self.value)
        local_gradients = (
            (self, np.sinh(self.value)),
        )
        return ReverseAD(value, local_gradients)

    def tanh(self):
        """
        Perform the hyperbolic tangent

        -- Parameters

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(2,label='x')
        >>> y = ReverseAD(3,label='y')
        >>> f = ReverseFunctions([x.tanh(), y.tanh()], [x, y])
        >>> f.vals
        [0.964, 0.995]
        >>> f.ders
        [[0.071, 0]
         [0, 0.010]]
        >>> f.vars
        ['x', 'y']
        """
        value = np.tanh(self.value)
        local_gradients = (
            (self, 1 - value ** 2),
        )
        return ReverseAD(value, local_gradients)

    def arcsin(self):
        """
        Perform the arcsine

        -- Parameters

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(0.5,label='x')
        >>> y = ReverseAD(-0.5,label='y')
        >>> f = ReverseFunctions([x.arcsin(), y.arcsin()], [x, y])
        >>> f.vals
        [0.524], -0.524]
        >>> f.ders
        [[1.155, 0]
         [0, 1.155]]
        >>> f.vars
        ['x', 'y']
        """
        if self.value <= -1 or self.value >= 1:
            raise ValueError("Arcsine cannot be applied to this value")
        value = np.arcsin(self.value)
        local_gradients = (
            (self, 1 / (1 - self.value ** 2) ** 0.5),
        )
        return ReverseAD(value, local_gradients)

    def arccos(self):
        """
        Perform the arccosine

        -- Parameters

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(0.5,label='x')
        >>> y = ReverseAD(-0.5,label='y')
        >>> f = ReverseFunctions([x.arccos(), y.arccos()], [x, y])
        >>> f.vals
        [1.047,2.094]
        >>> f.ders
        [[-1.155, 0]
         [0, -1.155]]
        >>> f.vars
        ['x', 'y']
        """
        if self.value <= -1 or self.value >= 1:
            raise ValueError("Arccosine cannot be applied to this value")
        value = np.arccos(self.value)
        local_gradients = (
            (self, -1 / (1 - self.value ** 2) ** 0.5),
        )
        return ReverseAD(value, local_gradients)

    def arctan(self):
        """
        Perform the arctangent

        -- Parameters

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(0.5,label='x')
        >>> y = ReverseAD(-0.5,label='y')
        >>> f = ReverseFunctions([x.arctan(), y.arctan()], [x, y])
        >>> f.vals
        [0.464, -0.464]
        >>> f.ders
        [[0.8, 0]
         [0, 0.8]]
        >>> f.vars
        ['x', 'y']
        """
        value = np.arctan(self.value)
        local_gradients = (
            (self, 1 / (1 + self.value ** 2)),
        )
        return ReverseAD(value, local_gradients)

    def logistic(self):
        """
        Perform the logistic

        -- Parameters

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(0.5,label='x')
        >>> y = ReverseAD(-0.5,label='y')
        >>> f = ReverseFunctions([x.logistic(), y.logistic()], [x, y])
        >>> f.vals
        [0.622, 0.378]
        >>> f.ders
        [[0.235, 0]
         [0, 0.235]]
        >>> f.vars
        ['x', 'y']
        """
        value = 1 / (1 + np.exp(-self.value))
        local_gradients = (
            (self, value * (1 - value)),
        )
        return ReverseAD(value, local_gradients)

    def sqrt(self):
        """
        Perform the square root 

        -- Parameters

        -- Return
        An ReverseAD object with calculated values, variable's children and local derivatives.

        -- Demo

        >>> x = ReverseAD(4,label='x')
        >>> y = ReverseAD(25,label='y')
        >>> f = ReverseFunctions([x.sqrt(), y.sqrt()], [x, y])
        >>> f.vals
        [2.0, 5.0]
        >>> f.ders
        [[0.25 0.  ]
         [0.   0.1 ]]
        >>> f.vars
        ['x', 'y']
        """
        return self.__pow__(1/2)

    def get_gradients(self):
        """ Compute the first derivatives of `variable`
        with respect to child variables.
        """
        gradients = defaultdict(lambda: 0)

        def compute_gradients(self, path_value):

            for child_variable, local_gradient in self.local_gradients:
                # print(child_variable.value)
                # "Multiply the edges of a path":
                value_of_path_to_child = path_value * local_gradient
                # "Add together the different paths":
                if child_variable == None:
                    # Escape condition (reach leaf nodes)
                    # gradients[self] += 1 * value_of_path_to_child
                    return
                else:
                    gradients[child_variable] += value_of_path_to_child

            # recurse through graph:
                compute_gradients(child_variable, value_of_path_to_child)

        compute_gradients(self, path_value=1)
        print(gradients)
        # (path_value=1 is from `variable` differentiated w.r.t. itself)

        return gradients


class ReverseFunctions():
    def __init__(self, functions, variables=[]):
        """
        -- Parameters
        functions : a list of evaluated functions 
            type: list of ReverseAD object or int (float)
        variables: a list of used variable used in the function
            type: list of reverseAD (input variable)

        """

        values = []
        for function in functions:
            # if function is of type ReverseAD
            try:
                values.append(function.value)
            # if function is a constant number
            except AttributeError:
                values.append(function)

        all_der = []
        for function in functions:
            curr_der = []
            # if function is not constant
            try:
                curr_grad = function.get_gradients()
                for var in variables:
                    # if a variable is not used in a function
                    if var not in curr_grad:
                        curr_der.append(0)
                        continue
                    # add the derivate of a variable stored in the curr_grad (dictionary)
                    curr_der.append(curr_grad[var])
            # if function is constant
            except:
                for var in variables:
                    curr_der.append(0)

            all_der.append(curr_der)

        # variable_names = [print_var_name(var) for var in variables]
        variable_names = [ReverseAD.node_dict[var] for var in variables]
        self.vals = values
        self.vars = variable_names
        self.ders = np.array(all_der)


# x = ReverseAD(4, label="x")
# y = ReverseAD(3, label="y")
# # z = ReverseAD(4, label="z")
# print(x)
# print(y)
# z = x * (x + y)
# # f = ReverseFunctions([x * (x + y)], [x, y])
# print(z.value)
# print(z.get_gradients())

# print(f.vars)
