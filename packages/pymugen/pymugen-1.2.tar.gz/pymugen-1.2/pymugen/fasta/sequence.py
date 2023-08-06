class Sequence(object):
    """Class that represents a genomic sequence. It has three elements, a prefix an
    infix and a suffix. In addition, the sequence has two attributes, one for the
    chromosome where the sequence is in and the other for annotations.

    This sequence can be represented as a string with the next format:

    ```
    chr/annotations|symbol_p_1-symbol_p_n,symbol_m_1-symbol_m_n,symbol_s_1-symbol_n_1
    ```

    The sequence can be accessed as a list of three elements, where each element is one
    part of the examples, for example:

    ```python
    sequence = Sequence("aaa", "bbb", "ccc")

    sequence[1]
    >>> bbb

    sequence[0:2]
    >>> aaabbb

    sequence[:]
    >>> aaabbbccc
    ```

    The literal symbols can be changed by inheriting the class and changing these
    variables:

     - `_prefix_suffix_separator = "|"`
     - `_sequence_part_separator = ","`
     - `_symbol_sequence_separator = "-"`
     - `_chromosome_separator = "/"`
    
    Parameters
    ----------
    prefix: str
        Prefix of the sequence.
    infix: str
        Infix of the sequence.
    suffix: str
        Suffix of the sequence.
    annotations: str = ""
        Annotations of the sequence.
    chromosome: str = ""
        Chromosome of the sequence.
    """

    _prefix_separator: str = "|"
    _sequence_part_separator: str = ","
    _symbol_sequence_separator: str = "-"
    _chromosome_separator: str = "/"

    def __init__(
        self,
        prefix: str,
        infix: str,
        suffix: str,
        annotations: str = "",
        chromosome: str = "",
    ) -> None:
        self.prefix = prefix
        self.infix = infix
        self.suffix = suffix
        self.sequence = (self.prefix, self.infix, self.suffix)

        self.annotations = annotations
        self.chromosome = chromosome
        super().__init__()

    @classmethod
    def from_string(cls, sequence: str):
        """Creates a sequence from a string sequence.
        
        Parameters
        ----------
        sequence: str
            Sequence in a string format.
        
        Returns
        -------
        Sequence object.
        """
        annotations = ""
        if cls._prefix_separator in sequence:
            annotations, sequence = sequence.split(cls._prefix_separator)

        chromosome = ""
        if cls._chromosome_separator in annotations:
            chromosome, annotations = annotations.split(cls._chromosome_separator)
        elif cls._chromosome_separator in sequence:
            chromosome, sequence = sequence.split(cls._chromosome_separator)

        prefix, infix, suffix = sequence.split(cls._sequence_part_separator)

        prefix = prefix.replace(cls._symbol_sequence_separator, "")
        infix = infix.replace(cls._symbol_sequence_separator, "")
        suffix = suffix.replace(cls._symbol_sequence_separator, "")

        return Sequence(prefix, infix, suffix, annotations, chromosome)

    def _sequence_part_str(self, sequence: str) -> str:
        """Joins a sequence using the symbols separator.
        
        Parameters
        ----------
        sequence: str
            Part of a sequence.
        
        Returns
        -------
        Sequence divided by the symbol separator.
        """
        return self._symbol_sequence_separator.join(sequence)

    def __str__(self):
        prefix_transformed = self._sequence_part_str(self.prefix)
        infix_transformed = self._sequence_part_str(self.infix)
        suffix_transformed = self._sequence_part_str(self.suffix)

        sequence = self._sequence_part_separator.join(
            [prefix_transformed, infix_transformed, suffix_transformed]
        )

        prefix = ""
        if self.annotations:
            prefix = f"{self.annotations}{self._prefix_separator}"

        if self.chromosome:
            prefix = f"{self.chromosome}{self._chromosome_separator}{prefix}"

        return f"{prefix}{sequence}"

    def __getitem__(self, key):
        start = None
        stop = None
        if type(key) is int:
            start = key
            stop = key + 1
            key = slice(None, None, None)

        start = start or key.start
        if start is None:
            start = start or 0

        stop = stop or key.stop
        if stop is None:
            stop = stop or 3

        if stop > 3 or start < 0:
            raise ValueError("Bad index, must be between 0 and 2")

        result = ""
        for index in range(start, stop):
            result += self.sequence[index]

        return result
