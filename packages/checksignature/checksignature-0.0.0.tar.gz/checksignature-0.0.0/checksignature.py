from typing import Callable
from typing import Optional
from typing import TypeVar


T = TypeVar('T')

class CheckSignature:

    def __init__(self, func: Optional[Callable[..., T]] = None):
        self.func = func

    def check(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        if self.func:
            self.check(*args, **kwargs)
            return self.func(*args, **kwargs)

    def __repr__(self):
        if self.func:
            return f'<CheckSignature({self.func.__name__})>'

    def __str__(self):
        if self.func:
            return self.func.__name__


def checksignature(function: Callable = None):
    return CheckSignature(function)

