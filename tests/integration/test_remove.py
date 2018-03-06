# vim:ts=4:sw=4:et:
# Copyright 2012-present Facebook, Inc.
# Licensed under the Apache License, Version 2.0

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
# no unicode literals

import WatchmanTestCase
import os
import shutil
import time


@WatchmanTestCase.expand_matrix
class TestRemove(WatchmanTestCase.WatchmanTestCase):
    def test_remove(self):
        root = self.mkdtemp()
        os.makedirs(os.path.join(root, 'one', 'two'))
        self.touchRelative(root, 'one', 'onefile')
        self.touchRelative(root, 'one', 'two', 'twofile')
        self.touchRelative(root, 'top')

        self.watchmanCommand('watch', root)
        self.assertFileList(root, files=[
            'one',
            'one/onefile',
            'one/two',
            'one/two/twofile',
            'top'])

        shutil.rmtree(os.path.join(root, 'one'))

        self.assertFileList(root, files=['top'])

        self.touchRelative(root, 'one')
        self.assertFileList(root, files=['top', 'one'])

        self.removeRelative(root, 'one')
        self.assertFileList(root, files=['top'])

        shutil.rmtree(root)
        os.makedirs(os.path.join(root, 'notme'))

        self.assertWaitFor(lambda: not self.rootIsWatched(root))
