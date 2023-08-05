from pytest import raises, warns

from dprop import depends_on, dprop, idprop, independent


class Class:
    a = independent(int)

    @depends_on(a)
    def b(self):
        return 6 * self.a + self.d

    c = idprop()

    @depends_on(c)
    def d(self):
        return self.c + 1

    @dprop
    def e(self):
        return 2 * self.d

    b.depends_on(d)
    e.depends_on(d)


def test_classvartypes():
    assert isinstance(Class.a, idprop)
    assert isinstance(Class.b, dprop)
    assert isinstance(Class.c, idprop)
    assert isinstance(Class.d, dprop)
    assert isinstance(Class.e, dprop)


def test_graph():
    assert Class.a.dependents == {Class.b}
    assert Class.b.dependents == set()
    assert Class.b.dependencies == {Class.a, Class.d}
    assert Class.c.dependents == {Class.d}
    assert Class.d.dependents == {Class.b, Class.e}
    assert Class.d.dependencies == {Class.c}
    assert Class.e.dependents == set()
    assert Class.e.dependencies == {Class.d}


def test_unset_indep():
    inst = Class()

    with raises(AttributeError):
        _ = inst.a

    with raises(AttributeError):
        _ = inst.b

    inst.a = 1
    assert inst.a == 1
    del inst.a

    with raises(AttributeError):
        _ = inst.a


def test_mechanics():
    inst = Class()
    inst.a = 1
    inst.c = 2

    assert not Class.b.get_value(inst).valid
    assert not Class.d.get_value(inst).valid
    assert not Class.e.get_value(inst).valid

    assert inst.a == 1
    assert inst.b == 9
    assert inst.c == 2
    assert inst.d == 3

    assert Class.b.get_value(inst).valid
    assert Class.d.get_value(inst).valid
    assert not Class.e.get_value(inst).valid

    assert inst.e == 2 * inst.d
    assert Class.e.get_value(inst).valid

    inst.a = 2

    assert not Class.b.get_value(inst).valid
    assert Class.d.get_value(inst).valid
    assert Class.e.get_value(inst).valid

    assert inst.b == 15


def test_setting_dprops():
    inst = Class()

    inst.c = 1
    assert inst.d == 2
    assert inst.e == 4

    with warns(RuntimeWarning):
        inst.d = 3

    assert inst.d == 3
    assert inst.c == 1
    assert not Class.e.get_value(inst).valid
    assert inst.e == 6
