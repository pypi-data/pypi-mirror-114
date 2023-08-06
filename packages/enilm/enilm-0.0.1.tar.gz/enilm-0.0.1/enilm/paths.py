"""Any helpers related to paths on different OS's"""
import re
from pathlib import Path
from typing import Union


def to_full_wsl(win_path: Union[str, Path]) -> str:
    r"""
    convert win path to wsl (with /mnt/ prefix)
    e.g.:
        C:\Users\Student -> /mnt/c/Users/Student
    """
    path_re = re.compile(r"^([A-Z]):(.*)")
    match = path_re.match(str(win_path))
    if match is None:
        raise ValueError(r"Path must match the regex ^([A-Z]):(.*), e.g. C:\Users\Student")
    driver = match.group(1)
    rest = match.group(2).replace("\\", "/")  # \Users\Student -> /Users/Student
    return f"/mnt/{driver.lower()}{rest}"
