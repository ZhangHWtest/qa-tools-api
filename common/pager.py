#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Pager:
    """数据分页"""
    def __init__(self, data_list, page_size=None):
        self.data = data_list  # 总数据
        self.page_size = page_size  # 单页大小
        self.is_start = False
        self.is_end = False
        self.data_count = len(data_list)     # 数据总数
        self.next_page = 0  # 下一页
        self.previous_page = 0  # 上一页
        if page_size:
            self.page_total_num = self.data_count / page_size     # 总页数
            if self.page_total_num == int(self.page_total_num):
                self.page_total_num = int(self.page_total_num)
            else:
                self.page_total_num = int(self.page_total_num) + 1
        else:
            self.page_total_num = 1

    def page_data(self, page_num=None):
        """
        获取一页的数据
        :param page_num: 要返回数据的页码
        :return: 如果页码超过总页码，返回空列表，否则返回一页的数据
        """
        if not page_num:
            return self.data
        if page_num > self.page_total_num:
            return []
        self.next_page = page_num + 1
        self.previous_page = page_num - 1
        if page_num == 1:
            self.is_start = True
            if self.page_total_num == 1:
                return self.data
        elif page_num == self.page_total_num:
            self.is_end = True
        if self.is_end:
            return self.data[(page_num - 1) * self.page_size:]
        else:
            return self.data[(page_num - 1) * self.page_size:page_num * self.page_size]


if __name__ == '__main__':
    data = list()
    for i in range(22):
        data.append(i)
    page = Pager(data, 5)
    print(page.page_data(1))
