from collections import OrderedDict as odict
from inspect import _empty as NoTypeInfo
from inspect import signature
from string import Template
from typing import Callable
from typing import Optional
from typing import TypeVar


T = TypeVar('T')

class CheckSignature:

    def __init__(self, func: Optional[Callable[..., T]] = None):
        self.func = func

    def evaluate(self, *args, **kwargs):
        if self.func:
            given_params = args + tuple(odict(kwargs).values())
            parameters = signature(self.func).parameters

            for i, key in enumerate(parameters.keys()):
                expected_type = parameters[key].annotation

                try:
                    given_param = given_params[i]
                except IndexError:
                    return None

                given_param_type = type(given_param)

                def raise_TypeError(expected_type_name: str):
                    issue = Template(
                        'Expected "$key" with value "$value" to be of type, "$expected_type". '
                    )
                    actuality = Template(
                        'Received "$given_type" instead.'
                    )
                    raise TypeError(
                        issue.substitute(
                            key=key,
                            value=given_param,
                            expected_type=expected_type_name
                        ) + actuality.substitute(
                            given_type=type(given_param).__name__
                        )
                    )

                if expected_type != NoTypeInfo:
                    if str(expected_type).startswith('typing.Union'):
                        if given_param_type not in expected_type.__args__:
                            raise_TypeError(f'{[et.__name__ for et in expected_type.__args__]}')
                    else:
                        if given_param_type != expected_type:
                            raise_TypeError(expected_type.__name__)

    def __call__(self, *args, **kwargs):
        if self.func:
            self.evaluate(*args, **kwargs)
            return self.func(*args, **kwargs)

    def __repr__(self):
        if self.func:
            return f'<CheckSignature({self.func.__name__})>'

    def __str__(self):
        if self.func:
            return self.func.__name__


def checksignature(function: Callable = None):
    return CheckSignature(function)

