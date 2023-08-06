#!/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function
from builtins import (bytes, super, range, zip, round, pow, object)

class PriceUtil:
    _EPSILON = 0.000001

    @staticmethod
    def equal(x, y, epsilon=_EPSILON):
        return abs(x - y) < epsilon

    @staticmethod
    def greater_than(x, y):
        return x - y > PriceUtil._EPSILON

    @staticmethod
    def less_than(x, y):
        return y - x > PriceUtil._EPSILON

    @staticmethod
    def equal_greater_than(x, y):
        return PriceUtil.equal(x, y) or PriceUtil.greater_than(x, y)

    @staticmethod
    def equal_less_than(x, y):
        return PriceUtil.equal(x, y) or PriceUtil.less_than(x, y)

    @staticmethod
    def compare(x, y):
        if PriceUtil.equal(x, y):
            return 0
        elif PriceUtil.greater_than(x, y):
            return 1
        else:
            return -1

    @staticmethod
    def valid_price(price):
        return PriceUtil.greater_than(price, 0)

    @staticmethod
    def is_zero(x):
        return PriceUtil.equal(x, 0)

    @staticmethod
    def same_side(x, y):
        return ((PriceUtil.equal_greater_than(x, 0) and PriceUtil.equal_greater_than(y, 0)) or
                (PriceUtil.equal_less_than(x, 0) and PriceUtil.equal_less_than(y, 0))
                )

class price_util(PriceUtil):
    pass