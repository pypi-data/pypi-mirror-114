from contextlib import contextmanager
from pathlib import Path
import requests

_converters = dict(real=float, integer=int, complex=complex, pattern=bool)


def get_mm_type_converter(t):
    return _converters[t]


def _coord_row_iter(line_num, f, converter, header):
    pattern = header["mm_type"] == "pattern"
    line = f.readline()
    while line:
        line = line.strip()
        row = line.split()
        if pattern:
            yield line_num, int(row[0]), int(row[1]), True
        else:
            yield line_num, int(row[0]), int(row[1]), converter(row[2])
        line = f.readline()
        line_num += 1


def _array_iter(line_num, f, converter, header):
    nrows = header["nrows"]
    general = header["mm_storage"] == "general"
    pattern = header["mm_type"] == "pattern"
    i = -1
    j = 0
    line = f.readline()
    while line:
        i += 1
        if i == nrows:
            j += 1
            if general:
                i = 0
            else:
                i = j
        if pattern:
            yield line_num, i, j, True
        else:
            yield line_num, i, j, converter(line.strip())
        line = f.readline()
        line_num += 1


@contextmanager
def http_stream_opener(url, mode=None):
    s = requests.Session()
    with s.get(url, headers=None, stream=True) as resp:
        resp.readlines = resp.iter_lines
        yield resp


@contextmanager
def suitesparse_opener(uri):
    pass


@contextmanager
def mmread(filename, opener=Path.open, collection=False):

    if isinstance(filename, str):
        if filename.startswith("http"):
            opener = http_stream_opener
        elif filename.startswith("ssmc://"):
            opener = suitesparse_opener
        else:
            filename = Path(filename)

    header = dict(
        mm_format="coordinate",
        mm_type="real",
        mm_storage="general",
    )
    got_mm_header = False

    nrows = 0
    ncols = 0
    nvals = 0

    line_num = 0
    with opener(filename, "r") as f:
        line = f.readline()
        while line:
            lower_line = line.strip().lower()
            if line_num == 0 and lower_line.startswith("%%matrixmarket"):
                _, mm_format, mm_type, mm_storage = lower_line[14:].split()

                if mm_format not in ("coordinate", "array"):
                    raise TypeError(f"Invalid format {mm_format}")

                if mm_type not in ("integer", "real", "pattern"):
                    raise TypeError(f"Invalid type {mm_type}")

                if mm_storage not in (
                    "general",
                    "symmetric",
                    "skew-symmetric",
                    "hermitian",
                ):
                    raise TypeError(f"Invalid storage {mm_storage}")

                header["mm_format"] = mm_format
                header["mm_type"] = mm_type
                header["mm_storage"] = mm_storage
                got_mm_header = True

            elif (
                line_num == 1 and got_mm_header and lower_line.startswith("%%graphblas")
            ):
                header["gb_type"] = line[11:]

            elif line.lstrip().startswith("%"):
                line_num += 1
                line = f.readline()
                continue

            else:
                data_row = list(map(int, line.split()))
                data_row_len = len(data_row)
                if data_row_len not in (2, 3):
                    raise TypeError(
                        f"Invalid data row {data_row} on line {line_num} must have only 2 or 3 entries"
                    )
                if mm_format == "array":
                    nrows, ncols = data_row
                    nvals = nrows * ncols
                    _iter = _array_iter
                else:
                    nrows, ncols, nvals = data_row
                    _iter = _coord_row_iter
                header.update(nrows=nrows, ncols=ncols, nvals=nvals)
                break
            line_num += 1
            line = f.readline()

        converter = _converters[mm_type]

        yield header, _iter(line_num, f, converter, header)
