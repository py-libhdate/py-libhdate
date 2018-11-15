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
        
    def test_repr(self, _class):
        assert _class == eval(repr(_class))
        assert _class is not eval(repr(_class))

    def test_equality(self, _class):
        class_copy = _class
        class_copy.foo = 'bar'
        assert not _class == class_copy
        assert not _class == "not a class instance"

    def test_inequality(self):
        class_copy = _class
        class_copy.foo = 'bar'
        assert not _class != class_copy
        assert _class != "not a class instance"
