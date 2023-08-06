# -*- coding: utf-8 -*-

import pathlib
from unittest import TestCase

from pymugen.fasta.sequence import Sequence
from pymugen.transformers.mutationTransformer import MutationTransformer


class TestMutationParser(TestCase):
    def setUp(self) -> None:
        self.static_dir = f"{str(pathlib.Path(__file__).parent.absolute())}/static/"
        self.parser = MutationTransformer(
            f"{self.static_dir}vcfTestTransformers.vcf",
            f"{self.static_dir}test.fa.gz",
        )

        return super().setUp()

    def test_method_insertion(self):
        sequence = Sequence("ACGT", "", "ACGT")
        mutation = "ACGT"
        sequence_transformed = Sequence(
            "qwer",
            "tyui",
            "zxcv",
            ""
        )

        result = self.parser.method(sequence, mutation)

        self.assertEqual(result.prefix, sequence_transformed.prefix)
        self.assertEqual(result.infix, sequence_transformed.infix)
        self.assertEqual(result.suffix, sequence_transformed.suffix)
        self.assertEqual(result.annotations, sequence_transformed.annotations)

    def test_method_delete(self):
        sequence = Sequence("ACGT", "ACGT", "ACGT")
        mutation = ""
        sequence_transformed = Sequence(
            "qwer",
            "ghjk",
            "zxcv",
            "ACGT"
        )

        result = self.parser.method(sequence, mutation)

        self.assertEqual(result.prefix, sequence_transformed.prefix)
        self.assertEqual(result.infix, sequence_transformed.infix)
        self.assertEqual(result.suffix, sequence_transformed.suffix)
        self.assertEqual(result.annotations, sequence_transformed.annotations)

    def test_method_replace(self):
        sequence = Sequence("ACGT", "ACGT", "ACGT")
        mutation = "TGCA"
        sequence_transformed = Sequence(
            "qwer",
            "asdf",
            "zxcv",
            "ACGT"
        )

        result = self.parser.method(sequence, mutation)

        self.assertEqual(result.prefix, sequence_transformed.prefix)
        self.assertEqual(result.infix, sequence_transformed.infix)
        self.assertEqual(result.suffix, sequence_transformed.suffix)
        self.assertEqual(result.annotations, sequence_transformed.annotations)

    def test_method_mix(self):
        sequence = Sequence("ACGT", "AGCT", "ACGT")
        mutation = "GTTCAC"
        sequence_transformed = Sequence(
            "qwer",
            "uadtf",
            "zxcv",
            "AGCT"
        )

        result = self.parser.method(sequence, mutation)

        self.assertEqual(result.prefix, sequence_transformed.prefix)
        self.assertEqual(result.infix, sequence_transformed.infix)
        self.assertEqual(result.suffix, sequence_transformed.suffix)
        self.assertEqual(result.annotations, sequence_transformed.annotations)
