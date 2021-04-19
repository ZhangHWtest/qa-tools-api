"""
字典的合并
"""


def hebingDict(dict_list: dict):
    dictMerged = {}
    for item in dict_list:
        try:
            dictMerged.update(eval(item))
        except Exception as e:
            print(e)
    return dictMerged
