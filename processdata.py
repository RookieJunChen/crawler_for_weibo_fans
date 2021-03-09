import re
import json


# 整理数据
def organize_data(input_dataset):
    keyset = {'昵称'}
    sorted_dataset = []
    for data in input_dataset:
        for key in data.keys():
            if key in keyset:
                pass
            else:
                keyset.add(key)
    for data in input_dataset:
        for key in keyset:
            if key in data.keys():
                pass
            else:
                data[key] = '未知'
        sorted_dataset.append(data)
    return sorted_dataset


# 数据去重
def delete_duplication(input_dataset):
    name_set = {'烂柯人201506'}
    for data in input_dataset:
        if data['昵称'] in name_set:
            input_dataset.remove(data)
        else:
            name_set.add(data['昵称'])
    return input_dataset


# 通过正则表达式提取出地域
def get_address(info):
    address_format = re.compile(r"((甘肃|北京|海外|天津|河北|山西|内蒙古|辽宁|吉林|黑龙江|上海|江苏|浙江|安徽|福建|江西|山东|河南|湖北|湖南"
                                r"|广东|广西|海南|重庆|四川|贵州|云南|西藏|陕西|青海|宁夏|新疆|台湾|香港|澳门) [\u4E00-\u9FA5]+)"
                                r"|(甘肃|北京|海外|天津|河北|山西|内蒙古|辽宁|吉林|黑龙江|上海|江苏|浙江|安徽|福建|江西|山东|河南|湖北|湖南"
                                r"|广东|广西|海南|重庆|四川|贵州|云南|西藏|陕西|青海|宁夏|新疆|台湾|香港|澳门|其他)")
    result = address_format.search(info)
    if result:
        return result.group(0)
    else:
        return '未知'


# 通过正则表达式提取出年龄
def get_age(info):
    age_format = re.compile(r"(\d)+岁")
    result = age_format.search(info)
    if result:
        return result.group(0)
    else:
        return '未知'


# 通过正则表达式提取出星座
def get_constellation(info):
    constellation_format = re.compile("[\u4E00-\u9FA5]+座")
    result = constellation_format.search(info)
    if result:
        return result.group(0)
    else:
        return '未知'


if __name__ == "__main__":
    file = 'easy_result.json'
    fp = open(file, 'r')
    data = json.load(fp)
    fp.close()

    organize_data(data)
    for d in data:
        print(d)

    data.append(data[2])
    print(len(data))

    delete_duplication(data)
    for d in data:
        print(d)
    print(len(data))
