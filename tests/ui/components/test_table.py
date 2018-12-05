# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from clikit.ui.components import Table
from clikit.ui.style import TableStyle
from clikit.ui.style.alignment import Alignment


def test_render_ascii_border(io):
    table = Table(TableStyle.ascii())
    table.set_header_row(["ISBN", "Title", "Author"])
    table.add_rows(
        [
            ["99921-58-10-7", "Divine Comedy", "Dante Alighieri"],
            ["9971-5-0210-0", "A Tale of Two Cities", "Charles Dickens"],
            ["960-425-059-0", "The Lord of the Rings", "J. R. R. Tolkien"],
            ["80-902734-1-6", "And Then There Were None", "Agatha Christie"],
        ]
    )

    table.render(io)

    expected = """\
+---------------+--------------------------+------------------+
| ISBN          | Title                    | Author           |
+---------------+--------------------------+------------------+
| 99921-58-10-7 | Divine Comedy            | Dante Alighieri  |
| 9971-5-0210-0 | A Tale of Two Cities     | Charles Dickens  |
| 960-425-059-0 | The Lord of the Rings    | J. R. R. Tolkien |
| 80-902734-1-6 | And Then There Were None | Agatha Christie  |
+---------------+--------------------------+------------------+
"""

    assert expected == io.fetch_output()


def test_render_solid_border(io):
    table = Table(TableStyle.solid())
    table.set_header_row(["ISBN", "Title", "Author"])
    table.add_rows(
        [
            ["99921-58-10-7", "Divine Comedy", "Dante Alighieri"],
            ["9971-5-0210-0", "A Tale of Two Cities", "Charles Dickens"],
            ["960-425-059-0", "The Lord of the Rings", "J. R. R. Tolkien"],
            ["80-902734-1-6", "And Then There Were None", "Agatha Christie"],
        ]
    )

    table.render(io)

    expected = """\
┌───────────────┬──────────────────────────┬──────────────────┐
│ ISBN          │ Title                    │ Author           │
├───────────────┼──────────────────────────┼──────────────────┤
│ 99921-58-10-7 │ Divine Comedy            │ Dante Alighieri  │
│ 9971-5-0210-0 │ A Tale of Two Cities     │ Charles Dickens  │
│ 960-425-059-0 │ The Lord of the Rings    │ J. R. R. Tolkien │
│ 80-902734-1-6 │ And Then There Were None │ Agatha Christie  │
└───────────────┴──────────────────────────┴──────────────────┘
"""

    assert expected == io.fetch_output()


def test_render_no_border(io):
    table = Table(TableStyle.borderless())
    table.set_header_row(["ISBN", "Title", "Author"])
    table.add_rows(
        [
            ["99921-58-10-7", "Divine Comedy", "Dante Alighieri"],
            ["9971-5-0210-0", "A Tale of Two Cities", "Charles Dickens"],
            ["960-425-059-0", "The Lord of the Rings", "J. R. R. Tolkien"],
            ["80-902734-1-6", "And Then There Were None", "Agatha Christie"],
        ]
    )

    table.render(io)

    expected = """\
ISBN          Title                    Author
============= ======================== ================
99921-58-10-7 Divine Comedy            Dante Alighieri
9971-5-0210-0 A Tale of Two Cities     Charles Dickens
960-425-059-0 The Lord of the Rings    J. R. R. Tolkien
80-902734-1-6 And Then There Were None Agatha Christie
"""

    assert expected == io.fetch_output()


def test_render_empty(io):
    table = Table(TableStyle.ascii())
    table.render(io)

    assert "" == io.fetch_output()


def test_render_alignment(io):
    style = TableStyle.ascii()
    style.set_column_alignment(1, Alignment.CENTER)
    style.set_column_alignment(2, Alignment.RIGHT)

    table = Table(style)
    table.set_header_row(["ISBN", "Title", "Author"])
    table.add_rows(
        [
            ["99921-58-10-7", "Divine Comedy", "Dante Alighieri"],
            ["9971-5-0210-0", "A Tale of Two Cities", "Charles Dickens"],
            ["960-425-059-0", "The Lord of the Rings", "J. R. R. Tolkien"],
            ["80-902734-1-6", "And Then There Were None", "Agatha Christie"],
        ]
    )

    table.render(io)

    expected = """\
+---------------+--------------------------+------------------+
| ISBN          |          Title           |           Author |
+---------------+--------------------------+------------------+
| 99921-58-10-7 |      Divine Comedy       |  Dante Alighieri |
| 9971-5-0210-0 |   A Tale of Two Cities   |  Charles Dickens |
| 960-425-059-0 |  The Lord of the Rings   | J. R. R. Tolkien |
| 80-902734-1-6 | And Then There Were None |  Agatha Christie |
+---------------+--------------------------+------------------+
"""

    assert expected == io.fetch_output()


