import numpy as np

# Define Dual Numbers class w/ dunder methods 
class Dual():
    
    num_types = (int, float)
    
    def __init__(self, real, dual=[1]): # required
        self.real = real
        self.dual = np.array(dual)
        
    def __repr__(self):
        return "MyClass(real=%r,dual=%r)" % (self.real,self.dual)

    def __neg__(self): # required (-)
        return Dual(-self.real, -np.array(self.dual))
    
    def __add__(self, other): #required (+)
        if isinstance(other, Dual): 
            r = self.real + other.real
            d = np.array(self.dual) + np.array(other.dual)
        elif isinstance(other, Dual.num_types): 
            r = self.real + other
            d = np.array(self.dual)
        else: 
            raise TypeError(f'type {type(other)} cannot be added with type Dual')
    
        return Dual(r, d)
    
    def __radd__(self, other): 
        return self + other
    
    def __iadd__(self, other): #required (+=)
        self = self + other
        return self

    def __mul__(self, other): # required (*)
        if isinstance(other, Dual): 
            r1, r2 = self.real, other.real
            d1, d2 = np.array(self.dual), np.array(other.dual)
            r = r1 * r2
            d = r1 * d2 + r2 * d1
        elif isinstance(other, Dual.num_types): 
            r = self.real * other
            d = np.array(self.dual) * other
        else: 
            raise TypeError(f'type {type(other)} cannot be multiplied with type Dual')
    
        return Dual(r, d)
    
    def __rmul__(self, other):
        return self*other
    
    def __imul__(self,other): # required (*=)
        self = self * other
        return self

    def __sub__(self, other): # required (-)
        if isinstance(other, Dual): 
            r = self.real - other.real
            d = np.array(self.dual) - np.array(other.dual)
        elif isinstance(other, Dual.num_types): 
            r = self.real - other
            d = np.array(self.dual)
        else: 
            raise TypeError(f'type {type(other)} cannot be subtracted with type Dual')
            
        return Dual(r, d)
    
    def __rsub__(self, other): 
        return -self + other
    
    def __isub__(self, other): # required (-=)
        self = self - other
        return self
    
    def __truediv__(self,other): # required (\)
        if isinstance(other, Dual): 
            r1, r2 = self.real, other.real
            d1, d2 = np.array(self.dual), np.array(other.dual)
            r = r1 / r2
            d = (d1 * r2 - r1 * d2) / (r2**2)
        elif isinstance(other, Dual.num_types): 
            r = self.real * (1 / other)
            d = np.array(self.dual) * (1 / other)
        else: 
            raise TypeError(f'type {type(other)} cannot be divided with type Dual')
            
        return Dual(r, d)

    def __rtruediv__(self, other):
        return (self**-1) * other
    
    def __itruediv__(self,other): # required (\=)
        self = self / other
        return self
    
    def __pow__(self, other): # required (**)
        if isinstance(other, Dual): 
            r1, r2 = self.real, other.real
            d1, d2 = np.array(self.dual), np.array(other.dual)
            r = r1**r2
            d = (r1**r2)*((d2**(np.log(r1)))+((d1*r2)/r1))
        elif isinstance(other, Dual.num_types): 
            r = self.real**other
            d = other*(self.real**(other-1))*self.dual
        else: 
            raise TypeError(f'type {type(other)} cannot be pow with type Dual')
            
        return Dual(r, d)
    
    def __rpow__(self,other): 
        if isinstance(other, Dual.num_types): 
            r1, r2 = other, self.real 
            d1, d2 = 0, np.array(self.dual)
            r = r1**r2
            d = (r1**r2)*((d2**(np.log(r1)))+((d1*r2)/r1))
            return Dual(r, d)
        else: 
            raise TypeError(f'type {type(other)} cannot be pow with type Dual')
    
    def __eq__(self, other):
        if isinstance(other, Dual):
            if self.real == other.real and self.dual == other.dual:
                return True
            else:
                return False
        else:
            raise TypeError(f'type {type(other)} cannot be compared with type Dual')

    def __ne__(self, other):
        if isinstance(other, Dual):
            return (not self == other)
        else:
            raise TypeError(f'type {type(other)} cannot be compared with type Dual')
            
