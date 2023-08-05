import unittest

from . import ansi_swatch


class TestAnsiSwatch(unittest.TestCase):
    def setUp(self):
        ansi_swatch.load_ansi_map()

    def test_user_provided_ansi_map(self):
        """Assert that overriding the default dict modifies the value as we expect."""
        user_provided = {"my_key": "my_value"}

        ansi_swatch.load_ansi_map(user_provided)

        self.assertEqual(user_provided, ansi_swatch.ANSI_MAP)

    def test_default_ansi_map(self):
        """Assert that the default dict has keys in the format we expect."""

        for key in (
            "red_fore",
            "dim_style",
            "blue_back",
        ):
            ansi_swatch.ANSI_MAP[key]
