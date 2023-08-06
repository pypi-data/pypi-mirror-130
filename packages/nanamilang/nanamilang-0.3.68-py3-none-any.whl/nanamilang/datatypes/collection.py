"""NanamiLang Collection Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from functools import reduce
from typing import Generator

from .nil import Nil
from .base import Base
from .integernumber import IntegerNumber


class Collection(Base):
    """NanamiLang Collection Type Base Class"""

    _nil = Nil('nil')
    _hashed = _nil.hashed()
    _nil__hashed_val = _hashed
    _length: IntegerNumber = IntegerNumber(0)

    @staticmethod
    def _init__chance_to_process_and_override(reference) -> None:
        """
        NanamiLang Collection Type Base Class
        Give it a chance to process and override passed reference
        """

        return reference

    def _init__assertions_on_non_empty_reference(self,
                                                 reference) -> None:
        """NanamiLang Collection Type Base Class, assertions to run"""

        self.init_assert_only_base(reference)

    @staticmethod
    def _init__count_length(countable: tuple or set) -> int:
        """NanamiLang Collection Type Base Class, return count"""

        return len(countable)

    def count(self) -> IntegerNumber:
        """NanamiLang Collection Type Base Class, get self._length"""

        return self._length

    def elements(self) -> Generator:
        """NanamiLang Collection Type Base Class, return a Generator"""

        # By default, we assume that _python_reference is plain structure
        return (_ for _ in self._python_reference)

    def __init__(self, reference) -> None:
        """NanamiLang Collection Type Base Class, initialize new instance"""

        # In case of creating non-empty collection ...
        # (if empty, do not validate, calculate _hashed and _length)

        # By default, self._length would be IntegerNumber(0)
        #             self._python_reference default should be defined
        #             self._hashed would be Nil('nil')._hashed() value
        if reference:
            # Run assertions, they can be defined in
            # _init__assertions_on_non_empty_reference() hook-method
            self._init__assertions_on_non_empty_reference(reference)
            # Count summary integer value of each .hashed() instance value
            self._hashed = reduce(
                lambda e, n: e + n, map(lambda e: e.hashed(), reference)
            )
            # Count overall collection items using overridable hook-method
            self._length = IntegerNumber(self._init__count_length(reference))
            # Give derived class a chance to possibly override reference
            reference = self._init__chance_to_process_and_override(reference)

        super().__init__(reference)
        # Call Base.__init__ through super() to finish Base Nanamilang type initialization
