from contextlib import contextmanager
from typing import Counter


class TestCase:
    def assertEqual(self, lhs, rhs, msg: str = None):
        """Test that lhs and rhs and equal"""
        if not msg:
            msg = f"{lhs} different than {rhs}"
        assert lhs == rhs, msg

    def assertNotEqual(self, lhs, rhs, msg: str = None):
        """Test that lhs and rhs are different"""
        if not msg:
            msg = f"{lhs} equal to {rhs}"
        assert lhs != rhs, msg

    def assertTrue(self, expr: bool, msg: str = None):
        """Test that expr is true"""
        if not msg:
            msg = f"expresion should be true"
        assert expr, msg

    def assertFalse(self, expr: bool, msg: str = None):
        """Test that expr is false"""
        if not msg:
            msg = f"expresion should be false"
        assert not expr, msg

    def assertIs(self, lhs, rhs, msg: str = None):
        """Test that lhs and rhs are the same object"""
        if not msg:
            msg = f"{lhs} is not {rhs}"
        assert lhs is rhs, msg

    def assertIsNot(self, lhs, rhs, msg: str = None):
        """Test that lhs and rhs are different objects"""
        if not msg:
            msg = f"{lhs} is {rhs}"
        assert lhs is not rhs, msg

    def assertIsNone(self, expr, msg: str = None):
        """Test that expr is None"""
        if not msg:
            msg = f"{expr} is not None"
        assert expr is None, msg

    def assertIsNotNone(self, expr, msg: str = None):
        """Test that expr is not None"""
        if not msg:
            msg = f"{expr} is not None"
        assert expr is not None, f"{expr} is None"

    def assertIn(self, member, container, msg: str = None):
        """Test that member is in container"""
        if not msg:
            msg = f"{member} not in {container}"
        assert member in container, msg

    def assertNotIn(self, member, container, msg: str = None):
        """Test that member is not in container"""
        if not msg:
            msg = f"{member} in {container}"
        assert member not in container, msg

    def assertIsInstance(self, obj, cls: type, msg: str = None):
        """Test that obj an instance of cls"""
        if not msg:
            msg = f"{obj} is not instance of {cls}"
        assert isinstance(obj, cls), msg

    def assertIsNotInstance(self, obj, cls: type, msg: str = None):
        """Test that obj is not an instance of cls"""
        if not msg:
            msg = f"{obj} is instance of {cls}"
        assert not isinstance(obj, cls), msg

    def assertAlmostEqual(self, lhs, rhs, msg: str = None):
        """Test that lhs and rhs are approximately equal"""
        if not msg:
            msg = f"{lhs} not almost equal to {rhs}"
        assert round(lhs - rhs, 7) == 0, msg

    def assertNotAlmostEqual(self, lhs, rhs, msg: str = None):
        """Test that lhs and rhs are not approximately equal"""
        if not msg:
            msg = f"{lhs} almost equal to {rhs}"
        assert round(lhs - rhs, 7) != 0, msg

    def assertGreater(self, lhs, rhs, msg: str = None):
        """Test that lhs is greater than rhs"""
        if not msg:
            msg = f"{lhs} not greater than  {rhs}"
        assert lhs > rhs, msg

    def assertGreaterEqual(self, lhs, rhs, msg: str = None):
        """Test that lhs is greater than or equal to rhs"""
        if not msg:
            msg = f"{lhs} not greater than or equal to {rhs}"
        assert lhs >= rhs, msg

    def assertSmaller(self, lhs, rhs, msg: str = None):
        """Test that lhs is smaller than rhs"""
        if not msg:
            msg = f"{lhs} not smaller than  {rhs}"
        assert lhs < rhs, msg

    def assertSmallerEqual(self, lhs, rhs, msg: str = None):
        """Test that lhs is smaller than or equal to rhs"""
        if not msg:
            msg = f"{lhs} not smaller than or equal to {rhs}"
        assert lhs <= rhs, msg

    @contextmanager
    def assertRaises(self, exception: type, msg1: str = None, msg2: str = None):
        """Test that an expression is raised"""
        if not msg1:
            msg1 = "raised {} exception"

        if not msg2:
            msg2 = "no exception raised"
        try:
            yield
        except Exception as ex:
            assert type(ex) == exception, msg1.format(type(ex).__name__)
        else:
            assert False, msg2

    def assertSequenceEqual(self, rhs, lhs, msg: str = None):
        """Test that two sequences are equal"""
        if not msg:
            msg = "sequence are different"

        assert len(rhs) == len(lhs) and sorted(rhs) == sorted(lhs), msg

    def assertSequenceNotEqual(self, rhs, lhs, msg: str = None):
        """Test that two sequences are not equal"""
        if not msg:
            msg = "sequence equal"

        assert len(rhs) != len(lhs) or sorted(rhs) != sorted(lhs), msg

    def assertListEqual(self, rhs, lhs, msg: str = None):
        """Test that two lists are equal"""
        if not msg:
            msg = "lists are different"

        assert len(rhs) == len(lhs) and sorted(rhs) == sorted(lhs), msg

    def assertListNotEqual(self, rhs, lhs, msg: str = None):
        """Test that two lists are not equal"""
        if not msg:
            msg = "lists are equal"

        assert len(rhs) != len(lhs) or sorted(rhs) != sorted(lhs), msg

    def assertTupleEqual(self, rhs, lhs, msg: str = None):
        """Test that two tuples are equal"""
        if not msg:
            msg = "tuples are different"

        assert len(rhs) == len(lhs) and sorted(rhs) == sorted(lhs), msg

    def assertTupleNotEqual(self, rhs, lhs, msg: str = None):
        """Test that two tuples are not equal"""
        if not msg:
            msg = "tuples are equal"

        assert len(rhs) != len(lhs) or sorted(rhs) != sorted(lhs), msg

    def assertSetEqual(self, rhs, lhs, msg: str = None):
        """Test that two sets are equal"""
        if not msg:
            msg = "sets are different"

        assert rhs == lhs, msg

    def assertSetNotEqual(self, rhs, lhs, msg: str = None):
        """Test that two sets are not equal"""
        if not msg:
            msg = "sets are equal"

        assert rhs != lhs, msg

    def assertDictEqual(self, rhs, lhs, msg: str = None):
        """Test that two dictionaries are equal"""
        if not msg:
            msg = "dictionaries are different"

        assert rhs == lhs, msg

    def assertDictNotEqual(self, rhs, lhs, msg: str = None):
        """Test that two dictionaries are not equal"""
        if not msg:
            msg = "dictionaries are equal"

        assert rhs != lhs, msg

    def assertCountEqual(self, rhs, lhs, msg: str = None):
        """Test that two sequences contains the sames elements"""
        if not msg:
            msg = "sequences contains different elements"

        assert Counter(list(rhs)) == Counter(list(lhs)), msg
