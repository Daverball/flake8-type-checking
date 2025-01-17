"""
File tests TC201:
    Annotation is wrapped in unnecessary quotes
"""
import textwrap

import pytest

from flake8_type_checking.constants import TC201
from tests.conftest import _get_error

examples = [
    ('', set()),
    ("x: 'int'", {'1:3 ' + TC201.format(annotation='int')}),
    ("x: 'Dict[int]'", {'1:3 ' + TC201.format(annotation='Dict[int]')}),
    ("from __future__ import annotations\nx: 'int'", {'2:3 ' + TC201.format(annotation='int')}),
    ("if TYPE_CHECKING:\n\tfrom typing import Dict\nx: 'Dict'", set()),
    ("if TYPE_CHECKING:\n\tfrom typing import Dict\nx: 'Dict[int]'", set()),
    (
        "from __future__ import annotations\nfrom typing import Dict\nx: Dict['int']",
        {'3:8 ' + TC201.format(annotation='int')},
    ),
    (
        "from __future__ import annotations\nif TYPE_CHECKING:\n\tfrom typing import Dict\nx: Dict['int']",
        {'4:8 ' + TC201.format(annotation='int')},
    ),
    (
        textwrap.dedent('''
            from __future__ import annotations

            if TYPE_CHECKING:
                import something

            x: "something"
            '''),
        set(),
    ),
    (
        textwrap.dedent('''
        from __future__ import annotations

        if TYPE_CHECKING:
            import something

        def example(x: "something") -> something:
            pass
        '''),
        set(),
    ),
    (
        textwrap.dedent('''
    class X:
        def foo(self) -> 'X':
            pass
    '''),
        set(),
    ),
    (
        textwrap.dedent('''
    from __future__ import annotations
    class X:
        def foo(self) -> 'X':
            pass
    '''),
        set(),
    ),
]


@pytest.mark.parametrize(('example', 'expected'), examples)
def test_TC201_errors(example, expected):
    assert _get_error(example, error_code_filter='TC201') == expected
