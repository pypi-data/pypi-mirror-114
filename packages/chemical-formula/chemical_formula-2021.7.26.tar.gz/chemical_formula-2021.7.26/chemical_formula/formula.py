# -*- coding: utf-8 -*-

"""Handling of chemical formulae.
"""

import collections.abc
import logging

# logging.basicConfig(level="DEBUG")
logger = logging.getLogger(__name__)

open_parenthesis = {"(": ")", "[": "]", "{": "}"}
close_parenthesis = {j: i for i, j in open_parenthesis.items()}


def parse_formula(text):
    """Parse a chemical formula into a dictionary.

    Parameters
    ----------
    text : str
        The chemical formula to parse.

    Returns
    dict(str: float)

    The approach is as follows:
    The first character must be an opening parenthesis or the first letter of a chemical
    symbol. If it is a parenthesis, the entire expression in the parenthesis is given
    recursively to this routine to handle.
    """
    # Remove any blank space in the string
    chars = [i for i in text if i.isspace() is False]

    logging.debug(f"{chars=}")

    result = {}
    i = 0
    n = len(chars)
    level = 0
    while i < n:
        next_char = chars[i]
        logging.debug(f"{next_char=}")
        if next_char in open_parenthesis:
            close = open_parenthesis[next_char]
            level = 1
            j = i + 1
            while j < n:
                # Handle parenthetical expressions recursively
                logging.debug(f"   {j=} {chars[j]=}")
                if chars[j] in open_parenthesis:
                    level += 1
                elif chars[j] in close_parenthesis:
                    level -= 1
                    if level == 0:
                        if close != chars[j]:
                            raise ValueError(
                                "Mismatched parenthesis:\n"
                                f"    {''.join(chars)}\n"
                                f"    {(i - 1) * ' '}^{(j - 1 - 1) * ' '}^"
                            )
                        logging.debug("\n\n\n")
                        sub_result = parse_formula("".join(chars[i + 1 : j]))
                        logging.debug("\n\n\n")
                        i = j + 1
                        logging.debug(f"    {i=} {sub_result=}")
                        break
                j += 1
            i = j + 1
            if i >= n:
                logging.debug(f"----{sub_result=}")
                logging.debug(f"        {result=}")
                for symbol, proportion in sub_result.items():
                    if symbol in result:
                        result[symbol] += proportion
                    else:
                        result[symbol] = proportion
                logging.debug(f"        {result=}")
            else:
                # There may be a proportion after the parentheses
                next_char = chars[i]
                if next_char.isdecimal() or next_char == ".":
                    # A proportion
                    proportion = next_char
                    i += 1
                    logging.debug(f"    {i=} {n=} {proportion=}")
                    while i < n:
                        next_char = chars[i]
                        if next_char.isdecimal() or next_char == ".":
                            proportion += next_char
                        i += 1
                    if "." in proportion:
                        proportion = float(proportion)
                    else:
                        proportion = int(proportion)
                    for symbol in sub_result:
                        sub_result[symbol] *= proportion
                logging.debug(f"    {sub_result=}")
                logging.debug(f"        {result=}")
                for symbol, proportion in sub_result.items():
                    if symbol in result:
                        result[symbol] += proportion
                    else:
                        result[symbol] = proportion
                logging.debug(f"        {result=}")
        elif next_char.isalpha():
            logging.debug(f"looking for symbol {next_char=}")
            if next_char.isupper():
                symbol = next_char
                i += 1
                if i == n:
                    if symbol in result:
                        result[symbol] += 1
                    else:
                        result[symbol] = 1
                    break
                next_char = chars[i]
                if next_char in open_parenthesis:
                    if symbol in result:
                        result[symbol] += 1
                    else:
                        result[symbol] = 1
                    continue
                if next_char.isalpha():
                    if next_char.islower():
                        symbol += next_char
                        i += 1
                    else:
                        logging.debug(f"    in symbol {next_char=}")
                        if symbol in result:
                            result[symbol] += 1
                        else:
                            result[symbol] = 1
                        continue
                # Have the symbol, so what comes next_char?
                next_char = chars[i]
                logging.debug(f"    {next_char=}")
                if next_char.isalpha():
                    # Starting another chemical symbol
                    continue
                elif next_char.isdecimal() or next_char == ".":
                    # A proportion
                    proportion = next_char
                    i += 1
                    logging.debug(f"    {i=} {n=} {proportion=}")
                    while i < n:
                        next_char = chars[i]
                        if next_char.isdecimal() or next_char == ".":
                            proportion += next_char
                        else:
                            break
                        i += 1
                    if "." in proportion:
                        proportion = float(proportion)
                    else:
                        proportion = int(proportion)
                    if symbol in result:
                        result[symbol] += proportion
                    else:
                        result[symbol] = proportion
            else:
                raise ValueError(
                    f"Incorrect formula\n    {''.join(chars)}\n    {i * ' '}^"
                )
        else:
            raise ValueError(
                f"Incorrect formula. Expected symbol or parenthesis (i = {i})\n"
                f"    {''.join(chars)}\n    {i * ' '}^"
            )
    logging.debug(f"{result=}")

    return result


class Formula(collections.abc.MutableMapping):
    """A dictionary-like object for handling formulae."""

    def __init__(self, arg=None):
        self._data = []
        if arg is not None:
            if isinstance(arg, str):
                self.formula = arg

    def __getitem__(self, key):
        """Allow [] to access the data!"""
        if key in self._data:
            return self._data(key)
        else:
            return 0

    def __setitem__(self, key, value) -> None:
        """Allow x[key] access to the data"""
        self._data[key] = value

    def __delitem__(self, key) -> None:
        """Allow deletion of keys"""
        del self._data[key]

    def __iter__(self) -> iter:
        """Allow iteration over the object"""
        return iter(self._data)

    def __len__(self) -> int:
        """The len() command"""
        return len(self._data)

    def __repr__(self) -> str:
        """The string representation of this object"""
        return self.formula

    def __str__(self) -> str:
        """The pretty string representation of this object"""
        return self.formula

    def __contains__(self, key) -> bool:
        """Return a boolean indicating if a key exists."""
        return key in self._data

    def __eq__(self, other):
        """Return a boolean if this object is equal to another"""
        return self._data == other._data

    @property
    def formula(self):
        """The chemical formula."""
        data = self._data
        if "C" in data:
            result = "C"
            if data["C"] != 1:
                result += str(data["C"])
            if "H" in data:
                result += "H"
                if data["H"] != 1:
                    result += str(data["H"])
            for element in sorted(data.keys()):
                if element != "C" and element != "H":
                    result += element
                    if data[element] != 1:
                        result += str(data[element])
        else:
            result = ""
            for element in sorted(data.keys()):
                result += element
                if data[element] != 1:
                    result += str(data[element])

        return result

    @formula.setter
    def formula(self, text):
        self._data = parse_formula(text)

    def to_dict(self):
        return {**self._data}


if __name__ == "__main__":  # pragma: no cover
    formula = Formula()

    formula.formula = "H4C"
    print(f"formula = {formula.formula}")

    formula.formula = "(H2SO4)4"
    print(f"formula = {formula.formula}")

    formula.formula = "CH3C(CH3)(CH3)CH2(CH(CH3)(CH3))"
    print(f"formula = {formula.formula}")