class FwdAD():
    
    def __init__(self, functions, inputs):
        self.functions = functions
        self.inputs = inputs
        self.outputs = {}
        self.update_grads()
    
            
    def update_grads(self): 
        for i, var in enumerate(self.inputs): 
            if not var.dual: # if the variable has no dual
                der = np.zeros(len(self.inputs)) # each input has a gradient in each Dual
                der[i] = 1 # assign dual value to 1 for this input's corresponding gradient 
                var.dual = der
            elif len(var.dual) == 1: # if the variable has a single value in dual
                der = np.zeros(len(self.inputs)) # each input has a gradient in each Dual
                der[i] = var.dual # assign dual value for this input's corresponding gradient 
                var.dual = der 
            elif len(var.dual) != len(self.inputs): # if variable dual does not account for all inputs
                raise Error('Pre-defined derivatives must account for gradients at all variables')
            # if none of these conditions are true, 
            # var.dual exists AND is len(inputs), no need to change
            
    # evaluate and save output Vars to outputs
    def evaluate(self):
        # could also include support for if function is a string input
        for i,f in enumerate(self.functions):
            self.outputs[f'f{i}'] = f(*self.inputs)
        return self.outputs # final Vars containing both value and gradients
    
    def get_grad(self):
        grads = {}
        for f, var in self.outputs.items():
            grads[f] = var.dual
        return grads
    
    def get_val(self):
        vals = {}
        for f, var in self.outputs.items():
            vals[f] = var.real
        return vals
    
    def reevaluate(self, inputs): 
        self.inputs = inputs # update input values
        self.update_grads()
        return self.evaluate() # evalute
    

# Define Var Numbers class w/ methods for Fwd Pass AD
class Var():
    
    num_types = (int, float)
    
    def __init__(self, val, children=(), operation=None, tag=None): # required
        self.val = val
        self.children = children # (var1, loc_grad)
        self.adj = 0
        self.operation = operation # only used to create graph
        self.tag = tag # only used to create graph

    def __repr__(self):
        return "Var(val=%r, children=%r, adj=%r)" % (self.val,self.children,self.adj)

    def __neg__(self): # required (-)
        val = -self.val
        children = ((self, -1),)
        return Var(val, children, operation='neg')
    
    def __add__(self, other): #required (+)
        if isinstance(other, Var): 
            val = self.val + other.val
            children = ((self, 1), (other, 1))
        elif isinstance(other, Var.num_types): 
            val = self.val + other
            children = ((self, 1),(other, 0))
        else: 
            raise TypeError(f'type {type(other)} cannot be added with type Var')

        return Var(val, children, operation='add')
    
    def __radd__(self, other): 
        return self + other
    
    def __iadd__(self, other): #required (+=)
        self = self + other
        return self

    def __mul__(self, other): # required (*)
        if isinstance(other, Var): 
            val = self.val * other.val
            children = ((self, other.val), (other, self.val))
        elif isinstance(other, Var.num_types): 
            val = self.val * other
            children = ((self, other), (other, 0))
        else: 
            raise TypeError(f'type {type(other)} cannot be multiplied with type Var')
    
        return Var(val, children, operation='mul')
    
    def __rmul__(self, other):
        return self*other
    
    def __imul__(self,other): # required (*=)
        self = self * other
        return self

    def __sub__(self, other): # required (-)
        if isinstance(other, Var): 
            val = self.val - other.val
            children = ((self, 1), (other, -1))
        elif isinstance(other, Var.num_types): 
            val = self.val - other
            children = ((self, 1), (other, 0))
        else: 
            raise TypeError(f'type {type(other)} cannot be subtracted with type Var')
            
        return Var(val, children, operation='sub')
    
    def __rsub__(self, other): 
        return -self + other
    
    def __isub__(self, other): # required (-=)
        self = self - other
        return self
    
    def __truediv__(self,other): # required (\)
        if isinstance(other, Var): 
            val = self.val / other.val
            children = ((self, 1/other.val), 
                        (other, -self.val/(other.val**2)))
        elif isinstance(other, Var.num_types): 
            val = self.val / other
            children = ((self, 1/other), (other, 0))
        else: 
            raise TypeError(f'type {type(other)} cannot be divided with type Var')
            
        return Var(val, children, operation='div')

    def __rtruediv__(self, other):
        return (self**-1) * other
    
    def __itruediv__(self,other): # required (\=)
        self = self / other
        return self
    
    def __pow__(self, other): # required (**)
        if isinstance(other, Var): 
            val = self.val**other.val
            children = ((self, other.val*(self.val**(other.val-1))), 
                        (other, np.log(self.val)*(self.val**other.val)))
        elif isinstance(other, Var.num_types): 
            val = self.val**other
            children = ((self, other*(self.val**(other-1))), (other, 0))
        else: 
            raise TypeError(f'type {type(other)} cannot be pow with type Var')
            
        return Var(val, children, operation='pow')
    
    def __rpow__(self,other): 
        if isinstance(other, Var.num_types): 
            val = other**self.val
            children = ((self, np.log(other)*(other**self.val)), (other, 0))
            return Var(val, children, operation='pow')
        else: 
            raise TypeError(f'type {type(other)} cannot be pow with type Var')
                 
    def __eq__(self, other):
        if isinstance(other, Var):
            if self.val == other.val and self.children == other.children and self.operation == other.operation:
                return True
            else:
                return False
        else:
            raise TypeError(f'type {type(other)} cannot be compared with type Var')

    def __ne__(self, other):
        if isinstance(other, Var):
            return (not self == other)

        
