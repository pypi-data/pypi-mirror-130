from typing import Union
from unittest import TestCase

from checksignature import checksignature


class CheckSignatureTest(TestCase):

    @checksignature
    def function(a: str, b: int, c, **kwargs):
        return a, b, c, kwargs

    def test_function_executes_with_compatible_signature(self):
        self.function('one', 2, 3.0, **{'four': 4})

    def test_TypeError_thrown_on_incompatible_signature(self):
        with self.assertRaises(TypeError):
            self.function(1, 2, 3.0, **{'four': 4})

    def test_can_handle_signature_with_Union(self):

        @checksignature
        def function(a: Union[int, str]):
            return a

        function(1)

