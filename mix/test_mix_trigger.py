#!/usr/bin/env python

from datetime import datetime

from jubatest import *
from jubatest.log import LogLevel

class MixTriggerTestBase(object):
    @classmethod
    def setUpCluster(cls, env):
        cls.node0 = env.get_node(0)
        cls.cluster = env.cluster(CLASSIFIER, default_config(CLASSIFIER))

        options = []
        (interval_sec, interval_count) = cls.get_intervals()
        if interval_sec is not None:
            options += [('--interval_sec', interval_sec)]
        if interval_count is not None:
            options += [('--interval_count', interval_count)]
        cls.server0 = env.server(cls.node0, cls.cluster, options)

    def send_datum(self, cli, count):
        d = self.server0.types.datum([('foo', 'bar')], [])
        for i in range(count):
            cli.train([('label', d)])

    def mix_logs(self, target):
        return target.log().message('mixed with ').get()

# ----------------------- #

class MixTriggerDisabledTest(JubaTestCase, MixTriggerTestBase):
    @classmethod
    def get_intervals(cls):
        return (0, 0)

    def test(self):
        """
        Test that MIX is not triggered.
        """
        with self.server0 as cli:
            self.send_datum(cli, 513)
            sleep(17)
        self.assertEqual(0, len(self.mix_logs(self.server0)))

# ----------------------- #

def createMixTriggerTimerOnlyTest(interval_sec):
    class MixTriggerTimerOnlyTestBase(MixTriggerTestBase):
        @classmethod
        def get_intervals(cls):
            return (interval_sec, 0)

        def test(self):
            """
            Test that MIX is correctly triggered in interval_sec seconds.
            """
            with self.server0 as cli:
                sleep(interval_sec)
            self.assertEqual(1, len(self.mix_logs(self.server0)))
    return MixTriggerTimerOnlyTestBase

class MixTriggerTimerOnly_1_Test(JubaTestCase, createMixTriggerTimerOnlyTest(4)):   pass
class MixTriggerTimerOnly_16_Test(JubaTestCase, createMixTriggerTimerOnlyTest(16)): pass
class MixTriggerTimerOnly_32_Test(JubaTestCase, createMixTriggerTimerOnlyTest(32)): pass

# ----------------------- #

def createMixTriggerCounterOnlyTest(interval_count):
    class MixTriggerCounterOnlyTestBase(MixTriggerTestBase):
        @classmethod
        def get_intervals(cls):
            return (0, interval_count)

        def test(self):
            """
            Test that MIX is correctly triggered after interval_count requests.
            """
            with self.server0 as cli:
                self.send_datum(cli, interval_count)
                sleep(1) # allow MIX to begin
            self.assertEqual(1, len(self.mix_logs(self.server0)))
    return MixTriggerCounterOnlyTestBase

class MixTriggerCounterOnly_1_Test(JubaTestCase, createMixTriggerCounterOnlyTest(1)):       pass
class MixTriggerCounterOnly_512_Test(JubaTestCase, createMixTriggerCounterOnlyTest(512)):   pass
class MixTriggerCounterOnly_1024_Test(JubaTestCase, createMixTriggerCounterOnlyTest(1024)): pass

# ----------------------- #

class MixTriggerTimerCounterTest(JubaTestCase, MixTriggerTestBase):
    @classmethod
    def get_intervals(cls):
        return (8, 256)

    def test(self):
        """
        Test that MIX is correctly triggered by both interval_sec and interval_count
        """
        with self.server0 as cli:
            begin = datetime.now()

            # Trigger Counter
            def _send_request():
                self.send_datum(cli, 256)
                sleep(1) # allow MIX to begin
            (result, timeLeft) = self.assertRunsWithin(8, _send_request)
            first_mix = datetime.now()

            # Trigger Timer
            sleep(timeLeft)
            sleep(1) # allow MIX to begin
            second_mix = datetime.now()
        first_mix_logs = self.server0.log().time_range(begin, first_mix).message('mixed with').get()
        self.assertEqual(1, len(first_mix_logs))
        second_mix_logs = self.server0.log().consume(first_mix_logs[0]).message('mixed with').get()
        self.assertEqual(1, len(second_mix_logs))
