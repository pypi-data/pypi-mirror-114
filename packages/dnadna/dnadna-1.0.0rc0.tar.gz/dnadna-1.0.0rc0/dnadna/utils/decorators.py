"""Miscellaneous decorator implementations."""


from functools import lru_cache, wraps


class cached_property(property):
    """
    Read-only property that is computed once, then its computed value cached
    on the instance.

    Examples
    --------

    >>> from dnadna.utils.decorators import cached_property
    >>> class Test:
    ...     @cached_property
    ...     def expensive_property(self):
    ...         \"\"\"Computes an expensive property.\"\"\"
    ...         print('Computing expensive property (once).')
    ...         return 42
    ...
    >>> it = Test()
    >>> it.expensive_property
    Computing expensive property (once).
    42
    >>> it.expensive_property
    42

    Deleting the property simply invalidates the cache, so its value must be
    recomputed:

    >>> del it.expensive_property
    >>> it.expensive_property
    Computing expensive property (once).
    42
    >>> it.expensive_property
    42

    The `cached_property` inherits its docstring from the getter:

    >>> Test.expensive_property.__doc__
    'Computes an expensive property.'

    Inherit the `cached_property`'s module name from the getter (this is
    necessary in order to work properly with some introspection code,
    especially in the doctest framework):

    >>> Test.expensive_property.__module__ == Test.__module__
    True
    """

    sentinel = object()
    """
    A singleton object to return for missing cache values.

    Like `None`, but we don't use `None` for this purpose since it could be
    a valid return value for a property.
    """

    def __init__(self, fget):
        super().__init__(fget)
        self.key = fget.__name__
        self.__module__ = fget.__module__

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        val = self.retrieve(obj)
        if val is not self.sentinel:
            return val
        else:
            val = self.fget(obj)
            self.store(obj, val)
            return val

    def __delete__(self, obj):
        """Invalidates the cache."""

        self.invalidate(obj)

    def cache(self, obj):
        """
        Returns the cache object used to store the values of this
        property.

        Typically this is just the instance's ``__dict__``, but subclasses may
        use any kind of cache.
        """

        return obj.__dict__

    def store(self, obj, value):
        """
        Store this property's value in the object's cache.

        This can be overridden by subclasses to support different caching
        mechanisms. See for example `cached_classproperty`.
        """

        self.cache(obj)[self.key] = value

    def retrieve(self, obj):
        """
        Retrieve this property's value from the object's cache.

        This can be overridden by subclasses to support different caching
        mechanisms. See for example `cached_classproperty`.

        If the value is not found in the cache, this should return
        `cached_property.sentinel`.
        """

        return self.cache(obj).get(self.key, self.sentinel)

    def invalidate(self, obj):
        """
        Clear this property's value from the object's cache.

        If the cache was not populated to begin with this is simply a no-op.

        This can be overridden by subclasses to support different caching
        mechanisms. See for example `cached_classproperty`.

        If the value is not found in the cache, this should return
        `cached_property.sentinel`.
        """

        try:
            del self.cache(obj)[self.key]
        except KeyError:
            pass


class classproperty(property):
    """
    Simple classproperty implementation.

    Currently only supports getters.

    Examples
    --------

    >>> from dnadna.utils.decorators import classproperty
    >>> class MyClass:
    ...     @classproperty
    ...     def classname(cls):
    ...         return cls.__name__
    >>> MyClass.classname
    'MyClass'
    """

    def __init__(self, fget):
        super().__init__(fget)

    def __get__(self, obj, cls=None):
        if cls is None:
            return self

        return super().__get__(cls, type(cls))


class cached_classproperty(classproperty, cached_property):
    """
    Like `cached_property`, but for `classproperties <classproperty>`.

    Examples
    --------

    >>> from dnadna.utils.decorators import cached_classproperty
    >>> class Test:
    ...     @cached_classproperty
    ...     def expensive_property_a(cls):
    ...         \"\"\"Computes an expensive property.\"\"\"
    ...         print('Computing expensive property (once).')
    ...         return 42
    ...
    ...     @cached_classproperty
    ...     def expensive_property_b(cls):
    ...         \"\"\"Computes an expensive property.\"\"\"
    ...         print('Computing expensive property (once).')
    ...         return 777
    ...
    >>> Test.expensive_property_a
    Computing expensive property (once).
    42
    >>> Test.expensive_property_a
    42
    >>> Test.expensive_property_b
    Computing expensive property (once).
    777
    >>> Test.expensive_property_b
    777
    """

    def cache(self, obj):
        # cached_classproperty needs to use a different storage mechanism,
        # since the property itself already lives in the class's __dict__
        if not hasattr(obj, '_classproperty_cache'):
            obj._classproperty_cache = {}

        return obj._classproperty_cache


def format_docstring(*args, **kwargs):
    """
    Decorator which formats a docstring containing format variables.

    The values for variables used in the format string are passed to this
    decorator.

    Examples
    --------

    >>> from dnadna.utils.decorators import format_docstring
    >>> @format_docstring(name='Celine')
    ... def hello(name):
    ...     \"\"\"Says hello.  For example, hello({name!r}).\"\"\"
    ...     print('Hello', name)
    ...
    >>> print(hello.__doc__)
    Says hello.  For example, hello('Celine').
    """

    def decorator(func_or_cls):
        doc = func_or_cls.__doc__
        if doc:
            func_or_cls.__doc__ = doc.format(*args, **kwargs)
        return func_or_cls

    return decorator


class _HashDict(dict):
    """
    Hashable dict.

    Only works for simple cases where all values are also hashable.

    This does not guarantee immutability or an immutable hash; it is only
    mean to be used with `lru_cache_with_dict`.
    """

    def __hash__(self):
        return hash(frozenset(self.items()))


def lru_cache_with_dict(maxsize=128, typed=False):
    """
    Wrapper for `functools.lru_cache` with limited support for simple `dict`
    arguments that have immutable values.

    Examples
    --------

    >>> from dnadna.utils.decorators import lru_cache_with_dict
    >>> @lru_cache_with_dict()
    ... def sum_values(x):
    ...     print(f'adding arguments in {x}')
    ...     return sum(x.values())
    ...
    >>> sum_values({'x': 1, 'y': 2})
    adding arguments in {'x': 1, 'y': 2}
    3
    >>> sum_values({'x': 1, 'y': 2})
    3
    >>> sum_values.cache_clear()
    >>> sum_values({'x': 1, 'y': 2})
    adding arguments in {'x': 1, 'y': 2}
    3
    """

    def wrapper(func):
        def unwrap_hashdict_func(*args, **kwargs):
            # Convert _HashDict arguments back to normal dicts
            args = [(dict(a) if isinstance(a, _HashDict) else a)
                    for a in args]
            kwargs = {k: (dict(v) if isinstance(v, _HashDict) else v)
                      for k, v in kwargs.items()}
            return func(*args, **kwargs)

        cache_wrapper = lru_cache(maxsize=maxsize, typed=typed)
        cached_func = cache_wrapper(unwrap_hashdict_func)

        @wraps(func)
        def wrap_hashdict_func(*args, **kwargs):
            args = [(_HashDict(a) if isinstance(a, dict) else a)
                    for a in args]
            kwargs = {k: (_HashDict(v) if isinstance(v, dict) else v)
                      for k, v in kwargs.items()}

            return cached_func(*args, **kwargs)

        wrap_hashdict_func.cache_info = cached_func.cache_info
        wrap_hashdict_func.cache_clear = cached_func.cache_clear

        return wrap_hashdict_func

    return wrapper
