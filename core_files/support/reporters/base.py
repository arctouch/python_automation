# Copyright 2020 ArcTouch LLC (authored by Thiago Werner at ArcTouch)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
# -*- coding: utf-8 -*-

from behave.model_core import Status

class Reporter(object):
    """
    Base class for all reporters.
    A reporter provides an extension point (variant point) for the runner logic.
    A reporter is called after a model element is processed
    (and its result status is known).
    Otherwise, a reporter is similar to a formatter, but it has a simpler API.

    Processing Logic (simplified)::

        config.reporters = ...  #< Configuration (and provision).
        runner.run():
            for feature in runner.features:
                feature.run()     # And feature scenarios, too.
                for reporter in config.reporters:
                    reporter.feature(feature)
            # -- FINALLY:
            for reporter in config.reporters:
                reporter.end()

    An existing formatter can be reused as reporter by using
    :class:`behave.report.formatter_reporter.FormatterAsReporter`.
    """

    def __init__(self, config):
        self.config = config

    def feature(self, feature):     # pylint: disable=no-self-use
        """
        Called after a feature was processed.

        :param feature:  Feature object (as :class:`behave.model.Feature`)
        """
        assert feature.status != Status.undefined
        raise NotImplementedError

    def end(self):
        """
        Called after all model elements are processed (optional-hook).
        """
        pass
