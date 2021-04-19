from .get_bug import get_bugs_total
from datetime import datetime


def get_report(product_id, module_id, start_day, end_day):
    # print(datetime.now())

    if not start_day:
        start_day = '2020-01-01'

    if not end_day:
        end_day = datetime.now().strftime("%Y-%m-%d")

    # RD 天维度数量
    day_rd_info = {}
    day_rd_resolve_info = {}
    # qa人员相关
    day_qa_info = {}

    # 调用方法
    bugs, users, total_bug = get_bugs_total(product_id, module_id)
    # 风险
    risks = ''

    # 天维度bug
    day_bug_info = {}

    for bug in bugs:
        # 创建时间的天
        day_bug = bug.get('openedDate').split(' ')[0]

        if start_day<=day_bug and day_bug<=end_day:

            # 重新写一下
            if day_bug_info.get(day_bug) is None:
                day_bug_info[day_bug] = {
                    'bug_total': 0,
                    'bug_open': 0,
                    'bug_closed': 0,
                    'bug_resolve': 0,
                    # BUG等级
                    'bug_crash': 0,
                    'bug_block': 0,
                    'bug_serious': 0,
                    'bug_sort': 0,
                    'bug_propose': 0,
                    'risks': '',
                }
            day_bug_info[day_bug]['bug_total'] += 1
            if bug.get('status') == 'active':
                day_bug_info[day_bug]['bug_open'] += 1
            elif bug.get('status') == 'closed':
                day_bug_info[day_bug]['bug_closed'] += 1
            elif bug.get('status') == 'resolved':
                day_bug_info[day_bug]['bug_resolve'] += 1

            # bug 等级
            if bug.get('severity') == '1':
                day_bug_info[day_bug]['bug_crash'] += 1
            elif bug.get('severity') == '2':
                day_bug_info[day_bug]['bug_block'] += 1
            elif bug.get('severity') == '3':
                day_bug_info[day_bug]['bug_serious'] += 1
            elif bug.get('severity') == '4':
                day_bug_info[day_bug]['bug_sort'] += 1
            elif bug.get('severity') == '5':
                day_bug_info[day_bug]['bug_propose'] += 1

            # 风险录入
            if bug.get('title') == '[风险]':
                new_str = bug.get('steps').replace('<p>', '')
                risks = risks + new_str.replace('</p>', '')
                risks = risks.replace('\n', '<br />')
                day_bug_info[day_bug]['risks'] = risks

        # rd总数统计
        if day_rd_info.get(day_bug) is None:
            day_rd_info[day_bug] = {}

        if bug.get('status') == 'active':
            if day_rd_info[day_bug].get(bug.get('assignedTo')) is None:
                day_rd_info[day_bug][bug.get('assignedTo')] = 1
            else:
                day_rd_info[day_bug][bug.get('assignedTo')] += 1
        else:
            if day_rd_info[day_bug].get(bug.get('resolvedBy')) is None:
                day_rd_info[day_bug][bug.get('resolvedBy')] = 1
            else:
                day_rd_info[day_bug][bug.get('resolvedBy')] += 1

        # rd解决数量
        if day_rd_resolve_info.get(day_bug) is None:
            day_rd_resolve_info[day_bug] = {}

        if bug.get('status') != 'active':
            if day_rd_resolve_info[day_bug].get(bug.get('resolvedBy')) is None:
                day_rd_resolve_info[day_bug][bug.get('resolvedBy')] = 1
            else:
                day_rd_resolve_info[day_bug][bug.get('resolvedBy')] += 1

        # qa统计
        if day_qa_info.get(day_bug) is None:
            day_qa_info[day_bug] = {}

        if day_qa_info[day_bug].get(bug.get('openedBy')) is None:
            day_qa_info[day_bug][bug.get('openedBy')] = 1
        else:
            day_qa_info[day_bug][bug.get('openedBy')] += 1

    # print('end_day_bug_info:', day_bug_info)
    print('day_rd_info:', day_rd_info)
    print('day_rd_resolve_info:', day_rd_resolve_info)
    # print('day_qa_info:', day_qa_info)
    # print('users:', users)
    # print(total_bug)
    # print(datetime.now())
    return day_bug_info, day_rd_info, day_rd_resolve_info, day_qa_info, users


if __name__ == '__main__':
    get_report(120, 1404, '2020-01-01', '2021-01-31')
