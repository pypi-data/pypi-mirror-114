# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Sequence, Union

from pymugen.fasta.fastaReader import FastaReader
from pymugen.fasta.sequence import Sequence
from vcf import Reader as VcfReader


class Transformer(ABC):
    """Transforms data from a VCF file using a FASTA file.

    The transformer needs to define a method named `method`, which generates a new
    sequence from the original one with different notation.

    For example, if we have the sequence `abbc = Sequence(a, bb, c)` and the mutation
    `aa` this `method` changes it into another representation, for example to
    `smms = Sequence(s, mm, s, bb)`, where the mutation will be added and transformed
    and the reference infix is saved as annotation.

    ```python
        Sequence("s", "mm", "s", "b") = method(Sequence("a", "b", "c"), "bb")
    ```

    Parameters
    ----------
    vcf_path: str
        Path of the vcf file.
    fasta_path: str
        Path of the fasta file.
    """

    fasta_reader: FastaReader = None
    _sequences_separator: str = "\n"

    def __init__(self, vcf_path: str, fasta_path: str):
        self.vcf = VcfReader(open(vcf_path, "r"))
        self.fasta_reader = FastaReader(fasta_path)

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the transformer."""
        pass

    @property
    def filename(self) -> str:
        """Default filename for the results."""
        return f"transformed_{self.name}_data.pvcf"

    @abstractmethod
    def method(self, sequence: Sequence, mutation: str) -> Sequence:
        """Transforms the sequence with a given mutation to a new sequence with
        different notation.

        For example, if we have the sequence `abbc = Sequence(a, bb, c)` and the
        mutation `aa` this `method` changes it into another representation, for example
        to `smms = Sequence(s, mm, s, bb)`, where the mutation will be added and
        transformed and the reference infix is saved as annotation.

        ```python
            Sequence("s", "mm", "s", "b") = method(Sequence("a", "b", "c"), "bb")
        ```

        Parameters
        ----------
        sequence: Sequence
            Sequence.
        muatation: str
            Mutation.

        Returns
        -------
        Transformed sequence.
        """
        pass

    def generate_sequences(
        self,
        path: str,
        prefix_length: int = 5,
        suffix_length: int = 5,
        chromosome: bool = False,
        filename: str = False,
        original: bool = False
    ):
        """Generates a file with the mutated sequences using the method `method` for
        transform the sequence and the mutation and returns a list of sequence or pairs
        of sequences if the parameter orignal is set to True.

        Parameters
        ----------
        path: str
            Path to store the data.
        prefix_length: int = 5
            Length of the prefix.
        suffix_length: int = 5
            Length of the suffix.
        chromosome: bool = False
            If true add the chromosome where the sequences is from into the file.
        filename: str = default_filename
            Filename of the result file.
        original: bool = True
            Adds the original sequence into the file and changes the result from a list
            of sequences to a list of pairs of sequences, where the first sequence is
            the orignal and the second the transformed

        Returns
        -------
        Transformed sequences from vcf.
        """

        if not filename:
            filename = self.filename

        sequences = []
        with open(f"{path}/{filename}", "w") as transformed_data_file:
            for i in self.vcf:
                sequence = self.fasta_reader.sequence(
                    i.CHROM, i.POS - 1, prefix_length, suffix_length, len(i.REF)
                )

                assert sequence.infix.upper() == i.REF.upper()

                if chromosome:
                    sequence.chromosome = i.CHROM

                transformed_sequence = self.method(sequence, i.ALT[0].sequence)

                result = str(transformed_sequence)
                element = result
                if original:
                    result = f"{sequence}{self._sequences_separator}{result}"
                    element = (str(sequence), element)

                sequences.append(element)
                transformed_data_file.write(result)

        return sequences

    @classmethod
    def retrive_sequence(cls, sequence: str) -> Sequence:
        """Retrive a string sequence into a sequence object.

        Parameters
        ----------
        sequence: str
            Sequence in a string format.

        Returns
        -------
        Sequence or sequences.
        """
        if cls._sequences_separator in sequence:
            original, sequence = sequence.split(cls._sequences_separator)
            return (Sequence.from_string(original), Sequence.from_string(sequence))
        return Sequence.from_string(sequence)
