# Copyright (c) Meta Platforms, Inc. and affiliates.
# SPDX-License-Identifier: GPL-3.0-or-later

import pydoc
import unittest

import drgn


class TestDocs(unittest.TestCase):
    def test_render(self):
        pydoc.render_doc(drgn)
