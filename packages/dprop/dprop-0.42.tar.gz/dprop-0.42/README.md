## dprop
#### *Everything is connected, maan!*

----------

This tiny package implements the notion of "dependent properties", whose values
are computed based on other properties and cached for re-use, but then smartly
invalidated when a `(great-)*(grand)?parent` property's value changes.

Here is a simple example:

```python
from dprop import independent, depends_on    

class Class:
    a = independent(float)  # type info optional

    @depends_on(a)
    def b(self):
        print('computing b')
        return 6 * self.a

    def __init__(self, a: float):
        # independent properties can be set inside and outside the class as usual
        self.a = a


inst = Class(7)
assert inst.a == 7
assert inst.b == 42  # prints "computing b"

assert inst.b == 42  # value is re-used! (nothing printed)


# Re-setting an independent property invalidates (does not actually delete,
# though) all "later" properties.
inst.a = 26/6
assert inst.b == 26  # prints "computing b"
```
