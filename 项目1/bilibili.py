import requests
import re
import urllib.parse
import hashlib
import time
from pprint import pprint
from math import ceil
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import schedule

# 浏览器身份信息
headers = {
    'accept':'*/*',
    'accept-encoding':'gzip, deflate, br, zstd',
    'accept-language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cookie':"",
    'origin':'https://space.bilibili.com',
    'pragma':'no-cache',
    'priority':'u=1, i',
    'referer':'https://space.bilibili.com/86758610/upload/video',
    'sec-ch-ua':'"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',
    'sec-ch-ua-mobile':'?0',
    'sec-ch-ua-platform':"Windows",
    'sec-fetch-dest':'empty',
    'sec-fetch-mode':'cors',
    'sec-fetch-site':'same-site',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0'
}

# 单页数据获取
def tougao_data(pn, mid):
    url = 'https://api.bilibili.com/x/space/wbi/arc/search?'
    payload = {
        'pn': pn,  # 页码
        'ps': '40',
        'tid': '0',
        'special_type': '',
        'order': 'pubdate',
        'mid': mid,  # up主ID
        'index': '0',
        'keyword': '',
        'order_avoided': 'true',
        'platform': 'web',
        'web_location': '333.1387',
        'dm_img_list': '[]',
        'dm_img_str': 'V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ',
        'dm_cover_img_str': 'QU5HTEUgKEludGVsLCBJbnRlbChSKSBJcmlzKFIpIFhlIEdyYXBoaWNzICgweDAwMDA0NkE2KSBEaXJlY3QzRDExIHZzXzVfMCBwc181XzAsIEQzRDExKUdvb2dsZSBJbmMuIChJbnRlbC',
        'dm_img_inter': '{"ds":[],"wh":[2050,-100,36],"of":[475,950,475]}',
        'w_webid': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzcG1faWQiOiIzMzMuOTk5IiwiYnV2aWQiOiJCOUFENTZBOC03NEJGLTQzNTMtQjA2Ri1EREQ3MEVCMzk2NjUwNzgwNWluZm9jIiwidXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdpbjY0OyB4NjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xMzQuMC4wLjAgU2FmYXJpLzUzNy4zNiBFZGcvMTM0LjAuMC4wIiwiYnV2aWRfZnAiOiIxZWMyYWY5MmJjYmFlOGUzYTQ0OTc0MDY2YThkNzkzYSIsImJpbGlfdGlja2V0IjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJbXRwWkNJNkluTXdNeUlzSW5SNWNDSTZJa3BYVkNKOS5leUpsZUhBaU9qRTNORE01TkRFNU9EVXNJbWxoZENJNk1UYzBNelk0TWpjeU5Td2ljR3gwSWpvdE1YMC5KLW44cmR4U3hiWUFKZFFnUG1zVGZRSkg3d2FOXzJ4UmJUTjY1cFp0WXNzIiwiY3JlYXRlZF9hdCI6MTc0MzY4OTYxOCwidHRsIjo4NjQwMCwidXJsIjoiLzg2NzU4NjEwL3VwbG9hZC92aWRlbyIsInJlc3VsdCI6MCwiaXNzIjoiZ2FpYSIsImlhdCI6MTc0MzY4OTYxOH0.D9DR9mtO4HKnhUmsgbLUErHyplOea1_iR7BsD9rghc5JGGdmraPoKCUb8RTe6K6iceK4xw9kQ3zVa_C__oUcbW_HOX-QQt1DTz_2dsZlUoWmbH9_NGHSy0eKmGAHe7pcJwuZJj_I7wlcZ5dqkfkeNs95wDZTa9IVkP5GsWSTpEqYZ-hop2SmmRaelVkQSeK5UXpezjrpnHqJiEW1lKmobYwDDhs4r6NyAYj1HXSqX-zcG-V_jlL7lvhfRqExj8Cx1f9V5FKn0d0cg0tkCagAIcQZzT9iie-aL4U1MlJmYHRRm5l1z9902_8HryyUNk6qBJw02b2S7jycADOf27PjJw',
        # 'w_rid': '133eaaecc26457d761df24791e3238be',
        'wts': int(time.time())  # 时间戳
    }

    # JS逆向代码
    # 计算f参数
    l = sorted(payload.keys())
    c = []
    pattern = re.compile(r"[!'()*]")  # 匹配需要替换的字符
    for key in l:
        value = payload[key]
        if value is not None:
            # 如果是字符串类型，替换特定字符
            if isinstance(value, str):
                value = pattern.sub('', value)
            # 对键和值进行URL编码
            encoded_key = urllib.parse.quote(key, safe='')
            encoded_value = urllib.parse.quote(str(value), safe='')
            c.append(f"{encoded_key}={encoded_value}")
    f = '&'.join(c)
    print(f)
    # o参数固定值
    o = "ea1db124af3c7062474693fa704f4ff8"
    # 计算w_rid: MD5(f+o)
    combined = f + o
    w_rid = hashlib.md5(combined.encode('utf-8')).hexdigest()
    payload['w_rid'] = w_rid

    # 数据请求
    res = requests.get(url, params=payload, headers=headers)
    # pprint(res.json())
    return res.json()

# 批量多页数据获取 → 分页存入list
def batch_data(mid):
    data_list = []

    data = tougao_data(pn=1, mid=mid)
    data_list.append(data)
    page_info = data['data']['page']
    loop_num = ceil(page_info['count'] / page_info['ps']) + 1

    for page in range(2, loop_num):
        data = tougao_data(pn=page, mid=mid)
        data_list.append(data)

    return data_list

# 数据处理：目标数据提取+拼接所有页+添加字段
def parse_data(raw_data):
    all_df = pd.DataFrame()
    for data in raw_data:
        vlist = data['data']['list']['vlist']
        df = pd.DataFrame(vlist)
        all_df = pd.concat([all_df, df], axis=0, ignore_index=True)
    all_df['获取时间'] = datetime.now()
    return all_df

# 数据存储：单个excel文件
def save_data(new_df):
    history_path = rf'./up数据/up投稿数据.xlsx'
    history_df = pd.read_excel(history_path)
    history_df = pd.concat([new_df, history_df])
    history_df.to_excel(history_path, index=False)

# 数据存储：数据库
# def save_data_db(new_df):
#     del new_df['description']  # 删除含emoji列
#     engine = create_engine("mysql+mysqldb://wangyisheng:Amazing2019!@rm-uf65dt8ph1r23763r0o.mysql.rds.aliyuncs.com:3306/bilibili?charset=utf8mb4")
#     new_df.to_sql('bili_video_data', engine, if_exists='append', index=False)

# 计算增量数据，存入excel → 供Tableau看板使用
def parse_data_for_bi():
    df = pd.read_excel(r'./up数据/up投稿数据.xlsx')
    df.sort_values(by=['获取时间'], ascending=False, inplace=True)
    gp = df.groupby(['author', 'title', 'bvid'], as_index=False)
    df['昨日播放数'] = gp['play'].shift(-1)  # 组内偏移
    df['播放增长'] = df['play'] - df['昨日播放数']
    df.to_excel(r'./up数据/up投稿数据_parse.xlsx', index=False)

# 任务流
def job():
    mid = '86758610'  # 可以批量导入多个up主ID
    data_list = batch_data(mid)
    df = parse_data(data_list)
    save_data(df)  # 存储处理后数据到excel
    # parse_data_for_bi()  # 基于excel数据计算增量数据，存入新的excel文件

if __name__ == '__main__':
    # 定时调度
    # schedule.every().day.at('10:30').do(job)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    job()


