# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime  # noqa: F401

import pytest

from hdate import HDate, Location, Zmanim  # noqa: F401

# pylint: disable=no-self-use
# pylint-comment: In tests, classes are just a grouping semantic


class TestClasses(object):

    CLASSES = ["HDate()", "Zmanim()", "Location()"]

    @pytest.fixture(params=CLASSES)
    def _class(self, request):
        yield eval(request.param)

    @pytest.fixture
    def _copy(self):
        def class_copy(original):
            import copy

            return copy.deepcopy(original)

        return class_copy

    def test_repr(self, _class):
        assert _class == eval(repr(_class))
        assert _class is not eval(repr(_class))

    def test_equality(self, _class, _copy):
        copy_ = _copy(_class)
        copy_.foo = "bar"
        assert not _class == copy_
        assert not _class == "not a class instance"

    def test_inequality(self, _class, _copy):
        copy_ = _copy(_class)
        copy_.foo = "bar"
        assert _class != copy_
        assert _class != "not a class instance"
