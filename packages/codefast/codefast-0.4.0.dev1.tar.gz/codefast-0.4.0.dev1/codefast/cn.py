'''Chinese
'''

punctuations = list('，。‘’“”！？（）、：；《》／-【】『』￥——')


def is_cn(c: str) -> bool:
    return '\u4e00' <= c <= '\u9fa5'


def is_cn_or_punc(c) -> bool:
    if is_cn(c): return True
    return c in punctuations


import re
from typing import List


def split_by_punc(sentence: str) -> List[str]:
    return list(filter(len, re.split('|'.join(punctuations), sentence)))
