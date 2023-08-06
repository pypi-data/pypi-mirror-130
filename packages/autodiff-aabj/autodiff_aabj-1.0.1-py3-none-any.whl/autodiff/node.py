import numpy as np


def sin(a):
    """
    Implements sine to contribute to a computational graph. Converts integers and floats to
    Node's, and inserts derivatives into the computational graph.

    Args:
        a (int, float, Node): Value to be calculated through sine.

    Returns:
        Node with values and derivatives along with a corresponding computational graph.

    Raises:
        TypeError if value is not of type int, float, or Node.
        """
    if isinstance(a, Node):
        return funcNode(np.sin, np.cos, None, a, None)
    elif isinstance(a, int) or isinstance(a, float):
        n = valNode()
        n.set_val(np.sin(a))
        return n
    else:
        raise TypeError


def arcsin(a):
    """
    Implements sine inverse function to contribute to a computational graph. Converts integers and floats to
    Node's, and inserts derivatives into the computational graph.

    Args:
        a (int, float, Node): Value to be calculated through arcsin.

    Returns:
        Node with values and derivatives along with a corresponding computational graph.

    Raises:
        TypeError if value is not of type int, float, or Node.
        """
    if isinstance(a, Node):
        return funcNode(np.arcsin, lambda x: 1 / np.sqrt(1 - x * x), None, a, None)
    elif isinstance(a, int) or isinstance(a, float):
        n = valNode()
        n.set_val(np.arcsin(a))
        return n
    else:
        raise TypeError


def cos(a):
    """
    Implements cosine to contribute to a computational graph. Converts integers and floats to
    Node's, and inserts derivatives into the computational graph.

    Args:
        a (int, float, Node): Value to be calculated through cosine.

    Returns:
        Node with values and derivatives along with a corresponding computational graph.

    Raises:
        TypeError if value is not of type int, float, or Node.
        """
    if isinstance(a, Node):
        return funcNode(np.cos, lambda x: -np.sin(x), None, a, None)
    elif isinstance(a, int) or isinstance(a, float):
        n = valNode()
        n.set_val(np.cos(a))
        return n
    else:
        raise TypeError


def arccos(a):
    """
    Implements inverse cosine  function to contribute to a computational graph. Converts integers and floats to
    Node's, and inserts derivatives into the computational graph.

    Args:
        a (int, float, Node): Value to be calculated through arccos.

    Returns:
        Node with values and derivatives along with a corresponding computational graph.

    Raises:
        TypeError if value is not of type int, float, or Node.
        """
    if isinstance(a, Node):
        return funcNode(np.arccos, lambda x: -1 / np.sqrt(1 - x * x), None, a, None)
    elif isinstance(a, int) or isinstance(a, float):
        n = valNode()
        n.set_val(np.arccos(a))
        return n
    else:
        raise TypeError


def tan(a):
    """
    Implements tangent to contribute to a computational graph. Converts integers and floats to
    Node's, and inserts derivatives into the computational graph.

    Args:
        a (int, float, Node): Value to be calculated through tan.

    Returns:
        Node with values and derivatives along with a corresponding computational graph.

    Raises:
        TypeError if value is not of type int, float, or Node.
        """
    if isinstance(a, Node):
        return funcNode(np.tan, lambda x: 1 / (np.cos(x)) ** 2, None, a, None)
    elif isinstance(a, int) or isinstance(a, float):
        n = valNode()
        n.set_val(np.tan(a))
        return n
    else:
        raise TypeError


def arctan(a):
    """
    Implements inverse tangent  function to contribute to a computational graph. Converts integers and floats to
    Node's, and inserts derivatives into the computational graph.

    Args:
        a (int, float, Node): Value to be calculated through arctan.

    Returns:
        Node with values and derivatives along with a corresponding computational graph.

    Raises:
        TypeError if value is not of type int, float, or Node.
        """
    if isinstance(a, Node):
        return funcNode(np.arctan, lambda x: 1 / (1 + x * x), None, a, None)
    elif isinstance(a, int) or isinstance(a, float):
        n = valNode()
        n.set_val(np.arctan(a))
        return n
    else:
        raise TypeError


def sinh(a):
    """
    Implements hyperbolic sine to contribute to a computational graph. Converts integers and floats to
    Node's, and inserts derivatives into the computational graph.

    Args:
        a (int, float, Node): Value to be calculated through hyperbolic sine.

    Returns:
        Node with values and derivatives along with a corresponding computational graph.

    Raises:
        TypeError if value is not of type int, float, or Node.
        """
    if isinstance(a, Node):
        return funcNode(np.sinh, np.cosh, None, a, None)
    elif isinstance(a, int) or isinstance(a, float):
        n = valNode()
        n.set_val(np.sinh(a))
        return n
    else:
        raise TypeError


