import numpy as np


class AutoDiff():
    def __init__(self, val, der=1.0, label=""):
        """
        Constructs an AD object

        -- Parameters
        val : value of input variables, the input value can be int,float or numpy arrays, but later will be converted to two-dimensional array
            type: two-dimensional array
        der :  derivatives with respect to each variable, default is set to 1.0
            type: two-dimensional array
        label : variable name, default is set to "".
            type: list

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> a = 2.0  # Value to evaluate at
        >>> x = AutoDiff(a, der=1, label="x")
        """

        # convert val to two-dimensional array
        if isinstance(val, float) or isinstance(val, int):
            value = np.array(val, dtype=np.float64).reshape(1, -1)
        elif isinstance(val, np.ndarray):
            value = val.reshape(val.shape[0], 1)
        else:
            raise TypeError(
                f'Value should be int or float and not {type(val)}')

        self.val = np.array(value, dtype=np.float64)

        # convert der to two-dimensional array
        if isinstance(der, float) or isinstance(der, int):
            der = np.array(der, dtype=np.float64).reshape(1, -1)
        elif isinstance(der, np.ndarray) and der.shape[0] == 1:
            der = der.reshape(der.shape[0], -1)
        elif isinstance(der, np.ndarray) and len(der.shape) == 2:
            der = der
        self.der = np.array(der, dtype=np.float64)

        # label needed to be stored in list
        if isinstance(label, list):
            self.label = label
        else:
            self.label = [label]

    def __add__(self, other):
        """
        Perform addition

        -- Parameters
        other : values to be added
            type: int or AutoDiff

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(2.0, der=1, label="x")
        >>> y = AutoDiff(3.0, der=1, label="y")
        >>> z = AutoDiff(4.0, der=1, label="z")
        >>> f = ForwardFunctions([x + y, y + z])
        >>> f.values
        [[5.0], [7.0]] 
        >>> f.jacobians
        [1.0, 1.0, 0], [0, 1.0, 1.0]]
        >>> f.labels
        ['x', 'y', 'z']

        """
        if isinstance(other, AutoDiff):
            # update value
            new_val = self.val + other.val

            new_labels = self.label.copy()
            other_labels = other.label.copy()
            new_der = self.der.copy()
            other_der = other.der.copy()

            for i, other_name in enumerate(other_labels):
                # if this varibale is used in previous calculation, for example, x + y + x, x used twice
                if other_name in new_labels:
                    # update directly on the original derivative
                    index_1 = new_labels.index(other_name)
                    new_der[:, index_1] = new_der[:, index_1] + other_der[:, i]

                # if variable never used before
                else:
                    # add a new column onto existing derivative matrix
                    new_der = np.concatenate(
                        (new_der, other.der[:, i].reshape(-1, 1)), axis=1)
                    # update variable list
                    new_labels.append(other_name)

            return AutoDiff(new_val, new_der, new_labels)
        else:
            return AutoDiff(self.val + other, self.der, self.label)

    def __radd__(self, other):
        """
        Perform reverse addition

        -- Parameters
        other : values to be added
            type: int or AutoDiff

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(2, der=1, label="x")
        >>> y = AutoDiff(3, der=1, label="y")
        >>> f = ForwardFunctions([3.0 + x, x + y])
        >>> f.values
        [[5.0], [5.0]] 
        >>> f.jacobians
        [[1.0, 0], [1.0, 1.0]]
        >>> f.labels
        ['x', 'y']

        """
        return self.__add__(other)

    def __sub__(self, other):
        """
        Perform subtraction

        -- Parameters
        other : values to be subtracted from self
            type: int or AutoDiff

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(2, der=1, label="x")
        >>> y = AutoDiff(3, der=1, label="y")
        >>> f = ForwardFunctions([x - 3.0, x + y])
        >>> f.values
        [[-1.0], [5.0]]
        >>> f.jacobians
        [[1.0, 0], [1.0, 1.0]]
        >>> f.labels
        ['x', 'y']

        """
        return self.__add__(-other)

    def __rsub__(self, other):
        """
        Perform reverse subtraction

        -- Parameters
        other : values from which self is substracted
            type: int or AutoDiff

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(2, der=1, label="x")
        >>> y = AutoDiff(3, der=1, label="y")
        >>> f = ForwardFunctions([3.0 - x, x + y])
        >>> f.values
        [[1.0], [5.0]]
        >>> f.jacobians
        [[-1.0, 0], [1.0, 1.0]]
        >>> f.labels
        ['x', 'y']
        """
        return -(self.__sub__(other))

    def __mul__(self, other):
        """
        Perform multiplication

        -- Parameters
        other : values to be multiplied to self
            type: int or AutoDiff

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(2, der=1, label="x")
        >>> y = AutoDiff(3, der=1, label="y")
        >>> f = ForwardFunctions([x * 3, x * y, y * x])
        >>> f.values
        [[6.0], [6.0], [6.0]]
        >>> f.jacobians
        [[3.0, 0], [3.0, 2.0], [3.0, 2.0]]
        >>> f.labels
        ['x', 'y']

        """

        if isinstance(other, AutoDiff):
            label1 = self.label.copy()
            label2 = other.label.copy()

            # merge all used labels by the order of appearance
            all_lables = label1 + \
                [label for label in label2 if label not in label1]

            der1 = self.der.copy()
            der2 = other.der.copy()
            val1 = self.val.copy()
            val2 = other.val.copy()

            # update value
            new_val = val1 * val2

            new_der = self.der.copy()

            for label in all_lables:
                # label only used in left side
                if label in label1 and label not in label2:
                    index = label1.index(label)
                    # update the existing derivative
                    new_der[:, index] = der1[:, index] * val2
                # label only used in right side
                elif label not in label1 and label in label2:
                    orig_index = label2.index(label)
                    tmp_der = der2[:, orig_index] * self.val
                    # add a new column to derivative
                    new_der = np.concatenate((new_der, tmp_der), axis=1)
                # label in both side
                elif label in label1 and label in label2:
                    index1 = label1.index(label)
                    index2 = label2.index(label)
                    # update existing derivative
                    new_der[:, index1] = self.val.copy() * \
                        other.der[:, index2] + \
                        self.der[:, index1] * other.val

            return AutoDiff(new_val, new_der, all_lables)

        elif isinstance(other, int) or isinstance(other, float):
            return AutoDiff(self.val * other, self.der * other, self.label)

    def __rmul__(self, other):
        """
        Perform reverse multiplication

        -- Parameters
        other : values to be multiplied to self
            type: int or AutoDiff

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(2, der=1, label="x")
        >>> y = AutoDiff(3, der=1, label="y")
        >>> f = ForwardFunctions([x * 3, x * y, y * x])
        >>> f.values
        [[6.0], [6.0], [6.0]] 
        >>> f.jacobians
        [[3.0, 0], [3.0, 2.0], [2.0, 3.0]]
        >>> f.labels
        ['x', 'y']


        """
        return self.__mul__(other)

    def __truediv__(self, other):
        """
        Perform true division

        -- Parameters
        other : values to divide self
            type: int or AutoDiff

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(2, der=1, label="x")
        >>> y = AutoDiff(3, der=1, label="y")
        >>> z = AutoDiff(4, der=1, label="z")
        >>> f = ForwardFunctions([x / 2, x / z])
        >>> f.values
        [[1.0], [0.5]]
        >>> f.jacobians
        [[0.5, 0], [0.25, -0.125]]
        >>> f.labels
        ['x', 'z']
        """

        if isinstance(other, AutoDiff):
            if other.val == 0:
                raise ZeroDivisionError

            label1 = self.label.copy()
            label2 = other.label.copy()

            # merge all used labels by the order of appearance
            all_lables = all_lables = label1 + \
                [label for label in label2 if label not in label1]

            der1 = self.der.copy()
            der2 = other.der.copy()
            val1 = self.val.copy()
            val2 = other.val.copy()

            # update value
            new_val = val1 / val2

            # new derivative
            new_der = self.der.copy()

            for label in all_lables:
                # label only used in left side
                if label in label1 and label not in label2:
                    index = label1.index(label)
                    new_der[:, index] = der1[:, index] / val2

                # label only used in right side
                elif label not in label1 and label in label2:
                    orig_index = label2.index(label)
                    tmp_der = -self.val * \
                        other.der[:, orig_index]/(other.val ** 2)
                    new_der = np.concatenate((new_der, tmp_der), axis=1)

                # label used in both sides
                elif label in label1 and label in label2:
                    index1 = label1.index(label)
                    index2 = label2.index(label)
                    tmp_der = (self.der[:, index1] * other.val - other.der[:,
                                                                           index2] * self.val) / other.val ** 2
                    new_der[:, index1] = tmp_der

            return AutoDiff(new_val, new_der, all_lables)

        elif isinstance(other, int) or isinstance(other, float):
            if other == 0:
                raise ZeroDivisionError
            new_val = self.val / other
            new_der = self.der / other
        return AutoDiff(new_val, new_der, self.label)

    def __rtruediv__(self, other):
        """
        Perform reverse true division

        -- Parameters
        other : values to be divided by self
            type: int or AutoDiff

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(2, der=1, label="x")
        >>> z = AutoDiff(2, der=1, label="z")
        >>> f = ForwardFunctions([x / 2, x / z, z / x])
        >>> f.values
        [[1.0], [1.0], [1.0]]
        >>> f.jacobians
        [[-0.5, 0], [0.5, -0.5], [0.5, -0.5]]
        >>> f.labels
        ['x', 'z']

        """
        if self.val == 0:
            raise ZeroDivisionError

        new_val = other / self.val
        new_der = (-other/(self.val ** 2)) * self.der
        return AutoDiff(new_val, new_der, self.label)

    def __neg__(self):
        """
        Perform negation

        -- Parameters

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(2, der=1, label="x")
        >>> z = AutoDiff(2, der=1, label="z")
        >>> f = ForwardFunctions([-x / z, x / z])
        >>> f.values
        [[-1.0], [1.0]] 
        >>> f.jacobians
        [[-0.5, 0.5], [0.5, -0.5]]
        >>> f.labels
        ['x', 'z']

        """
        return AutoDiff(-self.val, -self.der, self.label)

    def __pow__(self, other):
        """
        Perform the power of n

        -- Parameters
        other : exponent to which self is raised
            type: int or AutoDiff

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(2, der=1, label="x")
        >>> y = AutoDiff(3, der=1, label="y")
        >>> f = ForwardFunctions([x ** 2, (x + y) ** 2])
        >>> f.values
        [[4.0], [25.0]]
        >>> f.jacobians
        [[4.0, 0], [10.0, 10.0]]
        >>> f.labels
        ['x', 'y']

        """
        if isinstance(other, float) or isinstance(other, int):

            if other < 0 and self.val == 0:
                raise ZeroDivisionError

            if other < 1 and self.val < 0:
                raise
            new_val = self.val ** other
            new_der = other * self.val ** (other-1) * self.der
            return AutoDiff(new_val, new_der, self.label)

        if isinstance(other, AutoDiff):
            # update value
            base_val = self.val.copy()
            power_val = other.val.copy()
            new_val = base_val ** power_val

            # update derivative
            base_der = self.der.copy()
            power_der = other.der.copy()
            new_der = self.der.copy()

            labels_1 = self.label.copy()
            labels_2 = other.label.copy()
            # merge all labels and keep the original order
            all_labels = labels_1 + \
                [name for name in labels_2 if name not in labels_1]

            for i, name in enumerate(all_labels):
                # label only used in left side
                if name in labels_1 and name not in labels_2:
                    index_1 = labels_1.index(name)
                    new_der[:, index_1] = base_der[:, index_1] * \
                        power_val * (base_val ** (power_val - 1))
                # label only used in right side
                elif name not in labels_1 and name in labels_2:
                    index_2 = labels_2.index(name)
                    orig_der = power_der[:, index_2]
                    updated_der = orig_der * \
                        (base_val ** power_val) * np.log(base_val)
                    new_der = np.concatenate((new_der, updated_der), axis=1)

            return AutoDiff(new_val, new_der, all_labels)

    def __rpow__(self, other):
        """
        Raise a number to the power of self

        -- Parameters
        other : number to be raised

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(2, der=1, label="x")
        >>> y = AutoDiff(3, der=1, label="y")
        >>> f = ForwardFunctions([2 ** x, 2 ** (x + y)])
        >>> f.values
        [[4.0], [32.0]]
        >>> f.jacobians
        [[2.773, 0], [22.181, 22.181]] 
        >>> f.labels
        ['x', 'y']

        """
        if other == 0 and self.val < 0:
            raise ZeroDivisionError
        new_val = other ** self.val
        new_der = np.log(other) * new_val * self.der

        return AutoDiff(new_val, new_der, self.label)

    def sin(self):
        """
        Perform the sine

        -- Parameters

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(np.pi / 2, der=1, label="x")
        >>> y = AutoDiff(np.pi / 2, der=1, label="y")
        >>> f = ForwardFunctions([x.sin(), (x + y).sin()])
        >>> f.values
        [[1.0], [0]]
        >>> f.jacobians
        [[0, 0], [-1.0, -1.0]]
        >>> f.labels
        ['x', 'y']

        """
        new_val = np.sin(self.val)
        new_der = np.cos(self.val) * self.der

        return AutoDiff(new_val, new_der, self.label)

    def cos(self):
        """
        Perform the cosine

        -- Parameters

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(np.pi / 2, der=1, label="x")
        >>> y = AutoDiff(np.pi / 2, der=1, label="y")
        >>> f = ForwardFunctions([x.cos(), (x + y).cos()])
        >>> f.values
        [[0], [-1.0]]
        >>> f.jacobians
        [[-1.0, 0], [0, 0]]
        >>> f.labels
        ['x', 'y']

        """
        new_val = np.cos(self.val)
        new_der = -np.sin(self.val) * self.der
        return AutoDiff(new_val, new_der, self.label)

    def tan(self):
        """
        Perform the tagent

        -- Parameters

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(np.pi, der=1, label="x")
        >>> y = AutoDiff(np.pi, der=1, label="y")
        >>> f = ForwardFunctions([x.tan(), (x + y).tan()])
        >>> f.values
        [[0], [0]]
        >>> f.jacobians
        [[1.0, 0], [1.0, 1.0]]
        >>> f.labels
        ['x', 'y']

        """
        if (self.val / np.pi - 0.5) % 1 == 0.00:
            raise ValueError("Tangent cannot be applied to this value")
        new_val = np.tan(self.val)
        new_der = np.multiply(1 / np.power(np.cos(self.val), 2), self.der)
        return AutoDiff(new_val, new_der, self.label)

    def sinh(self):
        """
        Perform the hyperbolic sine

        -- Parameters

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(2, der=1, label="x")
        >>> y = AutoDiff(3, der=1, label="y")
        >>> f = ForwardFunctions([x.sinh(), y.sinh()])
        >>> f.values
        [[3.627], [10.018]] 
        >>> f.jacobians
        [[3.762, 0], [0, 10.068]]
        >>> f.labels
        ['x', 'y']

        """

        new_val = np.sinh(self.val)
        new_der = np.cosh(self.val) * self.der
        return AutoDiff(new_val, new_der, self.label)

    def cosh(self):
        """
        Perform the hyperbolic cosine

        -- Parameters

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(2, der=1, label="x")
        >>> y = AutoDiff(3, der=1, label="y")
        >>> f = ForwardFunctions([x.cosh(), y.cosh()])
        >>> f.values
        [[3.762], [10.068]]
        >>> f.jacobians
        [[3.627, 0], [0, 10.018]]
        >>> f.labels
        ['x', 'y']

        """
        new_val = np.cosh(self.val)
        new_der = np.sinh(self.val) * self.der
        return AutoDiff(new_val, new_der, self.label)

    def tanh(self):
        """
        Perform the hyperbolic tangent

        -- Parameters

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(2, der=1, label="x")
        >>> y = AutoDiff(3, der=1, label="y")
        >>> f = ForwardFunctions([x.tanh(), y.tanh()])
        >>> f.values
        [[0.964], [0.995]]
        >>> f.jacobians
        [[0.071, 0], [0, 0.010]]
        >>> f.labels
        ['x', 'y']

        """
        new_val = np.tanh(self.val)
        new_der = 1 - new_val ** 2
        return AutoDiff(new_val, new_der, self.label)

    def arcsin(self):
        """
        Perform the arcsine

        -- Parameters

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(0.5, der=1, label="x")
        >>> y = AutoDiff(-0.5, der=1, label="y")
        >>> f = ForwardFunctions([x.arcsin(), y.arcsin()])
        >>> f.values
        [[0.524], [-0.524]]
        >>> f.jacobians
        [[1.155, 0], [0, 1.155]]
        >>> f.labels
        ['x', 'y']
        """

        if (self.val <= -1).any() or (self.val >= 1).any():
            raise ValueError("Arcsine cannot be applied to this value")
        new_val = np.arcsin(self.val)
        new_der = self.der / ((1 - self.val ** 2) ** 0.5)
        return AutoDiff(new_val, new_der, self.label)

    def arccos(self):
        """
        Perform the arccosine

        -- Parameters

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(0.5, der=1, label="x")
        >>> y = AutoDiff(-0.5, der=1, label="y")
        >>> f = ForwardFunctions([x.arccos(), y.arccos()])
        >>> f.values
        [[1.047], [2.094]]
        >>> f.jacobians
        [[-1.155, 0], [0, -1.155]]
        >>> f.labels
        ['x', 'y']
        """

        if (self.val <= -1).any() or (self.val >= 1).any():
            raise ValueError("Arccosine cannot be applied to this value")
        new_val = np.arccos(self.val)
        new_der = -self.der / ((1 - self.val ** 2) ** 0.5)
        return AutoDiff(new_val, new_der, self.label)

    def arctan(self):
        """
        Perform the arctangent

        -- Parameters

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(0.5, der=1, label="x")
        >>> y = AutoDiff(-0.5, der=1, label="y")
        >>> f = ForwardFunctions([x.arctan(), y.arctan()])
        >>> f.values
        [[0.464], [-0.464]]
        >>> f.jacobians
        [[0.8, 0], [0, 0.8]]
        >>> f.labels
        ['x', 'y']
        """

        new_val = np.arctan(self.val)
        new_der = self.der / (1 + self.val ** 2)
        return AutoDiff(new_val, new_der, self.label)

    def logistic(self):
        """
        Perform the logistic

        -- Parameters

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(0.5, der=1, label="x")
        >>> y = AutoDiff(-0.5, der=1, label="y")
        >>> f = ForwardFunctions([x.logistic(), y.logistic()])
        >>> f.values
        [[0.622], [0.5]]
        >>> f.jacobians
        [[0.235, 0], [0, 0.25]]
        >>> f.labels
        ['x', 'y']
        """

        new_val = 1 / (1 + np.exp(-self.val))
        new_der = new_val * (1 - new_val) * self.der
        return AutoDiff(new_val, new_der, self.label)

    def sqrt(self):
        """
        Perform the square root 

        -- Parameters

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(4, der=1, label="x")
        >>> y = AutoDiff(25, der=1, label="y")
        >>> f = ForwardFunctions([x.sqrt(), y.sqrt()])
        >>> f.values
        [[2.0], [5.0]] 
        >>> f.jacobians
        [[0.25, 0], [0, 0.1]]
        >>> f.labels
        ['x', 'y']
        """

        return self.__pow__(1/2)

    def ln(self):
        """
        Perform the natural logarithm 

        -- Parameters

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(2, der=1, label="x")
        >>> y = AutoDiff(np.exp(1), der=1, label="y")
        >>> f = ForwardFunctions([x.ln(), y.ln()])
        >>> f.values
        [[0.693], [1.0]]
        >>> f.jacobians
        [[0.5, 0], [0, 0.368]] 
        >>> f.labels
        ['x', 'y']
        """

        if (self.val <= 0).any():
            raise ValueError("Natural log cannot be applied to this value")

        new_val = np.log(self.val)
        new_der = 1 / self.val * self.der
        return AutoDiff(new_val, new_der, self.label)

    def ln_base(self, base):
        """
        Perform the logarithm with a specific base

        -- Parameters

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(8, der=1, label="x")
        >>> y = AutoDiff(np.exp(1), der=1, label="y")
        >>> f = ForwardFunctions([x.ln_base(2), y.ln_base(np.exp(1))])
        >>> f.values
        [[3.0], [1.0]]
        >>> f.jacobians
        [[0.180, 0], [0, 0.368]] 
        >>> f.labels
        ['x', 'y']
        """
        if base == 0:
            raise ValueError("Base cannot be zero")
        return self.ln() / np.log(base)

    def exp(self):
        """
        Perform the exponential

        -- Parameters

        -- Return
        An AD object with calculated values, derivatives and variable labels.

        -- Demo

        >>> x = AutoDiff(2, der=1, label="x")
        >>> y = AutoDiff(3, der=1, label="y")
        >>> f = ForwardFunctions([x.exp(), y.exp()])
        >>> f.values
        [[7.389], [20.086]] 
        >>> f.jacobians
        [[7.389, 0], [0, 20.1]] 
        >>> f.labels
        ['x', 'y']

        """

        return self.__rpow__(np.exp(1))


