# decoratemethod

Let function decorator decorate the bound method for each instance.

## Usage

### lru_cache

To let each instance has their own lru cache:

``` py
from functools import lru_cache
from decoratemethod import decorate

class Foo:
    @decorate(lru_cache)
    def decorated_method(self, x):
        ...
```
