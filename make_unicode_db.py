"""
Tool that names each unicode character based on their name or their aliases

Must be run from the cpython repo root directory

Relies on Tools.unicode being an importable path due to implicit packages
"""
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
from pathlib import Path
from unicodedata import unidata_version
from Tools.unicode.makeunicodedata import UnicodeData, makeunicodename


def get_characters():
    unicode_data_path = Path(__file__).parent / "unicode_data.json"
    if unicode_data_path.exists():
        # If unicode_data.json path exists, load data from there
        with unicode_data_path.open(mode="rt") as f:
            characters = json.load(f)
    else:
        # Use CPython's makeunicodedata tool which downloads needed data
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            unicode = UnicodeData(unidata_version)
            makeunicodename(unicode, 1)
        characters = {
            chr(int(r.codepoint, 16)): {"name": r.name, "aliases": []}
            for r in unicode.table
            if r
        }
        for alias, codepoint in unicode.aliases:
            characters[chr(codepoint)]["aliases"].append(alias)
        with unicode_data_path.open(mode="wt") as f:
            json.dump(characters, f)
    return characters


characters = get_characters()


def name(character):
    r"""Like unicodedata.name, but works for unnamed characters like \n."""
    record = characters[character]
    if record["name"].startswith("<"):  # If no name, use the first alias
        return record["aliases"][0]
    return record["name"]