def cosh(a):
    """
    Implements hyperbolic cosine to contribute to a computational graph. Converts integers and floats to
    Node's, and inserts derivatives into the computational graph.

    Args:
        a (int, float, Node): Value to be calculated through hyperbolic cosine.

    Returns:
        Node with values and derivatives along with a corresponding computational graph.

    Raises:
        TypeError if value is not of type int, float, or Node.
        """
    if isinstance(a, Node):
        return funcNode(np.cosh, np.sinh, None, a, None)
    elif isinstance(a, int) or isinstance(a, float):
        n = valNode()
        n.set_val(np.cosh(a))
        return n
    else:
        raise TypeError


def tanh(a):
    """
    Implements hyperbolic tangent to contribute to a computational graph. Converts integers and floats to
    Node's, and inserts derivatives into the computational graph.

    Args:
        a (int, float, Node): Value to be calculated through hyperbolic tangent.

    Returns:
        Node with values and derivatives along with a corresponding computational graph.

    Raises:
        TypeError if value is not of type int, float, or Node.
        """
    if isinstance(a, Node):
        return funcNode(np.tanh, lambda x: 1 - np.tanh(x) ** 2, None, a, None)
    elif isinstance(a, int) or isinstance(a, float):
        n = valNode()
        n.set_val(np.tanh(a))
        return n
    else:
        raise TypeError


def sqrt(a):
    """
    Implements square-root to contribute to a computational graph. Converts integers and floats to
    Node's, and inserts derivatives into the computational graph.

    Args:
        a (int, float, Node): Value to be square-rooted.

    Returns:
        Node with values and derivatives along with a corresponding computational graph.

    Raises:
        TypeError if value is not of type int, float, or Node.
        """
    if isinstance(a, Node):
        return funcNode(np.sqrt, lambda x: 0.5 / np.sqrt(x), None, a, None)
    elif isinstance(a, int) or isinstance(a, float):
        n = valNode()
        n.set_val(np.sqrt(a))
        return n
    else:
        raise TypeError


def logistic(a):
    """
        Implements logistic function to contribute to a computational graph. Converts integers and floats to
        Node's, and inserts derivatives into the computational graph.

        Args:
            a (int, float, Node): Value of which we are calulating logistic.

        Returns:
            Node with values and derivatives along with a corresponding computational graph.

        Raises:
            TypeError if value is not of type int, float, or Node.
            """
    if isinstance(a, Node):
        return funcNode(_logistic, lambda x: _logistic(x) * (1 - _logistic(x)), None, a, None)
    elif isinstance(a, int) or isinstance(a, float):
        n = valNode()
        n._set_val(_logistic(a))
        return n
    else:
        raise TypeError


def _logistic(a):
    """
    Helper function for logistic, implements logistic function for int or float data type.
    Args:
        a (int, float): Real number whose logistic function is to be calculated.

    Returns:
        Logistic value of the argument a.
    """
    return (np.tanh(a / 2) + 1) * 0.5


def exp(a):
    """
    Implements exponential function to calculate values, derivatives, and to contribute to a computational graph. Converts integers and floats to
    Node's, and inserts derivatives into the computational graph.

    Args:
        a (int, float, Node): Value to be raised to the power of e.

    Returns:
        Node with values and derivatives along with a corresponding computational graph.

    Raises:
        TypeError if value is not of type int, float, or Node.
    """
    if isinstance(a, Node):
        return funcNode(np.exp, np.exp, None, a, None)
    elif isinstance(a, int) or isinstance(a, float):
        n = valNode()
        n.set_val(np.exp(a))
        return n
    else:
        raise TypeError


def log(a):
    """
    Alias for ln(a).

    Args:
        a (int, float, Node): Value to be passed through natural logarithm.

    Returns:
        Node with values and derivatives along with a corresponding computational graph.
    """

    return ln(a)


def ln(a):
    """
    Implements the natural logarithm to calculate values, derivative, and to contribute to a computational graph. Converts integers and floats to
    Node's, and inserts derivatives into the computational graph.

    Args:
        a (int, float, Node): Value to be passed through natural logarithm.

    Returns:
        Node with values and derivatives along with a corresponding computational graph.
    """
    if isinstance(a, Node):
        return funcNode(np.log, lambda x: 1 / x, None, a, None)
    elif isinstance(a, int) or isinstance(a, float):
        n = valNode()
        n.set_val(np.log(a))
        return n
    else:
        raise TypeError


