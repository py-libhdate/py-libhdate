"""Tests for common classes."""

# Imports are needed for evaluating the class.
# pylint: disable=unused-import
# It is OK for these test cases to use eval.
# pylint: disable=eval-used
import copy
import datetime  # noqa: F401

import pytest

from hdate import HDate, Location, Zmanim  # noqa: F401

# pylint-comment: In tests, classes are just a grouping semantic


class TestClasses:
    """Wrapper class for tests."""

    CLASSES = ["HDate()", "Zmanim()", "Location()"]

    @pytest.fixture(params=CLASSES)
    def _class(self, request):
        yield eval(request.param)

    @pytest.fixture
    def _copy(self):
        def class_copy(original):
            return copy.deepcopy(original)

        return class_copy

    def test_repr(self, _class):
        """Test that eval of repr returns a class equal to the class itself."""
        assert _class == eval(repr(_class))
        assert _class is not eval(repr(_class))

    def test_equality(self, _class, _copy):
        """Test classes to be equal."""
        copy_ = _copy(_class)
        copy_.foo = "bar"
        assert not _class == copy_
        assert not _class == "not a class instance"

    def test_inequality(self, _class, _copy):
        """Test inequality."""
        copy_ = _copy(_class)
        copy_.foo = "bar"
        assert _class != copy_
        assert _class != "not a class instance"