def test_render_with_word_wrapping(io):
    style = TableStyle.ascii()

    table = Table(style)
    table.set_header_row(["ISBN", "Title", "Author"])
    table.add_rows(
        [
            [
                "99921-58-10-7",
                "Divine Comedy Divine Comedy Divine Comedy Divine Comedy Divine Comedy ",
                "Dante Alighieri",
            ],
            [
                "9971-5-0210-0",
                "A Tale of Two Cities",
                "Charles Dickens Charles Dickens Charles Dickens",
            ],
            ["960-425-059-0", "The Lord of the Rings", "J. R. R. Tolkien"],
            ["80-902734-1-6", "And Then There Were None", "Agatha Christie"],
        ]
    )

    table.render(io)

    expected = """\
+---------------+------------------------------------+-------------------------+
| ISBN          | Title                              | Author                  |
+---------------+------------------------------------+-------------------------+
| 99921-58-10-7 | Divine Comedy Divine Comedy Divine | Dante Alighieri         |
|               | Comedy Divine Comedy Divine Comedy |                         |
| 9971-5-0210-0 | A Tale of Two Cities               | Charles Dickens Charles |
|               |                                    | Dickens Charles Dickens |
| 960-425-059-0 | The Lord of the Rings              | J. R. R. Tolkien        |
| 80-902734-1-6 | And Then There Were None           | Agatha Christie         |
+---------------+------------------------------------+-------------------------+
"""

    assert expected == io.fetch_output()


def test_render_with_word_wrapping_utf8(io):
    style = TableStyle.ascii()

    table = Table(style)
    table.set_header_row(["ISBN", "Title", "Author"])
    table.add_rows(
        [
            [
                "99921-58-10-7",
                "Diviné Cömédy Diviné Cömédy Diviné Cömédy Diviné Cömédy Diviné Cömédy ",
                "Dante Alighieri",
            ],
            [
                "9971-5-0210-0",
                "A Tale of Two Cities",
                "Charles Dickens Charles Dickens Charles Dickens",
            ],
            ["960-425-059-0", "The Lord of the Rings", "J. R. R. Tolkien"],
            ["80-902734-1-6", "And Then There Were None", "Agatha Christie"],
        ]
    )

    table.render(io)

    expected = """\
+---------------+------------------------------------+-------------------------+
| ISBN          | Title                              | Author                  |
+---------------+------------------------------------+-------------------------+
| 99921-58-10-7 | Diviné Cömédy Diviné Cömédy Diviné | Dante Alighieri         |
|               | Cömédy Diviné Cömédy Diviné Cömédy |                         |
| 9971-5-0210-0 | A Tale of Two Cities               | Charles Dickens Charles |
|               |                                    | Dickens Charles Dickens |
| 960-425-059-0 | The Lord of the Rings              | J. R. R. Tolkien        |
| 80-902734-1-6 | And Then There Were None           | Agatha Christie         |
+---------------+------------------------------------+-------------------------+
"""

    assert expected == io.fetch_output()


def test_render_with_more_word_wrapping(io):
    style = TableStyle.ascii()

    table = Table(style)
    table.set_header_row(["ISBN", "Title", "Author"])
    table.add_rows(
        [
            [
                "99921-58-10-7 99921-58-10-7 99921-58-10-7 99921-58-10-7",
                "Divine Comedy Divine Comedy Divine Comedy Divine Comedy Divine Comedy ",
                "Dante Alighieri",
            ],
            [
                "9971-5-0210-0",
                "A Tale of Two Cities",
                "Charles Dickens Charles Dickens Charles Dickens",
            ],
            ["960-425-059-0", "The Lord of the Rings", "J. R. R. Tolkien"],
            ["80-902734-1-6", "And Then There Were None", "Agatha Christie"],
        ]
    )

    table.render(io)

    expected = """\
+---------------+------------------------------------+-------------------------+
| ISBN          | Title                              | Author                  |
+---------------+------------------------------------+-------------------------+
| 99921-58-10-7 | Divine Comedy Divine Comedy Divine | Dante Alighieri         |
| 99921-58-10-7 | Comedy Divine Comedy Divine Comedy |                         |
| 99921-58-10-7 |                                    |                         |
| 99921-58-10-7 |                                    |                         |
| 9971-5-0210-0 | A Tale of Two Cities               | Charles Dickens Charles |
|               |                                    | Dickens Charles Dickens |
| 960-425-059-0 | The Lord of the Rings              | J. R. R. Tolkien        |
| 80-902734-1-6 | And Then There Were None           | Agatha Christie         |
+---------------+------------------------------------+-------------------------+
"""

    assert expected == io.fetch_output()


def test_render_with_word_cuts(io):
    style = TableStyle.ascii()

    table = Table(style)
    table.set_header_row(["ISBN", "Title", "Author"])
    table.add_rows(
        [
            [
                "99921-58-10-7",
                "DivineComedyDivineComedyDivineComedyDivineComedyDivineComedy ",
                "Dante Alighieri",
            ],
            [
                "9971-5-0210-0",
                "A Tale of Two Cities",
                "Charles Dickens Charles Dickens Charles Dickens",
            ],
            ["960-425-059-0", "The Lord of the Rings", "J. R. R. Tolkien"],
            ["80-902734-1-6", "And Then There Were None", "Agatha Christie"],
        ]
    )

    table.render(io)

    expected = """\
+---------------+----------------------------------+-------------------------+
| ISBN          | Title                            | Author                  |
+---------------+----------------------------------+-------------------------+
| 99921-58-10-7 | DivineComedyDivineComedyDivineCo | Dante Alighieri         |
|               | medyDivineComedyDivineComedy     |                         |
| 9971-5-0210-0 | A Tale of Two Cities             | Charles Dickens Charles |
|               |                                  | Dickens Charles Dickens |
| 960-425-059-0 | The Lord of the Rings            | J. R. R. Tolkien        |
| 80-902734-1-6 | And Then There Were None         | Agatha Christie         |
+---------------+----------------------------------+-------------------------+
"""

    assert expected == io.fetch_output()


