from common import read_lines, blocks_by_blank_line


def test_the_file_reader_gets_all_lines_when_no_blanks():
    assert len(list(read_lines("./src/examples/two_lines.txt"))) == 2


def test_the_file_reader_gets_all_lines_with_blanks():
    assert len(list(read_lines("./src/examples/three_lines_with_a_blank.txt"))) == 3


def test_lines_can_be_broken_into_chunks_by_new_lines():
    lines = read_lines("./src/examples/three_lines_with_a_blank.txt")
    chunks = list(blocks_by_blank_line(lines))

    assert chunks == [
        ["line one"],
        ["line three"],
    ]
