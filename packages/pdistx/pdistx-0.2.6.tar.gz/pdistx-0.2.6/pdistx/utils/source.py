from pathlib import Path
import re


def detect_source_encoding(path: Path):
    # according to PEP 0263
    # https://www.python.org/dev/peps/pep-0263/

    # read first two lines
    with open(path, 'rb') as file:
        lines = [file.readline(), file.readline()]

    # check if first line starts with a bom
    if lines[0].startswith(b'\xef\xbb\xbf'):
        return 'utf-8'

    # check for encoding marker
    for line in lines:
        m = re.match(rb'^[ \t\f]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)', line)
        if m:
            return m.group(1).decode('latin-1')

    # default encoding
    return 'utf-8'


def read_source(path: Path):
    # detect encoding
    encoding = detect_source_encoding(path)

    # read all lines with proper encoding
    with open(path, 'r', encoding=encoding) as file:
        lines = file.read().split('\n')

    # remove encoding markers (see PEP 0263)
    for i in range(0, min(2, len(lines))):
        if re.match(r'^[ \t\f]*#.*?coding[:=]', lines[i]):
            lines[i] = ''

    # join lines and done
    return '\n'.join(lines)
