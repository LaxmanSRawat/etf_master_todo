def inc(x):
    return x +1

def test_answer():
    assert inc(3) == 4

# Test exception raising 
import pytest


def f():
    raise SystemExit(1)


def test_mytest():
    with pytest.raises(SystemExit):
        f()

#use the context provided by raises to assert that an expected exception is part of a raised ExceptionGroup

def g():
    raise ExceptionGroup(
        "Group message",
        [
            RuntimeError(),
        ],
    )


def test_exception_in_group():
    with pytest.raises(ExceptionGroup) as excinfo:
        g()
    assert excinfo.group_contains(RuntimeError)
    assert not excinfo.group_contains(TypeError)

# group multiple tests into a class

class TestClass:
    def test_one(self):
        x = "this"
        assert "h" in x

    # def test_two(self):
    #     x = "hello"
    #     assert hasattr(x, "check")

# be aware of when grouping tests inside classes is that each test has a unique instance of the class
class TestClassDemoInstance:
    value = 0

    def test_one(self):
        self.value = 1
        assert self.value == 1

    # def test_two(self):
    #     assert self.value == 1