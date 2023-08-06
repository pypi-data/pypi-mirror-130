from typing import Union
from unittest import TestCase

from checksignature import CheckSignature
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

        function(1) == 1

    def test_can_handle_signature_fail_with_Union(self):

        @checksignature
        def function(a: Union[int, str]):
            return a

        with self.assertRaises(TypeError):
            function(1.0)

    def test_function_with_no_type_hints(self):

        @checksignature
        def function(a, b, c):
            return a, b, c

        function('one', 2, 3.0)

    def test_keyword_only_signatures(self):

        @checksignature
        def function(a, b: int, *, key=None):
            return a, b, key

        function('one', 2, key=3)

    def test_can_handle_function_with_no_args(self):

        @checksignature
        def function():
            pass

        function()

    def test_functionless_CheckSignature_evalutation(self):
        CheckSignature().evaluate() == None

    def test_functionless_CheckSignature__call__(self):
        CheckSignature()() == None

    def test_CheckSignature__str__(self):

        @checksignature
        def function():
            pass

        str(function)           == 'function'
        str(CheckSignature()) == ''

    def test_CheckSignature__repr__(self):

        @checksignature
        def function(a):
            return a

        repr(function)      == '<CheckSignature(function)>'
        repr(CheckSignature()) == '<CheckSignature()>'

