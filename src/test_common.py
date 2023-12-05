from common import read_lines


def test_the_file_reader_gets_all_lines_when_no_blanks():
    assert len(list(read_lines("./src/examples/two_lines.txt"))) == 2


def test_the_file_reader_gets_all_lines_with_blanks():
    assert len(list(read_lines("./src/examples/three_lines_with_a_blank.txt"))) == 3
