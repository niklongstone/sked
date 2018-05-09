"""Tests for main sked CLI module."""

from subprocess import PIPE, Popen as popen
from unittest import TestCase
from sked import __version__ as VERSION


class TestHelp(TestCase):
    def test_returns_usage_information(self):
        output = popen(['sked', '-h'], stdout=PIPE).communicate()[0]
        self.assertTrue(b'Usage:' in output)

        output = popen(['sked', '--help'], stdout=PIPE).communicate()[0]
        self.assertTrue(b'Usage:' in output)


class TestVersion(TestCase):
    def test_returns_version_information(self):
        output = popen(['sked', '--version'], stdout=PIPE).communicate()[0]
        self.assertEqual(output.strip(), str.encode(VERSION))
