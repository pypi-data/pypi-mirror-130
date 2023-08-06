from .dual import Dual

class Node:

    def __init__(self, parents = []):
        self._parents = parents

    def forward(self, value, direction):
        raise NotImplementedError

    def __add__(self, node):
        if isinstance(node, Node):
            return Add([self, node])
        return Add([self, Const(node)])

    def __radd__(self, node):
        if isinstance(node, Node):
            return Add([self, node])
        return Add([self, Const(node)])
    
    def __mul__(self, node):
        if isinstance(node, Node):
            return Mul([self, node])
        return Mul([self, Const(node)])

    def __rmul__(self, node):
        if isinstance(node, Node):
            return Mul([self, node])
        return Mul([self, Const(node)])
    
    def __sub__(self, node):
        if isinstance(node, Node):
            return Sub([self, node])
        return Sub([self, Const(node)])
    
    def __rsub__(self, node):
        if isinstance(node, Node):
            return Sub([self, node])
        return Sub([self, Const(node)])
    
    def __truediv__(self, node):
        if isinstance(node, Node):
            return Div([self, node])
        return Div([self, Const(node)])
    
    def __rtruediv__(self, node):
        if isinstance(node, Node):
            return Div([self, node])
        return Div([self, Const(node)])
    
    def __pow__(self, exponent):
        return Power([self], exponent)

class Var(Node):
    
    def __init__(self, name):
        super().__init__([])
        self._name = name
        
    def __repr__(self):
        return "Var(%s)" % self._name
    
    def __str__(self):
        return self._name
    
    def forward(self, value, direction):
        try:
            return Dual(value[self._name], direction[self._name])
        except:
            raise KeyError("Cannot perform forward mode: no value or direction for Var node %s was given" % self._name)

class Const(Node):
    
    def __init__(self, value):
        super().__init__([])
        self._value = value
        
    def __repr__(self):
        return "Const(%s)" % self._value
    
    def __str__(self):
        return str(self._value)
    
    def forward(self, value, direction):
        return Dual(self._value, 0)

class Add(Node):
    
    def __repr__(self):
        return "Add(%s)" % (", ".join([parent.__repr__() for parent in self._parents]))
    
    def __str__(self):
        return "(" + (" + ".join([str(parent) for parent in self._parents])) + ")"
    
    def forward(self, value, direction):
        if len(self._parents) == 0:
            return Dual(0, 0)
        return sum(parent.forward(value, direction) for parent in self._parents)

class Mul(Node):
    
    def __repr__(self):
        return "Mul(%s)" % (", ".join([parent.__repr__() for parent in self._parents]))
    
    def __str__(self):
        return "(" + (" * ".join([str(parent) for parent in self._parents])) + ")"
    
    def forward(self, value, direction):
        if len(self._parents) == 0:
            return Dual(0, 0)
        result = Dual(1, 0)
        for parent in self._parents:
            result *= parent.forward(value, direction)
        return result

class Sub(Node):
    
    def __init__(self, parents):
        assert len(parents) == 2, "Substraction requires exactly two node arguments"
        super().__init__(parents)
    
    def __repr__(self):
        return "Sub(%s)" % (", ".join([parent.__repr__() for parent in self._parents]))
    
    def __str__(self):
        return "(" + (" - ".join([str(parent) for parent in self._parents])) + ")"
    
    def forward(self, value, direction):
        return self._parents[0].forward(value, direction) - self._parents[1].forward(value, direction)

class Div(Node):
    
    def __init__(self, parents):
        assert len(parents) == 2, "Division requires exactly two node arguments"
        super().__init__(parents)
    
    def __repr__(self):
        return "Div(%s)" % (", ".join([parent.__repr__() for parent in self._parents]))
    
    def __str__(self):
        return "(" + (" / ".join([str(parent) for parent in self._parents])) + ")"
    
    def forward(self, value, direction):
        return self._parents[0].forward(value, direction) / self._parents[1].forward(value, direction)

class Power(Node):
    
    def __init__(self, parents, exponent):
        assert len(parents) == 1, "Power requires exactly one node argument (%s given)" % len(parents)
        super().__init__(parents)
        self._exponent = exponent
    
    def __repr__(self):
        return "Power(%s, %s)" % (self._parents[0].__repr__(), self._exponent)
    
    def __str__(self):
        return "(" + str(self._parents[0]) + "^" + str(self._exponent) + ")"
    
    def forward(self, value, direction):
        return self._parents[0].forward(value, direction).power(self._exponent)

