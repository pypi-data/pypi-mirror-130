#!/usr/bin/python
# encoding=utf-8

"""
@Author  :  Lijiawei
@Date    :  2021/12/11 11:22 上午 
@Desc    :  main line.
"""
from .platform import TextProcessor


def test():
    processor = TextProcessor()
    print(processor.PLUGINS)  # {’plugin1': <class '__main__.CleanMarkdownBolds'>}
    processed = processor.process(text="**foo bar**", plugins=('pg1',))
    print(processed)
    processed = processor.process(text="--foo bar--")
    print(processed)

