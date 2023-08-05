from baby_steps import given, then, when
from district42 import schema
from pytest import raises

from revolt import substitute
from revolt.errors import SubstitutionError


def test_none_substitution():
    with given:
        sch = schema.none

    with when:
        res = substitute(sch, None)

    with then:
        assert res == sch == schema.none
        assert id(res) != id(sch)


def test_none_substitution_invalid_value_error():
    with given:
        sch = schema.none

    with when, raises(Exception) as exception:
        substitute(sch, False)

    with then:
        assert exception.type is SubstitutionError
