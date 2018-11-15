# -*- coding: utf-8 -*-

from __future__ import print_function

import datetime

import pytest
from dateutil.tz import tzfile

from hdate import HDate, Zmanim, Location

# pylint: disable=no-self-use
# pylint-comment: In tests, classes are just a grouping semantic

class TestClasses(object):

    CLASSES = ['HDate()', 'Zmanim()', 'Location()']

    @pytest.fixture(params=CLASSES)
    def _class(self, request):
        yield eval(request.param)

    @pytest.fixture
    def _copy(self):
        def class_copy(original):
            import copy
            yield copy.deepcopy(original)
        
    def test_repr(self, _class):
        assert _class == eval(repr(_class))
        assert _class is not eval(repr(_class))

    def test_equality(self, _class, _copy):
        _copy.foo = 'bar'
        assert not _class == _copy
        assert not _class == "not a class instance"

    def test_inequality(self, _class, _copy):
        _copy.foo = 'bar'
        assert not _class != _copy
        assert _class != "not a class instance"
