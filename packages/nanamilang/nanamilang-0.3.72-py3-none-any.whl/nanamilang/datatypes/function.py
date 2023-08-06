"""NanamiLang Function Data Type"""

# This file is a part of NanamiLang Project
# This project licensed under GNU GPL version 2
# Initially made by @jedi2light (aka Stoian Minaiev)


from .base import Base


class Function(Base):
    """NanamiLang Function Data Type Class"""

    name: str = 'Function'
    _expected_type = dict
    _python_reference: dict
    purpose = 'Encapsulate function name and reference to its implementation'

    def __init__(self, reference: dict) -> None:
        """Initialize a new Function instance"""

        self.init_assert_reference_has_keys(
            reference, ('function_name',
                        'function_reference')
        )

        self._hashed = hash(
            reference.get('function_reference')
        )

        super().__init__(reference)

    def reference(self):
        """NanamiLang Function, reference() implementation"""

        return self._python_reference.get('function_reference')

    def format(self, **kwargs) -> str:
        """NanamiLang Function, format() method implementation"""

        return self._python_reference.get('function_name')

    def origin(self) -> str:
        """NanamiLang Function, origin() method implementation"""

        return self.format()
