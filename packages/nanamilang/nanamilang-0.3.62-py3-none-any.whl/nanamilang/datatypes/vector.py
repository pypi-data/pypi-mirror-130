"""NanamiLang Vector Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from functools import reduce

import nanamilang.shortcuts as shortcuts
from .base import Base
from .integernumber import IntegerNumber
from .nil import Nil


class Vector(Base):
    """NanamiLang Vector Data Type Class"""

    name: str = 'Vector'
    _expected_type = tuple
    _python_reference: tuple = tuple()
    _nil = Nil('nil')
    _hashed = _nil.hashed()
    _nil__hashed_val = _hashed
    _length: IntegerNumber = IntegerNumber(0)
    purpose = 'Implements Vector of NanamiLang Base data types'

    def get(self, index: IntegerNumber) -> Base:
        """NanamiLang Vector, get() implementation"""

        shortcuts.ASSERT_IS_INSTANCE_OF(
            index,
            IntegerNumber,
            message='Vector.get() index must be an IntegerNumber'
        )

        return shortcuts.get(self.reference(), index.reference(), self._nil)

    def count(self):
        """NanamiLang Set, count() implementation"""

        # Return pre-calculated (on init stage) Vector length
        return self._length

    def __init__(self, reference: tuple) -> None:
        """NanamiLang Vector, initialize new instance"""

        # In case of creating non-empty Vector ...
        # (if empty, do not validate, calculate _hashed and _length)
        if reference:
            self.init_assert_only_base(reference)
            self._hashed = reduce(
                lambda e, n: e + n, map(lambda e: e.hashed(), reference)
            )
            self._length = IntegerNumber(len(reference))

        super(Vector, self).__init__(reference=reference)

    def reference_as_tuple(self) -> tuple:
        """NanamiLang Vector, reference_as_tuple() implementation"""

        return self._python_reference

    def format(self) -> str:
        """NanamiLang Vector, format() method implementation"""

        # There is no sense to call that pipeline if we can just return '[]'
        if not self._python_reference:
            return '[]'
        return '[' + f'{" ".join((i.format() for i in self.reference()))}' + ']'
