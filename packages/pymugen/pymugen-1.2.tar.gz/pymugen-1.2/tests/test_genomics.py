# -*- coding: utf-8 -*-

from unittest import TestCase

from pymugen.utils.genomics import generate_dict_values


class TestGenomics(TestCase):
    def test_generate_dict_values(self):
        symbols = ["q", "w", "e", "r"]
        mapping = {"A": "q", "C": "w", "G": "e", "T": "r"}

        result = generate_dict_values(symbols)

        self.assertEqual(mapping, result)
