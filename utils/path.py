# -*- coding: utf-8 -*-
# Author : Cane
# Contact: caneman@163.com
# File   : path.py
# Time   : 2024/3/25 15:10

import os
from typing import Union, List


#  环境变量
def get_env(name: str, default: str = '', split: bool = True) -> Union[str, List[str], None]:
    if default:
        value_str = default.strip()
    else:
        value_str = os.environ.get(name)

    if not value_str:
        return None

    if not split:
        return value_str.strip()

    value_list = value_str.strip().split(';')
    if len(value_list) == 1:
        return value_list[0]
    else:
        return value_list


if __name__ == '__main__':
    pass
