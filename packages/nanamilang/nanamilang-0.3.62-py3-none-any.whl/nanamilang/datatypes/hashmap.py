"""NanamiLang HashMap Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from functools import reduce

import nanamilang.shortcuts as shortcuts
from .base import Base
from .integernumber import IntegerNumber
from .nil import Nil


class HashMap(Base):
    """NanamiLang HashMap Data Type Class"""

    name: str = 'HashMap'
    _expected_type = tuple
    _nil = Nil('nil')
    _python_reference = (_nil, _nil)
    _hashed = _nil.hashed()
    _nil__hashed_val = _hashed
    _length: IntegerNumber = IntegerNumber(0)
    purpose = 'Implement HashMap of NanamiLang Base data types'

    def get(self, key: Base) -> Base:
        """NanamiLang HashMap, get() implementation"""

        shortcuts.ASSERT_IS_CHILD_OF(
            key,
            Base,
            message='HashMap.get() key must be a child of Base'
        )

        return shortcuts.get(shortcuts.get(
            tuple(filter(
                lambda kv: kv[0].hashed() == key.hashed(),
                self._python_reference
            )), 0, ()
        ), 1, self._nil)

    def count(self):
        """NanamiLang Set, count() implementation"""

        # Return pre-calculated (on init stage) Vector length
        return self._length

    def __init__(self, reference: tuple) -> None:
        """NanamiLang HashMap, initialize new instance"""

        # In case of creating non-empty HashMap ...
        # (if empty, do not validate, calculate _hashed and _length)
        if reference:
            self.init_assert_only_base(reference)
            self.init_assert_ref_len_is_even(reference)
            self._hashed = reduce(
                lambda e, n: e + n, map(lambda e: e.hashed(), reference)
            )
            reference = shortcuts.enpart(reference)
            self._length = IntegerNumber(len(reference))

        super(HashMap, self).__init__(reference=reference)

    def reference_as_tuple(self) -> tuple:
        """NanamiLang HashMap, reference_as_tuple() method implementation"""

        return self.reference()

    def format(self) -> str:
        """NanamiLang HashMap, format() method implementation"""

        # There is no sense to call that pipeline if we can just return '{}'
        if self._python_reference == (self._nil, self._nil):
            return '{}'
        return '{' + f'{" ".join([f"{k.format()} {v.format()}" for k, v in self.reference()])}' + '}'
