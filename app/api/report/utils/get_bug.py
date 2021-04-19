import json
import requests


# 使用seesion登录，这样的好处是可以在接下来的访问中可以保留登录信息
session = requests.session()
base_url = "http://gaoxiaobang.5upm.com"


def get_sessionid():
    headers = {}
    params = {}
    url = base_url + "/api-getsessionid.json"
    result = session.get(url, headers=headers, params=params)
    str_data = result.json()['data']
    map_data = json.loads(str_data)     # string to map
    return map_data['sessionID']


def login_cd(sessionid):
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
    }
    params = {
        "account": "yszeng",
        "password": "123456",
        "zentaosid": sessionid,
    }
    url = base_url + "/user-login.json"
    session.post(url, headers=headers, params=params)


def module_bugs_sum(product_id, module_id):
    headers = {}
    params = {}
    url = base_url + "/bug-browse-"+ str(product_id) +"--byModule-"+ str(module_id) +".json"
    result = session.post(url, headers=headers, params=params)

    # 响应结果处理
    result_unicode1 = result.content.decode()       # 解码为unicode
    result_unicode1_map = json.loads(result_unicode1)  # string to map
    # print(type(result_unicode1_map))
    # print(result_unicode1_map['data'])

    # pager 转 map
    data_map = json.loads(result_unicode1_map['data'])
    # print(type(data_map))
    # print(data_map['pager'])

    # return bug total num
    return data_map['pager']['recTotal']


def module_bugs_map(product_id, module_id, total):
    headers = {}
    params = {}
    url = base_url + "/bug-browse-"+ str(product_id) +"--byModule-"+ str(module_id) +"--"+ str(total) +"-2000-1.json"
    result = session.post(url, headers=headers, params=params)

    # 响应结果处理
    result_unicode1 = result.content.decode()       # 解码为unicode
    result_unicode1_map = json.loads(result_unicode1)  # string to map
    # print(type(result_unicode1_map))
    # print(result_unicode1_map['data'])

    # pager 转 map
    data_map = json.loads(result_unicode1_map['data'])
    bugs = data_map['bugs']
    users = data_map['memberPairs']
    # print(type(data_map['bug']))
    # print(type(data_map['bugs'][0]))
    # print(len(data_map['bugs']))
    # print(data_map['bugs'])
    # print(data_map['bugs'][0])
    # print(users)

    # 返回 bug list
    return bugs, users

def bugs_info(bug_id):
    headers = {}
    params = {}
    # http://gaoxiaobang.5upm.com/bug-view-24492.json
    url = base_url + "/bug-view-"+ str(bug_id) +".json"

    result = session.post(url, headers=headers, params=params)

    # 响应结果处理
    result_unicode1 = result.content.decode()       # 解码为unicode
    result_unicode1_map = json.loads(result_unicode1)  # string to map

    # pager 转 map
    data_map = json.loads(result_unicode1_map['data'])
    bug_info = data_map['bug']
    print(bug_info)

    # 返回 bug list
    return bug_info

"/index.php?t=json&m=story&f=ajaxGetProjectStories&projectID={0}"


def get_bugs_total(product_id, module_id):
    sid = get_sessionid()
    login_cd(sid)
    total_bug = module_bugs_sum(product_id, module_id)
    bugs, users = module_bugs_map(product_id, module_id, total_bug)
    # users_bugs = users_bugs_map(product_id, module_id, total_bug)
    return bugs, users, total_bug


if __name__ == '__main__':
    sid = get_sessionid()
    login_cd(sid)
    # total_bug = module_bugs_sum(120, 1404)
    # module_bugs_map(120, 1403, total_bug)
    # get_bugs_total(120, 1403)
    bugs_info(24828)

