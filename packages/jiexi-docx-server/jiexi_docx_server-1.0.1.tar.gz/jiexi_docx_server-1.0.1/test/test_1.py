# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from jiexiproject.main.main import get_res_dict_math

"""测试试卷题目数量"""


def get_text_nums_of_volume(path):

    # _a = r"D:\解析文档\docx_jiexi\数学、英语docx\数学\2018-2019学年广东省深圳市龙岗区联考八年级（下）期中数学试卷.docx"

    res = get_res_dict_math(path)
    if res:
        return res[1]


if __name__ == "__main__":
    path = r"D:\解析文档\docx_jiexi\数学、英语docx\测试\数学"
    base_path = os.listdir(r"D:\解析文档\docx_jiexi\数学、英语docx\测试\数学")
    for i in base_path:
        nums = get_text_nums_of_volume(path + "//".encode("utf-8") + i)
        print(nums)
    # nums = get_text_nums_of_volume(r"D:\解析文档\docx_jiexi\数学、英语docx\数学\2019-2020学年广东省深圳市福田区八年级（下）期中数学试卷.docx")
    # print(nums)
