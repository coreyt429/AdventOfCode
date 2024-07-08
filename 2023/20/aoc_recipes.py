from abc import ABCMeta, ABC, abstractmethod
from numbers import Integral as _Integral

class PropertyConfigMeta(ABCMeta):
    """This metaclass extract the atributes defined for the main class
       that would overwrite any inherited attribute that was defined with
       the @property decorator somewhere in the inheritance chain an put 
       them in the class attribute "_new_default"
       """

    def __new__(mcls, name, bases, namespace, /, **kwargs):
        #arrive at this by looking at ABCMeta implementation on _py_abc
        #source code
        
        #list the properties that the new class would inherit
        properties = {p for bcls in bases
                        for cls in bcls.__mro__
                        for p,v in vars(cls).items()
                      if isinstance(v,property)
                      }
        #procede to extract the atributes that would
        #overwrite the properties inherited by non-property
        new_default = {}
        new_namespace = {}
        for k,v in namespace.items():
            if k in properties:
                if isinstance(v,property):
                    new_namespace[k] = v
                else:
                    new_default[k] = v
            else:
                new_namespace[k] = v
        cls = super().__new__(mcls, name, bases, new_namespace, **kwargs)
        if hasattr(cls,"_new_default"):
            cls._new_default = {**cls._new_default, **new_default}
        else:
            cls._new_default = new_default
        return cls


class PropertyConfig(metaclass=PropertyConfigMeta):
    """cooperative class that transform

       class A(SomeClass):
           a = 1
           b = 2

       into

       class A(SomeClass):
           def __init__(self, *arg, a = 1, b = 2, **karg):
               super().__init__(*arg, a = a, b = b, **karg)

       so long as a and b are defined as properties in SomeClass 
       (or somewhere in the inheritance chain)

       class SomeClass:

           @property
           def a(self):
               ...

           @property
           def b(self):
               ...

        Use as

        class A(PropertyConfig, SomeClass):
           a = 1
           b = 2
       """

    def __init__(self,*arg,**kwargs):
        for k,v in self._new_default.items():
            if k not in kwargs:
                kwargs[k]=v
        super().__init__(*arg,**kwargs)



class ConfigClass(ABC):
    """Cooperative class that offer a default __repr__ method
       based on the abstract property .config"""

    @property
    @abstractmethod
    def config(self) -> dict:
        """configuration of this class"""
        return {}

    def __repr__(self):
        return f"{type(self).__name__}({', '.join( f'{k}={v!r}' for k,v in self.config.items() )})"

    def make_new(self,**new_config):
        """Create a new instance of this class with the same configuration, plus whatever change are requested"""
        c = self.config
        c.update(new_config)
        return type(self)(**c)




class PowClass(object):
    '''Mix-in class that implements implements pow(x,n,m) for n numbers.Integral'''

    def __pow__(self,n,m=None):
        '''self**n [mod m]'''
        if isinstance(n,_Integral):
            if m is not None and not m:
                raise ValueError('pow() 3rd argument cannot be 0')
            one = self.unity
            if n:
                if n==1:
                    return self if m is None else (self%m)
                if n<0:
                    if m is not None:
                        raise ValueError('pow() 2nd argument cannot be negative when 3rd argument specified')
                    return 1/pow(self,-n)
                y = one
                x = self
                while n>1:
                    if n&1: #is odd
                        y  = y*x
                        n -= 1
                    x = x*x
                    n //= 2
                    if m is not None:
                        y %= m
                        x %= m
                return ( x*y ) if m is None else ( (x*y)%m )
            return one if m is None else (one%m)
        try:
            return super().__pow__(n,m)
        except AttributeError:
            return NotImplemented
    
    @property
    def unity(self):
        """the number 1 or equivalent of this class 
           (overwrite this if the unity for your class is differente)"""
        return 1