class ForwardFunctions():
    def __init__(self, functions, labels=None):
        values, jacobians, labels = [], [], []
        # collect all possible labels used in different functions
        for function in functions:
            # when the function use some variables, add them it
            try:
                labels.append(function.label)
            # when the function is constant number, skip it, since it doesn't contribute any new variable
            except:
                continue

        # when at least function is non-constant
        try:
            unique_labels = list(
                set(np.array(np.concatenate(labels, axis=0))))
        # when all functions is constant
        except ValueError:
            unique_labels = list(set(np.asarray(labels).flatten()))

        # sort the labels in alphabetical order
        unique_labels = sorted(unique_labels)

        # add function values
        for function in functions:
            value = []
            # when the function is of type AutoDiff, it is made up of other AutoDiff class, then we can access the val attribute
            # val is a 1 * 1 matrix
            try:
                value.append(function.val[0][0])
            # when the function is a constant (doesn't involve any AutoDiff variables), we will just append the value
            except AttributeError:
                value.append(function)
            values.append(value)

        for function in functions:
            curr_jacobian = []
            for var in unique_labels:
                # find the index of variables stored in the function and access it
                try:
                    index = function.label.index(
                        var)
                    curr_jacobian.append(function.der[0][index])
                # when the variable is not used in the function, we replace it with 0
                except:
                    curr_jacobian.append(0)
            jacobians.append(curr_jacobian)

        self.values = values
        self.jacobians = jacobians
        self.labels = unique_labels


# x = AutoDiff(2, der=1, label="x")
# y = AutoDiff(3, der=1, label="y")
# z = AutoDiff(4, der=1, label="z")

# x_func = ForwardFunctions([x*(x + y) + (y - x).ln() * x ** 2, x *(x + y)], [x, y])

# print(x_func.values, x_func.jacobians, x_func.labels)
