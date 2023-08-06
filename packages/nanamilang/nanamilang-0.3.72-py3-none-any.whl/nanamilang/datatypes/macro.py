"""NanamiLang Macro Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from .base import Base


class Macro(Base):
    """NanamiLang Macro Data Type Class"""

    name: str = 'Macro'
    _expected_type = dict
    _python_reference: dict
    purpose = 'Encapsulate macro name and reference to its implementation'

    def __init__(self, reference: dict) -> None:
        """Initialize a new Macro instance"""

        self.init_assert_reference_has_keys(
            reference, ('macro_name',
                        'macro_reference')
        )

        self._hashed = hash(
            reference.get('macro_reference')
        )

        super().__init__(reference)

    def reference(self):
        """NanamiLang Macro, reference() implementation"""

        return self._python_reference.get('macro_reference')

    def format(self, **kwargs) -> str:
        """NanamiLang Macro, format() method implementation"""

        return self._python_reference.get('macro_name')

    def origin(self) -> str:
        """NanamiLang Macro, origin() method implementation"""

        return self.format()