def test_render_with_word_wrapping_and_indentation(io):
    style = TableStyle.ascii()

    table = Table(style)
    table.set_header_row(["ISBN", "Title", "Author"])
    table.add_rows(
        [
            [
                "99921-58-10-7",
                "Divine Comedy Divine Comedy Divine Comedy Divine Comedy Divine Comedy ",
                "Dante Alighieri",
            ],
            [
                "9971-5-0210-0",
                "A Tale of Two Cities",
                "Charles Dickens Charles Dickens Charles Dickens",
            ],
            ["960-425-059-0", "The Lord of the Rings", "J. R. R. Tolkien"],
            ["80-902734-1-6", "And Then There Were None", "Agatha Christie"],
        ]
    )

    table.render(io, indentation=4)

    expected = """\
    +---------------+-----------------------------+-------------------------+
    | ISBN          | Title                       | Author                  |
    +---------------+-----------------------------+-------------------------+
    | 99921-58-10-7 | Divine Comedy Divine Comedy | Dante Alighieri         |
    |               | Divine Comedy Divine Comedy |                         |
    |               | Divine Comedy               |                         |
    | 9971-5-0210-0 | A Tale of Two Cities        | Charles Dickens Charles |
    |               |                             | Dickens Charles Dickens |
    | 960-425-059-0 | The Lord of the Rings       | J. R. R. Tolkien        |
    | 80-902734-1-6 | And Then There Were None    | Agatha Christie         |
    +---------------+-----------------------------+-------------------------+
"""

    assert expected == io.fetch_output()


def test_render_formatted_cells(io):
    table = Table(TableStyle.ascii())
    table.set_header_row(["ISBN", "Title", "Author"])
    table.add_rows(
        [
            ["<b>99921-58-10-7</b>", "Divine Comedy", "Dante Alighieri"],
            ["<b>9971-5-0210-0</b>", "A Tale of Two Cities", "Charles Dickens"],
            ["<b>960-425-059-0</b>", "The Lord of the Rings", "J. R. R. Tolkien"],
            ["<b>80-902734-1-6</b>", "And Then There Were None", "Agatha Christie"],
        ]
    )

    table.render(io)

    expected = """\
+---------------+--------------------------+------------------+
| ISBN          | Title                    | Author           |
+---------------+--------------------------+------------------+
| 99921-58-10-7 | Divine Comedy            | Dante Alighieri  |
| 9971-5-0210-0 | A Tale of Two Cities     | Charles Dickens  |
| 960-425-059-0 | The Lord of the Rings    | J. R. R. Tolkien |
| 80-902734-1-6 | And Then There Were None | Agatha Christie  |
+---------------+--------------------------+------------------+
"""

    assert expected == io.fetch_output()


def test_set_header_row_fails_if_too_many_cells():
    table = Table()

    table.add_row(["a", "b", "c"])

    with pytest.raises(ValueError):
        table.set_header_row(["a", "b", "c", "d"])


def test_set_header_row_fails_if_too_missing_cells():
    table = Table()

    table.add_row(["a", "b", "c"])

    with pytest.raises(ValueError):
        table.set_header_row(["a", "b"])


def test_add_row_fails_if_too_many_cells():
    table = Table()

    table.set_header_row(["a", "b", "c"])

    with pytest.raises(ValueError):
        table.add_row(["a", "b", "c", "d"])


def test_add_row_fails_if_too_missing_cells():
    table = Table()

    table.set_header_row(["a", "b", "c"])

    with pytest.raises(ValueError):
        table.add_row(["a", "b"])


def test_set_row_fails_if_too_many_cells():
    table = Table()

    table.add_row(["a", "b", "c"])
    table.add_row(["a", "b", "c"])

    with pytest.raises(ValueError):
        table.set_row(1, ["a", "b", "c", "d"])


def test_set_row_fails_if_too_missing_cells():
    table = Table()

    table.add_row(["a", "b", "c"])
    table.add_row(["a", "b", "c"])

    with pytest.raises(ValueError):
        table.set_row(1, ["a", "b"])


def test_set_rows(io):
    table = Table()

    table.set_rows([["a", "b", "c"], ["d", "e", "f"]])

    table.render(io)

    table.set_row(1, ["g", "h", "i"])

    table.render(io)

    expected = """\
+---+---+---+
| a | b | c |
| d | e | f |
+---+---+---+
+---+---+---+
| a | b | c |
| g | h | i |
+---+---+---+
"""

    assert expected == io.fetch_output()
