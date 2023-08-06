"""
小小明的代码
CSDN主页：https://blog.csdn.net/as604049322
"""

import difflib
import os

import cchardet


def file_diff_compare(file1, file2, diff_out="diff_result.html", max_width=70, numlines=0, show_all=False):
    with open(file1, "rb") as f:
        bytes: bytes = f.read()
        text1 = bytes.decode(cchardet.detect(bytes)['encoding'])
        text1 = text1.splitlines(keepends=True)
    with open(file2, "rb") as f:
        bytes: bytes = f.read()
        text2 = bytes.decode(cchardet.detect(bytes)['encoding'])
        text2 = text2.splitlines(keepends=True)

    d = difflib.HtmlDiff(wrapcolumn=max_width)
    with open(diff_out, 'w', encoding="u8") as f:
        f.write(d.make_file(text1, text2, context=not show_all, numlines=numlines))
    abspath = os.path.abspath(diff_out).replace("\\", "/")
    return f"file:///{abspath}"
