from clikit.utils.terminal import Terminal


def test_terminal_always_has_a_valid_width(mocker):
    mocker.patch(
        "clikit.utils.terminal.Terminal._get_terminal_size_windows",
        return_value=(0, 42),
    )
    mocker.patch(
        "clikit.utils.terminal.Terminal._get_terminal_size_tput", return_value=(0, 42)
    )
    mocker.patch(
        "clikit.utils.terminal.Terminal._get_terminal_size_linux", return_value=(0, 42)
    )

    terminal = Terminal()

    assert 80 == terminal.width
    assert 42 == terminal.height
