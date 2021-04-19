import datetime

def get_between_day(start_day=None, end_day=None):

    '''
    :param start_day:  开始天
    :param end_day:    结束天
    :return: date_list  开始于结束时间之内的所有天的list
    '''

    start_day = datetime.datetime.strptime(start_day, '%Y-%m-%d')
    end_day = datetime.datetime.strptime(end_day, '%Y-%m-%d')
    date_list = []
    date_list.append(start_day.strftime('%Y-%m-%d'))
    while start_day < end_day:
        start_day += datetime.timedelta(days=+1)  # 日期加一天
        date_list.append(start_day.strftime('%Y-%m-%d'))  # 日期存入列表
    return date_list
