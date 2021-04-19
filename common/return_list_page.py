# -*- coding: utf-8 -*-
from .pager import Pager


def list_page(data_list, page_size, page_num):
    """
    分页组装list信息，
    返回当页数据list和总页数total
    """
    if page_num:
        pager = Pager(data_list, page_size)
        data = pager.page_data(page_num)
        total = pager.page_total_num
    else:
        data = data_list
        total = 1
    return data, total