def _log_ab(arg, base=np.exp(1)):
    """
        Helper function for log_ab, implements logarithm function for int or float data type with arg as argument
        of logarithm and base as the base.
        Args:
            arg (int, float): Argument of the logarithm function.
            base (int, float): Base of the logarithm function.
        Returns:
            log value of the argument arg and base base .
    """

    return np.log(arg) / np.log(base)


def log_ab(a, b):
    """
        Implements the logarithm with arbitrary base b for argument a to calculate values, derivative, and to contribute
        to a computational graph. Converts integers and floats to Node's, and inserts derivatives into the computational graph.

        Args:
            a (int, float, Node): The Argument of logarithm.
            b (int, float, Node): The base of the logarithma
        Returns:
            Node with values and derivatives along with a corresponding computational graph.
        """
    if isinstance(a, Node) and isinstance(b, Node):
        return funcNode(_log_ab, lambda x, y: (1 / np.log(y)) * 1 / x,
                        lambda x, y: (-(1 / y) * np.log(x) * ((1 / np.log(y)) ** 2)),
                        a, b)
    elif isinstance(a, Node) and (isinstance(b, int) or isinstance(b, float)):
        return (log(a)) / np.log(b)

    elif (isinstance(a, int) or isinstance(a, float)) and isinstance(b, Node):
        return (np.log(a)) / log(b)

    elif (isinstance(a, int) or isinstance(a, float)) and (isinstance(b, int) or isinstance(b, float)):
        n = valNode()
        n._set_val((np.log(a)) / np.log(b))
        return n
    else:
        raise TypeError


class Node:
    """
    Node class that implements the following native python functions: addition, subtraction, multipliation,
    division, unary operators, and power. Depending on the implemented funtions, Node will check if the inputs
    are of type integer, float, or Node. If they are of tyep Node, then a new Node will be generated to be the
    parent of inputs and be returned. If the values are of type int or float, then the values are first convered
    to Node class by calling valNode, and be operated in the same way as when the inputs are of type Node.

    Attributes:
        add: Addition implementation for Node class.
        sub: Subtraction implementation for Node class.
        mul: Multiplication implementation for Node class.
        div: Division implementation for Node class.
        pow: Power implementation for Node class.
        pos: Positive unary operator for Node class.
        neg: Negative unary operator for Node class.


    """

    def __init__(self):
        pass

    def __add__(self, other):
        """Implements native python function for addition.

        Calculates and inserts the derivative values into the
        left and right nodes via valNode for construction of a computational graph.

        Args:
            other (int, float, Node): value to be added.

        Returns:
            None
        """
        if isinstance(other, Node):
            r = other
        elif isinstance(other, int) or isinstance(other, float):
            r = valNode()
            r.set_val(other)
        else:
            raise TypeError
        return funcNode(np.add, lambda x, y: 1, lambda x, y: 1, self, r)

    def __radd__(self, other):
        """Implements native python function for reverse of addition. Calculates and inserts the derivative values into the
        left and right nodes via valNode for construction of a computational graph.

        Args:
            other(int, float, Node): value to be added.

        """
        return self + other

    def __mul__(self, other):
        """Implements native python function for multiplication. Calculates and inserts the derivative values into the
        left and right nodes via valNode for construction of a computational graph.

        Args:
            other(int, float, Node): value to be multiplied.
        """
        if isinstance(other, Node):
            r = other
        elif isinstance(other, int) or isinstance(other, float):
            r = valNode()
            r.set_val(other)
        else:
            raise TypeError
        return funcNode(np.multiply, lambda x, y: y, lambda x, y: x, self, r)

    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        """
        Implements native python unary operator for negation.
        """
        return self * (-1)

    def __sub__(self, other):
        """Implements native python function for subtraction. Calculates and inserts the derivative values into the
        left and right nodes via valNode for construction of a computational graph.

        Args:
            other(int, float, Node): value to be subtracted.
        """
        if isinstance(other, Node):
            r = other
        elif isinstance(other, int) or isinstance(other, float):
            r = valNode()
            r.set_val(other)
        else:
            raise TypeError
        return funcNode(np.subtract, lambda x, y: 1, lambda x, y: -1, self, r)

    def __rsub__(self, other):
        return -self + other

    def __truediv__(self, other):
        """Implements native python function for division. Calculates and inserts the derivative values into the
        left and right nodes via valNode for construction of a computational graph.

        Args:
            other(int, float, Node): value to be multiplied.
        """
        if isinstance(other, Node):
            r = other
        elif isinstance(other, int) or isinstance(other, float):
            r = valNode()
            r.set_val(other)
        else:
            raise TypeError
        return funcNode(np.divide, lambda x, y: 1 / y, lambda x, y: -x / y / y, self, r)

    def __rtruediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            l = valNode()
            l.set_val(other)
        else:
            raise TypeError
        return funcNode(np.divide, lambda x, y: 1 / y, lambda x, y: -x / y / y, l, self)

    def __pow__(self, other):
        """Implements native python function for power. Calculates and inserts the derivative values into the
        left and right nodes via valNode for construction of a computational graph.

        Args:
            other(int, float, Node): value of the exponent.
        """
        if isinstance(other, Node):
            r = other
        elif isinstance(other, int) or isinstance(other, float):
            r = valNode()
            r.set_val(other)
        else:
            raise TypeError("unsupported input type(s) for the operand")
        return funcNode(np.power, lambda x, y: y * np.power(x, y - 1), lambda x, y: np.power(x, y) * np.log(x), self, r)

    def __rpow__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            l = valNode()
            l.set_val(other)
        else:
            raise TypeError
        return funcNode(np.power, lambda x, y: y * np.power(x, y - 1), lambda x, y: np.power(x, y) * np.log(x), l, self)

    def __pos__(self):
        """
        Implements positive unary operator.
        """
        return self


