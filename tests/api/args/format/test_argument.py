import pytest

from clikit.api.args.format import Argument


def test_create():
    arg = Argument("argument")

    assert "argument" == arg.name
    assert not arg.is_required()
    assert arg.is_optional()
    assert not arg.is_multi_valued()
    assert arg.default is None
    assert arg.description is None


def test_fail_if_name_is_null():
    with pytest.raises(ValueError):
        Argument(None)


def test_fail_if_name_is_empty():
    with pytest.raises(ValueError):
        Argument("")


def test_fail_if_name_is_not_a_string():
    with pytest.raises(ValueError):
        Argument(1234)


def test_fail_if_name_contains_spaces():
    with pytest.raises(ValueError):
        Argument("foo bar")


def test_fail_if_name_starts_with_hyphen():
    with pytest.raises(ValueError):
        Argument("-argument")


def test_fail_if_name_starts_with_number():
    with pytest.raises(ValueError):
        Argument("1argument")


@pytest.mark.parametrize(
    "flags",
    [
        Argument.REQUIRED | Argument.OPTIONAL,
        Argument.STRING | Argument.BOOLEAN,
        Argument.STRING | Argument.INTEGER,
        Argument.STRING | Argument.FLOAT,
        Argument.BOOLEAN | Argument.INTEGER,
        Argument.BOOLEAN | Argument.FLOAT,
        Argument.INTEGER | Argument.FLOAT,
    ],
)
def test_fail_if_invalid_flags_combination(flags):
    with pytest.raises(ValueError):
        Argument("argument", flags)


def test_required_argument():
    arg = Argument("argument", Argument.REQUIRED)

    assert "argument" == arg.name
    assert arg.is_required()
    assert not arg.is_optional()
    assert not arg.is_multi_valued()
    assert arg.default is None
    assert arg.description is None


def test_fail_if_required_argument_and_default_value():
    with pytest.raises(ValueError):
        Argument("argument", Argument.REQUIRED, default="Default")


def test_optional_argument():
    arg = Argument("argument", Argument.OPTIONAL)

    assert "argument" == arg.name
    assert not arg.is_required()
    assert arg.is_optional()
    assert not arg.is_multi_valued()
    assert arg.default is None
    assert arg.description is None


def test_optional_argument_with_default_value():
    arg = Argument("argument", Argument.OPTIONAL, default="Default")

    assert "argument" == arg.name
    assert not arg.is_required()
    assert arg.is_optional()
    assert not arg.is_multi_valued()
    assert "Default" == arg.default
    assert arg.description is None


def test_multi_valued_argument():
    arg = Argument("argument", Argument.MULTI_VALUED)

    assert "argument" == arg.name
    assert not arg.is_required()
    assert arg.is_optional()
    assert arg.is_multi_valued()
    assert arg.default == []
    assert arg.description is None


def test_required_multi_valued_argument():
    arg = Argument("argument", Argument.REQUIRED | Argument.MULTI_VALUED)

    assert "argument" == arg.name
    assert arg.is_required()
    assert not arg.is_optional()
    assert arg.is_multi_valued()
    assert arg.default == []
    assert arg.description is None


def test_optional_multi_valued_argument():
    arg = Argument("argument", Argument.OPTIONAL | Argument.MULTI_VALUED)

    assert "argument" == arg.name
    assert not arg.is_required()
    assert arg.is_optional()
    assert arg.is_multi_valued()
    assert arg.default == []
    assert arg.description is None


def test_optional_multi_valued_argument_with_default():
    arg = Argument(
        "argument", Argument.OPTIONAL | Argument.MULTI_VALUED, default=["foo", "bar"]
    )

    assert "argument" == arg.name
    assert not arg.is_required()
    assert arg.is_optional()
    assert arg.is_multi_valued()
    assert ["foo", "bar"] == arg.default
    assert arg.description is None


def test_fail_if_multi_values_argument_and_default_value_is_not_list():
    with pytest.raises(ValueError):
        Argument("argument", Argument.MULTI_VALUED, default="Default")


@pytest.mark.parametrize(
    "flags, string, output",
    [
        (0, "", ""),
        (0, "string", "string"),
        (0, "1", "1"),
        (0, "1.23", "1.23"),
        (0, "null", "null"),
        (Argument.NULLABLE, "null", None),
        (0, "true", "true"),
        (0, "false", "false"),
        (Argument.STRING, "", ""),
        (Argument.STRING, "string", "string"),
        (Argument.STRING, "1", "1"),
        (Argument.STRING, "1.23", "1.23"),
        (Argument.STRING, "null", "null"),
        (Argument.STRING | Argument.NULLABLE, "null", None),
        (Argument.STRING, "true", "true"),
        (Argument.STRING, "false", "false"),
        (Argument.BOOLEAN, "true", True),
        (Argument.BOOLEAN, "false", False),
        (Argument.BOOLEAN | Argument.NULLABLE, "null", None),
        (Argument.INTEGER, "1", 1),
        (Argument.INTEGER, "0", 0),
        (Argument.INTEGER | Argument.NULLABLE, "null", None),
        (Argument.FLOAT, "1", 1.0),
        (Argument.FLOAT, "1.23", 1.23),
        (Argument.FLOAT, "0", 0.0),
        (Argument.FLOAT | Argument.NULLABLE, "null", None),
    ],
)
def test_parse_value(flags, string, output):
    arg = Argument("argument", flags)

    assert output == arg.parse(string)


@pytest.mark.parametrize(
    "flags, string",
    [(Argument.BOOLEAN, "null"), (Argument.INTEGER, "null"), (Argument.FLOAT, "null")],
)
def test_parse_value_fails_if_invalid(flags, string):
    arg = Argument("argument", flags)

    with pytest.raises(ValueError):
        arg.parse(string)
