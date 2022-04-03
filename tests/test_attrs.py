"""
This file tests attrs support.

See https://github.com/snok/flake8-type-checking/issues/77
for discussion on the implementation.
"""

import textwrap

import pytest

from flake8_type_checking.codes import TC002
from tests import _get_error


@pytest.mark.parametrize(
    'imp, dec',
    (
        ['import attrs', '@attrs.define'],
        ['import attr', '@attr.s(auto_attribs=True)'],
        ['import attr', '@attr.define'],
    ),
)
def test_attrs_model(imp, dec):
    """
    Test `attrs` classes together with a non-`attrs` class that has a class var of the same type.
    `attrs` classes are instantiated using different dataclass decorators. The `attrs` module is imported as whole.
    """
    example = textwrap.dedent(
        f'''
        {imp}
        from decimal import Decimal

        {dec}
        class X:
            x: Decimal

        {dec}
        class Y:
            x: Decimal

        class Z:
            x: Decimal
        '''
    )
    assert _get_error(example, error_code_filter='TC001,TC002') == set()


@pytest.mark.parametrize(
    'imp, dec, expected',
    (
        ['import attrs', '@attrs.define', {'4:0 ' + TC002.format(module='decimal.Context')}],
        ['import attr', '@attr.s(auto_attribs=True)', {'4:0 ' + TC002.format(module='decimal.Context')}],
        ['import attr', '@attr.define', {'4:0 ' + TC002.format(module='decimal.Context')}],
    ),
)
def test_complex_attrs_model(imp, dec, expected):
    """
    Test `attrs` classes together with a non-`attrs` class tha has a class var of another type.
    `attrs` classes are instantiated using different dataclass decorators. The `attrs` module is imported as whole.
    """
    example = textwrap.dedent(
        f'''
        {imp}
        from decimal import Decimal
        from decimal import Context

        {dec}
        class X:
            x: Decimal

        {dec}
        class Y:
            x: Decimal

        class Z:
            x: Context
        '''
    )
    assert _get_error(example, error_code_filter='TC001,TC002') == expected


@pytest.mark.parametrize(
    'imp, dec, expected',
    (
        ['from attrs import define', '@define', {'4:0 ' + TC002.format(module='decimal.Context')}],
        ['from attr import s', '@s(auto_attribs=True)', {'4:0 ' + TC002.format(module='decimal.Context')}],
        ['from attr import define', '@define', {'4:0 ' + TC002.format(module='decimal.Context')}],
    ),
)
def test_complex_attrs_model_direct_import(imp, dec, expected):
    """
    Test `attrs` classes together with a non-`attrs` class tha has a class var of another type.
    `attrs` classes are instantiated using different dataclass decorators which are imported as submodules.
    """
    example = textwrap.dedent(
        f'''
        {imp}
        from decimal import Decimal
        from decimal import Context

        {dec}
        class X:
            x: Decimal

        {dec}
        class Y:
            x: Decimal

        class Z:
            x: Context
        '''
    )
    assert _get_error(example, error_code_filter='TC001,TC002') == expected


@pytest.mark.parametrize(
    'imp, dec, expected',
    (
        ['from attrs import define as asdfg', '@asdfg', {'4:0 ' + TC002.format(module='decimal.Context')}],
        [
            'from attr import s as ghdjfg',
            '@ghdjfg(auto_attribs=True)',
            {'4:0 ' + TC002.format(module='decimal.Context')},
        ],
        ['import attr as ghdjfg', '@ghdjfg.define', {'4:0 ' + TC002.format(module='decimal.Context')}],
        ['import attr.define as adasdfg', '@adasdfg', {'4:0 ' + TC002.format(module='decimal.Context')}],
    ),
)
def test_complex_attrs_model_as_import(imp, dec, expected):
    """
    Test `attrs` classes together with a non-`attrs` class tha has a class var of another type.
    `attrs` classes are instantiated using different dataclass decorators which are imported as submodules using an alias.
    """
    example = textwrap.dedent(
        f'''
        {imp}
        from decimal import Decimal
        from decimal import Context

        {dec}
        class X:
            x: Decimal

        {dec}
        class Y:
            x: Decimal

        class Z:
            x: Context
        '''
    )
    assert _get_error(example, error_code_filter='TC001,TC002') == expected


@pytest.mark.parametrize(
    'imp, dec, expected',
    (
        ['from attr import define', '@define(slots=False)', {'4:0 ' + TC002.format(module='decimal.Context')}],
        ['from attr import define', '@define(frozen=True)', {'4:0 ' + TC002.format(module='decimal.Context')}],
        [
            'from attr import define',
            '@define(slots=False, frozen=True)',
            {'4:0 ' + TC002.format(module='decimal.Context')},
        ],
        ['import attr', '@attr.define(slots=False, frozen=True)', {'4:0 ' + TC002.format(module='decimal.Context')}],
    ),
)
def test_complex_attrs_model_slots_frozen(imp, dec, expected):
    """
    Test `attrs` classes together with a non-`attrs` class tha has a class var of another type.
    `attrs` classes are instantiated using different dataclass decorators and arguments.
    """
    example = textwrap.dedent(
        f'''
        {imp}
        from decimal import Decimal
        from decimal import Context

        {dec}
        class X:
            x: Decimal

        {dec}
        class Y:
            x: Decimal

        class Z:
            x: Context
        '''
    )
    assert _get_error(example, error_code_filter='TC001,TC002') == expected