class Exp(Node):
    
    def __init__(self, parents):
        assert len(parents) == 1, "Exponential requires exactly one node argument (%s given)" % len(parents)
        super().__init__(parents)
    
    def __repr__(self):
        return "Exp(%s)" % self._parents[0].__repr__()
    
    def __str__(self):
        return "exp(" + str(self._parents[0]) + ")"
    
    def forward(self, value, direction):
        return self._parents[0].forward(value, direction).exp()

class Log(Node):
    
    def __init__(self, parents):
        assert len(parents) == 1, "Logarithm requires exactly one node argument (%s given)" % len(parents)
        super().__init__(parents)
    
    def __repr__(self):
        return "Log(%s)" % self._parents[0].__repr__()
    
    def __str__(self):
        return "log(" + str(self._parents[0]) + ")"
    
    def forward(self, value, direction):
        return self._parents[0].forward(value, direction).log()

class Cos(Node):
    
    def __init__(self, parents):
        assert len(parents) == 1, "Cosine requires exactly one node argument (%s given)" % len(parents)
        super().__init__(parents)
    
    def __repr__(self):
        return "Cos(%s)" % self._parents[0].__repr__()
    
    def __str__(self):
        return "cos(" + str(self._parents[0]) + ")"
    
    def forward(self, value, direction):
        return self._parents[0].forward(value, direction).cos()

class Sin(Node):
    
    def __init__(self, parents):
        assert len(parents) == 1, "Sine requires exactly one node argument (%s given)" % len(parents)
        super().__init__(parents)
    
    def __repr__(self):
        return "Sin(%s)" % self._parents[0].__repr__()
    
    def __str__(self):
        return "sin(" + str(self._parents[0]) + ")"
    
    def forward(self, value, direction):
        return self._parents[0].forward(value, direction).sin()

class Tan(Node):
    
    def __init__(self, parents):
        assert len(parents) == 1, "Tan requires exactly one node argument (%s given)" % len(parents)
        super().__init__(parents)
    
    def __repr__(self):
        return "Tan(%s)" % self._parents[0].__repr__()
    
    def __str__(self):
        return "tan(" + str(self._parents[0]) + ")"
    
    def forward(self, value, direction):
        return self._parents[0].forward(value, direction).tan()

if __name__ == "__main__":
    x = Var("x")
    d = x.forward({"x": 2}, {"x": 1})
    print("Forward on x -> %s at x = 2, d = 1:" % x, d)
    
    y = Var("y")
    z = x + y
    d = z.forward({"x": 2, "y": 1}, {"x": 1, "y": 1})
    print("Forward on x, y -> %s at (x, y) = (2, 1), d = (1, 1):" % z, d)
    
    z = x * y
    d = z.forward({"x": 2, "y": 1}, {"x": 1, "y": 1})
    print("Forward on x, y -> %s at (x, y) = (2, 1), d = (1, 1):" % z, d)
    
    z = x * y + x + y + 3.5
    d = z.forward({"x": 2, "y": 1}, {"x": 1, "y": 1})
    print("Forward on x, y -> %s at (x, y) = (2, 1), d = (1, 1):" % z, d)
    
    z = x / y + x - y + 3.5
    d = z.forward({"x": 2, "y": 1}, {"x": 1, "y": 1})
    print("Forward on x, y -> %s at (x, y) = (2, 1), d = (1, 1):" % z, d)
    
    try:
        
        # Should throw an exception indicating that we need 2 arguments
        u = Sub([])
    except Exception as e:
        print(e)
        
    try:
        
        # Should throw an exception indicating that we need 2 arguments
        u = Div([])
    except Exception as e:
        print(e)
    
    # Functions
    
    z = x ** 4
    d = z.forward({"x": 2}, {"x": 1})
    print("Forward on x -> %s at x = 2, d = 1:" % z, d)
    
    try:
        
        # Should throw an exception indicating that we need 1 argument
        u = Power([], 2)
    except Exception as e:
        print(e)