#!/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, absolute_import, print_function
from builtins import (bytes, super, range, zip, round, pow, object)

import pandas as pd


class GlobalUtil:
    bar_column = ['symbol', 'trade_date', 'time_stop', 'suspend', 'close', 'high',
                  'low', 'open', 'pre_close', 'settle', 'pre_settle',
                  'volume', 'turnover', 'total_volume', 'total_turnover', 'position']
    bar_columns = ['close', 'high',
                  'low', 'open', 'pre_close', 'settle', 'pre_settle',
                  'volume', 'turnover', 'total_volume', 'total_turnover', 'position']

    callback = {"on_initialize", "on_before_market_open",
                "on_tick", "on_first_tick", "on_bar",
                "on_handle_data", "on_terminate",
                "on_timer", "on_order_update"}

