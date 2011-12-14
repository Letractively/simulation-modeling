# -*- coding: utf-8 -*-

import os, sys
tests = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(tests))

import unittest
from models.kiosk import kiosk

revenue_mean = [[3000] * 3] * 3
damage       = [3000] * 3

kiosk(revenue_mean, damage, [0.5, 0.9, 0.1], 0.25, -1, 2, 10)