class RevAD():
    
    def __init__(self, functions, inputs):
        self.functions = functions
        self.inputs = inputs
        self.outputs = {}
        self.variables = []
    
    # Fwd pass for RevAD and save output Vars to outputs
    def evaluate(self):
        # could also include support for if function is a string input
        for i,f in enumerate(self.functions):
            self.outputs[f'f{i}'] = f(*self.inputs)
        
        for var in self.outputs.values(): 
            var.adj = 1
            
        return self.outputs # final Vars containing both value and local gradients
    
    def get_grad(self):
        # dictionary for output
        grads = {}

        # recursively compute children
        def compute_gradients(var, path_value):
            for child, loc_grad in var.children:
                if isinstance(child, Var):
                    # "Multiply the edges of a path":
                    value_of_path_to_child = path_value * loc_grad
                    # "Add together the different paths":
                    child.adj += value_of_path_to_child
                    # recurse through graph:
                    compute_gradients(child, value_of_path_to_child)
        
        # compute gradient for each function in functions, save to dictionary for each function
        for f, var in self.outputs.items(): 
            f_i_grads = [] # dictionary to store function grdients
            compute_gradients(var, path_value=var.adj) # compute function gradients
            
            # save adjuncts for inputs in a dictionary and reset to 0 for next function
            for var in self.inputs: 
                f_i_grads.append(var.adj)
                var.adj = 0
            
            # store gradients in dictionary under function
            grads[f] = np.array(f_i_grads)
            
        # return gradients    
        return grads
    
    def get_val(self):
        # dictionary for output
        vals = {}
        
        # save output values in dictionary 
        for f, var in self.outputs.items():
            vals[f] = var.val
        return vals
    
    def reevaluate(self, inputs): 
        self.inputs = inputs # update input values
        return self.evaluate() # evalute
        
    def export_graph_info(self): 
        def _traverse(var):
    
            if len(var.children) > 0: 
                for child, loc_grad in var.children:
                    if isinstance(child, Var): 
                        _traverse(child)
                
            if var not in self.variables:
                self.variables.append(var)
        
        rows =[]
        
        for f, var in self.outputs.items():
            _traverse(var)
        
        x = 0
        v = 0
        for var in self.variables: 
            if var in self.inputs: 
                var.tag = f'x{x}'
                x += 1
            else: 
                var.tag = f'v{v}'
                v +=1
        
        for var in self.variables: 
            children_tags = []
            for child, loc_grad in var.children:
                if isinstance(child, Var):
                    children_tags.append(child.tag)
                else: 
                    children_tags.append(child)
                
            row = [var.tag, var.operation, *children_tags]
            if len(row) != 4: 
                count = 4 - len(row)
                while count > 0: 
                    row.append(None)
                    count -= 1
                
            rows.append(row)
        
        rows = np.array(rows)
            
        return rows

# elementary functions
def cos(a): # required
    if isinstance(a, Dual): 
        r = np.cos(a.real)
        d = -1*np.sin(a.real)*np.array(a.dual)
        return Dual(r, d)
    elif isinstance(a, Var):
        val = np.cos(a.val)
        children = ((a, -1*np.sin(a.val)),)
        return Var(val, children, operation='cos')
    else: 
        try: 
            return np.cos(a)
        except: 
            raise TypeError(f'cos does not support type {type(a)}')

def sin(a): # required 
    if isinstance(a, Dual): 
        r = np.sin(a.real)
        d = np.cos(a.real)*np.array(a.dual)
        return Dual(r, d)
    elif isinstance(a, Var):
        val = np.sin(a.val)
        children = ((a, np.cos(a.val)),)
        return Var(val, children, operation='sin')
    else: 
        try: 
            return np.sin(a)
        except: 
            raise TypeError(f'sin does not support type {type(a)}')

