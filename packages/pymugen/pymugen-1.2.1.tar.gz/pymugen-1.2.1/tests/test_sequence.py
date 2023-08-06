# -*- coding: utf-8 -*-

from unittest import TestCase

from pymugen.fasta.sequence import Sequence


class TestMutationParser(TestCase):
    def setUp(self) -> None:
        self.sequence = Sequence("aaa", "bbb", "ccc", "ddd")
        return super().setUp()

    def test_from_string(self):
        sequence_string = str(self.sequence)

        result = Sequence.from_string(sequence_string)

        self.assertEqual(result.prefix, self.sequence.prefix)
        self.assertEqual(result.infix, self.sequence.infix)
        self.assertEqual(result.suffix, self.sequence.suffix)
        self.assertEqual(result.annotations, self.sequence.annotations)
    
    def test_from_string_no_annotation(self):
        sequence = Sequence("aaa", "bbb", "ccc")
        sequence_string = str(sequence)

        result = Sequence.from_string(sequence_string)

        self.assertEqual(result.prefix, sequence.prefix)
        self.assertEqual(result.infix, sequence.infix)
        self.assertEqual(result.suffix, sequence.suffix)
        self.assertEqual(result.annotations, sequence.annotations)
    
    def test_from_string_chromosome(self):
        sequence = Sequence("aaa", "bbb", "ccc", "ddd", "chr1")
        sequence_string = str(sequence)

        result = Sequence.from_string(sequence_string)

        self.assertEqual(result.prefix, sequence.prefix)
        self.assertEqual(result.infix, sequence.infix)
        self.assertEqual(result.suffix, sequence.suffix)
        self.assertEqual(result.annotations, sequence.annotations)

    def test_from_string_no_annotation_chromosome(self):
        sequence = Sequence("aaa", "bbb", "ccc", "", "chr1")
        sequence_string = str(sequence)

        result = Sequence.from_string(sequence_string)

        self.assertEqual(result.prefix, sequence.prefix)
        self.assertEqual(result.infix, sequence.infix)
        self.assertEqual(result.suffix, sequence.suffix)
        self.assertEqual(result.annotations, sequence.annotations)

    def test__sequence_part_str(self):
        sequence_part = "aaa"
        sequence_part_str = f"a-a-a"

        result = self.sequence._sequence_part_str(sequence_part)

        self.assertEqual(result, sequence_part_str)

    def test___str__(self):
        sequence_str = f"""ddd|a-a-a,b-b-b,c-c-c"""

        result = str(self.sequence)

        self.assertEqual(result, sequence_str)

    def test___str__no_annotations(self):
        sequence = Sequence("aaa", "bbb", "ccc")
        sequence_str = f"""a-a-a,b-b-b,c-c-c"""

        result = str(sequence)

        self.assertEqual(result, sequence_str)

    def test___str__chromosme(self):
        sequence = Sequence("aaa", "bbb", "ccc", "ddd", "chr1")
        sequence_str = f"""chr1/ddd|a-a-a,b-b-b,c-c-c"""

        result = str(sequence)

        self.assertEqual(result, sequence_str)

    def test___getitem__1(self):
        sequence_symbols = "aaa"

        result = self.sequence[0]

        self.assertEqual(result, sequence_symbols)

    def test___getitem__2(self):
        sequence_symbols = "bbbccc"

        result = self.sequence[1:]

        self.assertEqual(result, sequence_symbols)


    def test___getitem__3(self):
        sequence_symbols = "aaabbb"

        result = self.sequence[:2]

        self.assertEqual(result, sequence_symbols)

    def test___getitem__4(self):
        sequence_symbols = "bbb"

        result = self.sequence[1:2]

        self.assertEqual(result, sequence_symbols)

    def test___getitem__5(self):
        sequence_symbols = "aaabbbccc"

        result = self.sequence[:]

        self.assertEqual(result, sequence_symbols)

    def test___getitem__6(self):
        error = False

        try:
            self.sequence[5]
        except:
            error = True

        self.assertTrue(error)

    def test___getitem__7(self):
        error = False

        try:
            self.sequence[-1]
        except:
            error = True

        self.assertTrue(error)