class valNode(Node):
    """
    Sets variables as valNode class, which allows the users to auto-differentiate functions that use them. valNode class
    overrides native python functions and unary operators, in order to construct a sequential computational graph.

    Attributes:
        val (int, float): Current value of the variable.
        name (str): The name of the variable.
        der (int, float): Derivative of variable, which is used in the reverse mode.
    """

    def __init__(self, name=None):
        super().__init__()
        self.der = 0
        self.name = name

    def _set_val(self, val):
        """
        Sets the numeric value for a valNode.

        Args:
            val(int, float): numeric value of the valNode.
        """
        self.val = val

    def set_val(self, val):
        """
        Alias for _set_val(self, val).  Sets the numeric value for a valNode.

        Args:
            val(int, float): numeric value of the valNode.

        """
        if isinstance(val, int) or isinstance(val, float):
            self._set_val(val)
        else:
            raise TypeError("The value for a variable should be 'int' or 'float'.")

    def __str__(self):
        """
        Prints information about a specified valNode.

        Returns:
            Returns the name of the valNode or it's value if the name is empty.
        """
        return str(self.name) if self.name != None else str(self.val)

    def forward(self):
        """
        Executes a simple forward pass for a single node.

        Returns:
            Current value and empty derivative if no name. Otherwise returns the value of the specified valNode and
            derivative 1.
        """
        if self.name is None:
            return self.val, {}
        return self.val, {self.name: 1}

    def forward_pass(self):
        self.der = 0
        return self.val

    def reverse_pass(self, partial, adjoint):
        if self.name == None:
            return dict()
        self.der += partial * adjoint
        return {self.name: self}

    def _reset_der(self):
        self.der = 0


