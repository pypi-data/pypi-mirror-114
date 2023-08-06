# -*- coding: utf-8 -*-

import pathlib
from unittest import TestCase
from unittest.mock import mock_open, patch

from pymugen.fasta.sequence import Sequence
from pymugen.transformers.extendedTransformer import ExtendedTransformer


class TestExtendedParserVcf_ParserVcf(TestCase):
    def setUp(self) -> None:
        self.static_dir = f"{str(pathlib.Path(__file__).parent.absolute())}/static/"
        self.parser = ExtendedTransformer(
            f"{self.static_dir}vcfTestTransformers.vcf",
            f"{self.static_dir}test.fa.gz",
        )

        return super().setUp()

    def test_name(self):
        name = "extended"

        result = self.parser.name

        self.assertEqual(result, name)

    def test_filename(self):
        filename = "transformed_extended_data.pvcf"

        result = self.parser.filename

        self.assertEqual(result, filename)

    def test_method(self):
        sequence = Sequence("ACGT", "ACGT", "ACGT")
        mutation = "TGCA"
        sequence_transformed = Sequence("qwer", "fdsa", "zxcv", "ACGT")

        result = self.parser.method(sequence, mutation)

        self.assertEqual(result.prefix, sequence_transformed.prefix)
        self.assertEqual(result.infix, sequence_transformed.infix)
        self.assertEqual(result.suffix, sequence_transformed.suffix)
        self.assertEqual(result.annotations, sequence_transformed.annotations)

    def test_generate_sequences(self):
        sequences = [
            "G|,a,x-z-v-c-x",
            "G|r-e-w-q-r,f-a,x-z-v-c-x",
            "T|q-r-e-w-q,s,c",
            "T|,a,c-z-x-v-c",
            "T|w-r-e-q-w,f-a,c-z-x-v-c",
            "T|w-r-e-q-w,s,c-z-x-v-c",
        ]
        with patch("builtins.open", mock_open(read_data="data")):
            result = self.parser.generate_sequences("")

        self.assertEqual(result, sequences)

    def test_generate_sequences_chromosome(self):
        sequences = [
            "chr1/G|,a,x-z-v-c-x",
            "chr1/G|r-e-w-q-r,f-a,x-z-v-c-x",
            "chr1/T|q-r-e-w-q,s,c",
            "chr2/T|,a,c-z-x-v-c",
            "chr2/T|w-r-e-q-w,f-a,c-z-x-v-c",
            "chr2/T|w-r-e-q-w,s,c-z-x-v-c",
        ]
        with patch("builtins.open", mock_open(read_data="data")):
            result = self.parser.generate_sequences("", chromosome=True)

        self.assertEqual(result, sequences)

    def test_generate_sequences_original(self):
        sequences = [
            (',G,C-A-T-G-C', 'G|,a,x-z-v-c-x'),
            ('T-G-C-A-T,G,C-A-T-G-C', 'G|r-e-w-q-r,f-a,x-z-v-c-x'),
            ('A-T-G-C-A,T,G', 'T|q-r-e-w-q,s,c'),
            (',T,G-A-C-T-G', 'T|,a,c-z-x-v-c'),
            ('C-T-G-A-C,T,G-A-C-T-G', 'T|w-r-e-q-w,f-a,c-z-x-v-c'),
            ('C-T-G-A-C,T,G-A-C-T-G', 'T|w-r-e-q-w,s,c-z-x-v-c')
        ]
        with patch("builtins.open", mock_open(read_data="data")):
            result = self.parser.generate_sequences("", original=True)

        self.assertEqual(result, sequences)

    def test_retrive_sequence(self):
        sequence = "chr1/G|,a,x-z-v-c-x"
        sequence_transformed = Sequence("", "a", "xzvcx", "G", "chr1")

        result = ExtendedTransformer.retrive_sequence(sequence)

        self.assertEqual(result.prefix, sequence_transformed.prefix)
        self.assertEqual(result.infix, sequence_transformed.infix)
        self.assertEqual(result.suffix, sequence_transformed.suffix)
        self.assertEqual(result.annotations, sequence_transformed.annotations)
        self.assertEqual(result.chromosome, sequence_transformed.chromosome)

    def test_retrive_sequence_original(self):
        sequence = "chr1/,G,C-A-T-G-C\nchr1/G|,a,x-z-v-c-x"
        sequence_transformed = Sequence("", "a", "xzvcx", "G", "chr1")
        sequence_original_transformed = Sequence("", "G", "CATGC", "", "chr1")

        result = ExtendedTransformer.retrive_sequence(sequence)

        self.assertEqual(result[0].prefix, sequence_original_transformed.prefix)
        self.assertEqual(result[0].infix, sequence_original_transformed.infix)
        self.assertEqual(result[0].suffix, sequence_original_transformed.suffix)
        self.assertEqual(result[0].annotations, sequence_original_transformed.annotations)
        self.assertEqual(result[0].chromosome, sequence_original_transformed.chromosome)
        self.assertEqual(result[1].prefix, sequence_transformed.prefix)
        self.assertEqual(result[1].infix, sequence_transformed.infix)
        self.assertEqual(result[1].suffix, sequence_transformed.suffix)
        self.assertEqual(result[1].annotations, sequence_transformed.annotations)
        self.assertEqual(result[1].chromosome, sequence_transformed.chromosome)
