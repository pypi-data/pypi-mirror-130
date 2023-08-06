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
        n._set_val(np.sin(a))
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
        n._set_val(np.cos(a))
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
        n._set_val(np.tan(a))
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
        n._set_val(np.sinh(a))
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
        n._set_val(np.cosh(a))
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
        return funcNode(np.tanh, lambda x: 1-np.tanh(x)**2, None, a, None)
    elif isinstance(a, int) or isinstance(a, float):
        n = valNode()
        n._set_val(np.tanh(a))
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
        return funcNode(np.sqrt, lambda x: 0.5/np.sqrt(x), None, a, None)
    elif isinstance(a, int) or isinstance(a, float):
        n = valNode()
        n._set_val(np.sqrt(a))
        return n
    else:
        raise TypeError

def logistic(a):
    if isinstance(a, Node):
        return funcNode(_logistic, lambda x: _logistic(x) * (1 - _logistic(x)), None, a, None)
    elif isinstance(a, int) or isinstance(a, float):
        n = valNode()
        n._set_val(_logistic(a))
        return n
    else:
        raise TypeError


def _logistic(a):
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
        n._set_val(np.exp(a))
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
        n._set_val(np.log(a))
        return n
    else:
        raise TypeError

def _log_ab(arg, base=np.exp(1)):
    return np.log(arg) / np.log(base)


def log_ab(a, b):
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


class Node:
    """
    Node class that implements the following native python functions: addition, subtraction, multipliation,
    division, unary operators, and power. Depending on the implemented funtions, Node will check if the inputs
    are of type integer, float, or Node. If they are of tyep Node, then the value and it's derivative is computed
    and stored in a dictionary. If the values are of type int or float, then the values are first convered to Node
    class by calling valNode.

    Attributes:
        val (int, float): Current value of the variable.
        der (int, float): Derivative of variable.
        add: Addition implementation for Node class.
        sub: Subtraction implementation for Node class.
        mul: Multiplication implementation for Node class.
        div: Division implementation for Node class.
        pow: Power implementation for Node class.
        pos: Positive unary operator for Node class.
        neg: Negative unary operator for Node class.


    """

    def __init__(self):
        # self.der = dict()
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
            r._set_val(other)
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
            r._set_val(other)
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
            r._set_val(other)
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
            r._set_val(other)
        else:
            raise TypeError
        return funcNode(np.divide, lambda x, y: 1 / y, lambda x, y: -x / y / y, self, r)

    def __rtruediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            l = valNode()
            l._set_val(other)
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
            r._set_val(other)
        else:
            raise TypeError
        return funcNode(np.power, lambda x, y: y * np.power(x, y - 1), lambda x, y: np.power(x, y) * np.log(x), self, r)

    def __rpow__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            l = valNode()
            l._set_val(other)
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
    overrides native python functions and unary operators, in order to construct a sequential computational graph. Sets
    the initial derivative (0) for each assigned variable.
    """
    def __init__(self, name = None):
        super().__init__()
        self.der = 0
        self.name = name
        # if name != None:
        #     self.der[name]=1

    def _set_val(self, val):
        """
        Sets the numeric value for a valNode.

        Args:
            val(int, float): numeric value of the valNode.
        """
        self.val = val

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
            Current value and empty derivative if number. Otherwise returns the value of the specified valNode and
            empty dictionary.
        """
        if self.name is None:
            return self.val, {self.name: 0}
        return self.val, {self.name: 1}
    
    def forward_pass(self):
        self.der = 0
        return self.val

    def reverse(self, partial, adjoint):
        # print(partial, adjoint)
        if self.name != None:
            self.der += partial * adjoint


class funcNode(Node):
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

    def reverse(self, partial, adjoint):
        if self.right != None:
            lder = self.leftdf(self.left.val, self.right.val)
            rder = self.rightdf(self.left.val, self.right.val)
            self.left.reverse(lder, partial * adjoint)
            self.right.reverse(rder, partial * adjoint)
        else:
            lder = self.leftdf(self.left.val)
            self.left.reverse(lder, partial * adjoint)

        # return self.val

            
            
if __name__ == '__main__':

    
    # v = vector([1,2,3])
    
    def f(v):
        '''
            f takes a size=3 vector and output a size=2 vector
        '''
        f1 = sin(ln(v[0]))+tan(v[0]**2+v[0]*v[1]+v[2])
        f2 = ln(sin(exp(v[0])+v[1])) + exp(v[1]) + v[2]
        return f1,f2

    '''x = valNode('x')
    y = valNode('y')
    c = valNode('c')
    f = sin(log(x)) + tan(x * x + y * x + x ** 3 * y)
    x._set_val(2)
    y._set_val(3)
    c._set_val(np.pi)
    print(f.forward())
    f.forward_pass()
    f.reverse(1,1)
    print(f.val, x.der, y.der)
    
    x.der = 0
    y.der = 0
    f = log(sin(exp(x)+y)) + exp(y) + x
    x._set_val(0)
    y._set_val(1)
    print(f.forward())
    f.forward_pass()
    f.reverse(1,1)
    print(f.val, x.der, y.der)
    
    x.der = 0
    y.der = 0
    f = log(sin(x+y)**2)+exp(x**2+y**2)
    print(f)
    x._set_val(1)
    y._set_val(2)
    print(f.forward())
    f.forward_pass()
    f.reverse(1,1)
    print(f.val, x.der, y.der)
    
    print("testing: sin(ab + b)")
    a = valNode('a')
    b = valNode('b')
    f = sin(a * b + b)
    a._set_val(2)
    b._set_val(5)
    # print(f)
    # print(f.forward())
    f_val, f_grad = f.forward()

    actual_f_val = np.sin(a.val * b.val + b.val)
    actual_f_grad = {
        'a': b.val * np.cos((a.val + 1) * b.val),
        'b': (a.val + 1) * np.cos((a.val + 1) * b.val)
    }

    assert np.isclose(f_val, actual_f_val)

    for var in f_grad:
        assert np.isclose(f_grad[var], actual_f_grad[var])

    f.forward_pass()
    # print(f.val, )
    f.reverse(1, 1)
    reverse_grads = {
        'a': a.der,
        'b': b.der
    }
    for var in f_grad:
        assert np.isclose(f_grad[var], reverse_grads[var])

    print("testing: e^(a/c) + b")
    a = valNode('a')
    b = valNode('b')
    c = valNode('c')
    f = exp(a / c) + b
    a._set_val(np.pi / 2)
    b._set_val(np.pi / 3)
    c._set_val(np.pi)

    actual_f_val = np.exp(a.val / c.val) + b.val
    # print(np.exp(a.val / c.val), np.arccos(np.exp(a.val / c.val)))

    actual_f_grad = {
        'a': (np.exp(a.val / c.val)) / (c.val),
        'b': 1,
        'c': -(a.val * np.exp(a.val / c.val)) / (c.val ** 2),
    }

    f.forward_pass()
    # print(f.val, )
    f.reverse(1, 1)
    reverse_grads = {
        'a': a.der,
        'b': b.der,
        'c': c.der,
    }

    for var in actual_f_grad.keys():
        assert np.isclose(actual_f_grad[var], reverse_grads[var])'''




