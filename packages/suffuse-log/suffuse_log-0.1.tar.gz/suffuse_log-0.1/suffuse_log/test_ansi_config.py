import unittest

from .ansi_config import AnsiConfig


class TestAnsiConfig(unittest.TestCase):
    def test_style(self):

        input_ = "value with spaces and , | complex / characters "
        styles = ("red_fore", "blue_back")

        actual = AnsiConfig.style(input_, styles)
        expected = "\x1b[31m\x1b[44mvalue with spaces and , | complex / characters \x1b[0m"

        self.assertEqual(actual, expected)