class funcNode(Node):
    """
    Sets intermediate variables as funcNode class to memorize the functions needed to represent the final output 
    function. funcNode class overrides native python functions and unary operators, in order to construct a 
    sequential computational graph, based on which the users can auto-differentiate the functions they are interested
    in.

    Attributes:
        val (int, float): Current value of the intermediate variable.
        func (callable): The arithmetic function executed to calculate the intermediate variable.
        leftdf (callable): The arithmetic function to calculate the partial derivative of the current node 
        with respect to its left child.
        rightdf (callable): The arithmetic function to calculate the partial derivative of the current node 
        with respect to its right child.
        left (Node): Left child of the node.
        right (Node): Right child of the node.


    """

    def __init__(self, func, leftdf, rightdf, left, right):
        super().__init__()
        self.func = func
        self.leftdf = leftdf
        self.rightdf = rightdf
        self.val = None
        self.left = left
        self.right = right

    def __str__(self):
        return f'{self.func.__name__}' + \
               '\n|\n|-(L)->' + '\n|      '.join(str(self.left).split('\n')) + \
               '\n|\n|-(R)->' + '\n|      '.join(str(self.right).split('\n'))

    def forward(self):
        """
            calculate function value and derivatives with forward mode.
            Args:
                self (Node): The current node.

            Returns:
                val (float): The value of the function
                der (dict): The dictionary containing all the partial derivatives of the functions with 
                variable names as keys.

        """    
        if self.right != None:
            aval, ader = self.left.forward()
            bval, bder = self.right.forward()
            val = self.func(aval, bval)
            der = dict()
            for k in ader:
                der[k] = ader[k] * self.leftdf(aval, bval)
            for k in bder:
                if k in der:
                    der[k] += bder[k] * self.rightdf(aval, bval)
                else:
                    der[k] = bder[k] * self.rightdf(aval, bval)
            return val, der
        else:
            aval, ader = self.left.forward()
            val = self.func(aval)
            der = dict()
            for k in ader:
                der[k] = ader[k] * self.leftdf(aval)
            return val, der

    def forward_pass(self):
        if self.right != None:
            self.val = self.func(self.left.forward_pass(), self.right.forward_pass())
        else:
            self.val = self.func(self.left.forward_pass())
        return self.val

    def reverse_pass(self, partial, adjoint):
        if self.right != None:
            lder = self.leftdf(self.left.val, self.right.val)
            rder = self.rightdf(self.left.val, self.right.val)
            lvars = self.left.reverse_pass(lder, partial * adjoint)
            rvars = self.right.reverse_pass(rder, partial * adjoint)
            for v in rvars:
                if v not in lvars:
                    lvars[v] = rvars[v]
        else:
            lder = self.leftdf(self.left.val)
            lvars = self.left.reverse_pass(lder, partial * adjoint)

        return lvars

    def reverse(self):
        """
            calculate function value and derivatives with reverse mode.
            Args:
                self (Node): The current node.

            Returns:
                val (float): The value of the function
                der (dict): The dictionary containing all the partial derivatives of the functions with 
                variable names as keys.

        """    
        self.forward_pass()
        variables = self.reverse_pass(1, 1)
        der = {v: node.der for v, node in variables.items()}
        return self.val, der


class vector:
    """
        Combines several valNodes together to support vectorized input variables. vector and valNode share
        the same syntaxes for .set_val, .der and ._reset_der. Every single element in the vector variable 
        can be indexed.
    """
    
    def __init__(self, *args):
        self.size = len(args)
        self.elements = args

    def set_val(self, array):
        """
            set the value of the vector variable.
            Args:
                array (list): A list of value to be set for the vector.

            Returns:
                None

            Raises:
                ValueError if the input size does not match the vector size.
        """
        if len(array) != self.size:
            raise ValueError(f"Input size has a mismatch with the vector size ({self.size})")
        for node, val in zip(self.elements, array):
            node.set_val(val)

    def __getitem__(self, key):
        return self.elements[key]

    def __iter__(self, key):
        return iter(self.elements)

    def grad(self, var):
        """
            auto-diff for vector functions
            currently we only use reverse mode to calculate gradient for vector functions
            Args: 
                the variable or vector variables var, which is used to define the function 
                and for which we need to calculate the derivatives
            Return: Jacobian matrix
        """
        der_array = []
        var._reset_der()
        for f in self.elements:
            f.forward_pass()
            f.reverse_pass(1, 1)
            der_array.append(var.der)
            var._reset_der()
        return der_array

    def evaluate(self):
        """
            evaluation for vector functions
            Return: The vector values of the vector function.
        """
        return [f.forward_pass() for f in self.elements]

    @property
    def der(self):
        return [node.der for node in self.elements]

    def _reset_der(self):
        """
           this function only works if it is a variable vector
        """
        for node in self.elements:
            node.der = 0


def variables(name, size=None):
    """
        initialize independent variables for the function of interest
        
        Args:
            name (str): The name to identify the variable.
            size (int): The size of the variable.

        Returns:
            vector when size > 1
            valNode when size = 1 or None
    """
    if (size is None) or (size == 1):
        return valNode(name)
    elems = [valNode(name + '___' + str(i)) for i in range(size)]
    return vector(*elems)


if __name__ == '__main__':
    def func(v):    
        # f takes a size=3 vector and output a size=2 vector
        f1 = sin(ln(v[0])) + tan(v[0] ** 2 + v[0] * v[1] + v[0] ** 3 * v[1])
        f2 = v[0] * v[1] + v[1] ** 2 + sqrt(v[0])
        return vector(f1, f2)


    f = func(v)
    print(f.evaluate())
    print(f.grad(v))


    # vector function can also take a scalar input variable
    def func1(x):
        f1 = x ** 2
        f2 = x ** 3
        return vector(f1, f2)


    f = func1(x)
    print(f.evaluate())
    print(f.grad(x))
