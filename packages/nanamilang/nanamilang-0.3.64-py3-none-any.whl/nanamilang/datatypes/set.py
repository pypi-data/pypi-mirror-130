"""NanamiLang Set Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from functools import reduce

import nanamilang.shortcuts as shortcuts
from .base import Base
from .integernumber import IntegerNumber
from .nil import Nil


class Set(Base):
    """NanamiLang Set Data Type Class"""

    name: str = 'Set'
    _expected_type = set
    _python_reference: set = set()
    _nil = Nil('nil')
    _hashed = _nil.hashed()
    _nil__hashed_val = _hashed
    _length: IntegerNumber = IntegerNumber(0)
    purpose = 'Implements Set of NanamiLang Base data types'

    def get(self, element: Base) -> Base:
        """NanamiLang Set, get() implementation"""

        shortcuts.ASSERT_IS_CHILD_OF(
            element,
            Base,
            message='Set.get() element must be derived from Base'
        )

        return shortcuts.get(
            tuple(filter(
                lambda e: e.hashed() == element.hashed(),
                self._python_reference
            )), 0, self._nil
        )

    def count(self):
        """NanamiLang Set, count() implementation"""

        # Return pre-calculated (on init stage) Vector length
        return self._length

    def __init__(self, reference: set) -> None:
        """NanamiLang Set, initialize new instance"""

        # In case of creating non-empty Set ...
        # (if empty, do not validate, calculate _hashed and _length)
        if reference:
            self.init_assert_only_base(reference)
            self._hashed = reduce(
                lambda e, n: e + n, map(lambda e: e.hashed(), reference)
            )
            self._length = IntegerNumber(len(reference))

        super(Set, self).__init__(reference=reference)

    def reference_as_tuple(self) -> tuple:
        """NanamiLang Set, reference_as_tuple() implementation"""

        return tuple(self._python_reference) if self._python_reference else ()

    def format(self) -> str:
        """NanamiLang Set, format() method implementation"""

        # There is no sense to call that pipeline if we can just return '#{}'
        if not self._python_reference:
            return '#{}'
        return '#{' + f'{" ".join((i.format() for i in self.reference()))}' + '}'
