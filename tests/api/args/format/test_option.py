import pytest

from clikit.api.args.format import Option


def test_create():
    opt = Option("option")

    assert "option" == opt.long_name
    assert opt.short_name is None
    assert opt.is_long_name_preferred()
    assert not opt.is_short_name_preferred()
    assert not opt.accepts_value()
    assert not opt.is_value_required()
    assert not opt.is_value_optional()
    assert not opt.is_multi_valued()
    assert opt.default is None
    assert "..." == opt.value_name


def test_dashed_long_name():
    opt = Option("--option")

    assert "option" == opt.long_name


def test_fail_if_long_name_is_null():
    with pytest.raises(ValueError):
        Option(None)


def test_fail_if_long_name_is_empty():
    with pytest.raises(ValueError):
        Option("")


def test_fail_if_long_name_is_not_a_string():
    with pytest.raises(ValueError):
        Option(1234)


def test_fail_if_long_name_contains_spaces():
    with pytest.raises(ValueError):
        Option("foo bar")


def test_fail_if_long_name_starts_with_number():
    with pytest.raises(ValueError):
        Option("1option")


def test_fail_if_long_name_is_one_character():
    with pytest.raises(ValueError):
        Option("o")


def test_fail_if_long_name_starts_with_single_hyphen():
    with pytest.raises(ValueError):
        Option("-option")


def test_fail_if_long_name_starts_with_three_hyphens():
    with pytest.raises(ValueError):
        Option("-option")


@pytest.mark.parametrize(
    "flags",
    [
        Option.NO_VALUE | Option.OPTIONAL_VALUE,
        Option.NO_VALUE | Option.REQUIRED_VALUE,
        Option.NO_VALUE | Option.MULTI_VALUED,
        Option.PREFER_LONG_NAME | Option.PREFER_SHORT_NAME,
        Option.STRING | Option.BOOLEAN,
        Option.STRING | Option.INTEGER,
        Option.STRING | Option.FLOAT,
        Option.BOOLEAN | Option.INTEGER,
        Option.BOOLEAN | Option.FLOAT,
        Option.INTEGER | Option.FLOAT,
    ],
)
def test_fail_if_invalid_flag_combination(flags):
    with pytest.raises(ValueError):
        Option("option", "o", flags)


def test_short_name():
    opt = Option("option", "o")

    assert "o" == opt.short_name


def test_dashed_short_name():
    opt = Option("option", "-o")

    assert "o" == opt.short_name


def test_fail_if_short_name_is_empty():
    with pytest.raises(ValueError):
        Option("option", "")


def test_fail_if_short_name_is_not_string():
    with pytest.raises(ValueError):
        Option("option", 1234)


def test_fail_if_short_name_is_longer_than_one_letter():
    with pytest.raises(ValueError):
        Option("option", "ab")


def test_no_value():
    opt = Option("option", flags=Option.NO_VALUE)

    assert not opt.accepts_value()
    assert not opt.is_value_required()
    assert not opt.is_value_optional()
    assert not opt.is_multi_valued()
    assert opt.default is None


def test_fail_if_no_value_and_default_value():
    with pytest.raises(ValueError):
        Option("option", flags=Option.NO_VALUE, default="Default")


def test_optional_value():
    opt = Option("option", flags=Option.OPTIONAL_VALUE)

    assert opt.accepts_value()
    assert not opt.is_value_required()
    assert opt.is_value_optional()
    assert not opt.is_multi_valued()
    assert opt.default is None


def test_optional_value_with_default():
    opt = Option("option", flags=Option.OPTIONAL_VALUE, default="Default")

    assert opt.accepts_value()
    assert not opt.is_value_required()
    assert opt.is_value_optional()
    assert not opt.is_multi_valued()
    assert "Default" == opt.default


def test_required_value():
    opt = Option("option", flags=Option.REQUIRED_VALUE)

    assert opt.accepts_value()
    assert opt.is_value_required()
    assert not opt.is_value_optional()
    assert not opt.is_multi_valued()
    assert opt.default is None


def test_required_value_with_default():
    opt = Option("option", flags=Option.REQUIRED_VALUE, default="Default")

    assert opt.accepts_value()
    assert opt.is_value_required()
    assert not opt.is_value_optional()
    assert not opt.is_multi_valued()
    assert "Default" == opt.default


def test_multi_valued():
    opt = Option("option", flags=Option.MULTI_VALUED)

    assert opt.accepts_value()
    assert opt.is_value_required()
    assert not opt.is_value_optional()
    assert opt.is_multi_valued()
    assert [] == opt.default


def test_multi_valued_with_default():
    opt = Option("option", flags=Option.MULTI_VALUED, default=["foo", "bar"])

    assert opt.accepts_value()
    assert opt.is_value_required()
    assert not opt.is_value_optional()
    assert opt.is_multi_valued()
    assert ["foo", "bar"] == opt.default


def test_fail_if_multi_valued_with_default_not_list():
    with pytest.raises(ValueError):
        Option("option", flags=Option.MULTI_VALUED, default="Default")


@pytest.mark.parametrize(
    "flags, string, output",
    [
        (0, "", ""),
        (0, "string", "string"),
        (0, "1", "1"),
        (0, "1.23", "1.23"),
        (0, "null", "null"),
        (Option.NULLABLE, "null", None),
        (0, "true", "true"),
        (0, "false", "false"),
        (Option.STRING, "", ""),
        (Option.STRING, "string", "string"),
        (Option.STRING, "1", "1"),
        (Option.STRING, "1.23", "1.23"),
        (Option.STRING, "null", "null"),
        (Option.STRING | Option.NULLABLE, "null", None),
        (Option.STRING, "true", "true"),
        (Option.STRING, "false", "false"),
        (Option.BOOLEAN, "true", True),
        (Option.BOOLEAN, "false", False),
        (Option.BOOLEAN | Option.NULLABLE, "null", None),
        (Option.INTEGER, "1", 1),
        (Option.INTEGER, "0", 0),
        (Option.INTEGER | Option.NULLABLE, "null", None),
        (Option.FLOAT, "1", 1.0),
        (Option.FLOAT, "1.23", 1.23),
        (Option.FLOAT, "0", 0.0),
        (Option.FLOAT | Option.NULLABLE, "null", None),
    ],
)
def test_parse_value(flags, string, output):
    arg = Option("option", flags=flags)

    assert output == arg.parse(string)


@pytest.mark.parametrize(
    "flags, string",
    [(Option.BOOLEAN, "null"), (Option.INTEGER, "null"), (Option.FLOAT, "null")],
)
def test_parse_value_fails_if_invalid(flags, string):
    arg = Option("argument", flags=flags)

    with pytest.raises(ValueError):
        arg.parse(string)