def tan(a): #required
    if isinstance(a, Dual): 
        r = np.tan(a.real)
        d = np.array(a.dual)/((np.cos(a.real))**2)
        return Dual(r, d)
    elif isinstance(a, Var):
        val = np.tan(a.val)
        children = ((a, 1/((np.cos(a.val))**2)),)
        return Var(val, children, operation='tan')
    else: 
        try: 
            return np.tan(a)
        except: 
            raise TypeError(f'tan does not support type {type(a)}')

def arccos(a):
    if isinstance(a, Dual): 
        r = np.arccos(a.real)
        d = -1/np.sqrt(1-a.real**2)*np.array(a.dual)
        return Dual(r, d)
    elif isinstance(a, Var):
        val = np.arccos(a.val)
        children = ((a, -1/np.sqrt(1-a.val**2)),)
        return Var(val, children, operation='arccos')
    else: 
        try: 
            return np.arccos(a)
        except: 
            raise TypeError(f'cos does not support type {type(a)}')

def arcsin(a):
    if isinstance(a, Dual): 
        r = np.arcsin(a.real)
        d = 1/np.sqrt(1-a.real**2)*np.array(a.dual)
        return Dual(r, d)
    elif isinstance(a, Var):
        val = np.arcsin(a.val)
        children = ((a, 1/np.sqrt(1-a.val**2)),)
        return Var(val, children, operation='arcsin')
    else: 
        try: 
            return np.arcsin(a)
        except: 
            raise TypeError(f'cos does not support type {type(a)}')

def arctan(a):
    if isinstance(a, Dual): 
        r = np.arctan(a.real)
        d = 1/(1+a.real**2)*np.array(a.dual)
        return Dual(r, d)
    elif isinstance(a, Var):
        val = np.arctan(a.val)
        children = ((a, 1/(1+a.val**2)),)
        return Var(val, children, operation='arctan')
    else: 
        try: 
            return np.arctan(a)
        except: 
            raise TypeError(f'cos does not support type {type(a)}')

def cosh(a): # update
    try: 
        return (exp(a)+exp(-a))/2
    except: 
        raise TypeError(f'cosh does not support type {type(a)}')

def sinh(a): 
    try: 
        return (exp(a)-exp(-a))/2
    except: 
        raise TypeError(f'sinh does not support type {type(a)}')

def tanh(a):
    try: 
        return (exp(a)-exp(-a))/(exp(a)+exp(-a))
    except: 
        raise TypeError(f'tanh does not support type {type(a)}')
    
def coth(a): 
    try: 
        return (exp(a)+exp(-a))/(exp(a)-exp(-a))
    except: 
        raise TypeError(f'coth does not support type {type(a)}')

def sech(a):
    try: 
        return 2/(exp(a)+exp(-a))
    except: 
        raise TypeError(f'sech does not support type {type(a)}')

def csch(a): 
    try: 
        return 2/(exp(a)-exp(-a))
    except: 
        raise TypeError(f'csch does not support type {type(a)}')

def sqrt(a):
    if isinstance(a, Dual): 
        r = np.sqrt(a.real)
        d = 1/(2*np.sqrt(a.real))*np.array(a.dual)
        return Dual(r, d)
    elif isinstance(a, Var):
        val = np.sqrt(a.val)
        children = ((a, 1/(2*np.sqrt(a.val))),)
        return Var(val, children, operation='sqrt')
    else: 
        try: 
            return np.sqrt(a)
        except: 
            raise TypeError(f'cos does not support type {type(a)}')

def exp(a): # required
    if isinstance(a, Dual): 
        r = np.exp(a.real)
        d = np.exp(a.real)*np.array(a.dual)
        return Dual(r, d)
    elif isinstance(a, Var):
        val = np.exp(a.val)
        children = ((a, np.exp(a.val)),)
        return Var(val, children, operation='exp')
    else: 
        try: 
            return np.exp(a)
        except: 
            raise TypeError(f'exp does not support type {type(a)}')

def log(a, base=np.e):
    if isinstance(a, Dual): 
        r = np.log(a.real) / np.log(base)
        d = np.array(a.dual)/(np.log(a.real)*np.log(base))
        return Dual(r, d)
    elif isinstance(a, Var):
        val = np.log(a.val) / np.log(base)
        children = ((a, 1/(np.log(a.val)*np.log(base))),)
        return Var(val, children, operation=f'log{base}')
    else: 
        try: 
            return np.log(a) / np.log(base)
        except: 
            raise TypeError(f'exp does not support type {type(a)}')

def logistic(x, k=1, x0=0, L=1):
    try: 
        return L/(1+exp(-k*(x-x0)))
    except: 
        raise TypeError(f'logistic does not support type {type(x)}')
                          
                          
                          
                          