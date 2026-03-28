import base64
import json
import gzip
import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii
from pprint import pprint
import requests
import pandas as pd
import os
from datetime import date, timedelta
import schedule
import time

# 全局变量-请求标头
headers = {
    'accept':'application/json, text/plain, */*',
    'accept-encoding':'gzip, deflate, br, zstd',
    'accept-language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control':'no-cache',
    'cookie':'',
    'origin':'https://www.chanmama.com',
    'pragma':'no-cache',
    'priority':'u=1, i',
    'referer':'https://www.chanmama.com/bloggerRank/_ISK2rs8iAP3gowCHnHIGy4iu5oITwXf.html?activeTab=live',
    'sec-ch-ua':'"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
    'sec-ch-ua-mobile':'?0',
    'sec-ch-ua-platform':"Windows",
    'sec-fetch-dest':'empty',
    'sec-fetch-mode':'cors',
    'sec-fetch-site':'same-site',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
    'x-client-hash':'238c297e40532fd37ca098637f852b70e6768d66',
    'x-client-id':'67742636',
    'x-client-version':'1',
    'x-encrypt-version':'2',
    'x-platform-id':'10000'
}

# 解码函数
def decrypt(data):
    n = {
        "words": [
            1265252208,
            1366438980,
            1714975542,
            1951949399
        ],
        "sigBytes": 16
    }

    # 转换密钥（验证密钥长度）
    try:
        key_bytes = b''.join(struct.pack('>I', word) for word in n['words'])[:n['sigBytes']]
        if len(key_bytes) not in {16, 24, 32}:
            raise ValueError(f"Invalid AES key length: {len(key_bytes)} bytes")
    except struct.error as e:
        raise ValueError("Invalid word value in key") from e

    # 处理Base64解码
    try:
        ciphertext = base64.b64decode(data)
    except binascii.Error as e:
        raise ValueError("Invalid base64 encoding") from e

    # AES解密
    try:
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        decrypted_data = cipher.decrypt(ciphertext)
        unpadded_data = unpad(decrypted_data, AES.block_size)
    except ValueError as e:
        raise ValueError("Decryption or unpadding failed") from e


    # 尝试多种解码方式
    def try_decode(data):
        # 先尝试直接解码为JSON
        try:
            return json.loads(data.decode('utf-8'))
        except UnicodeDecodeError:
            pass

        # 尝试gzip解压
        try:
            if data[:2] == b'\x1f\x8b':  # gzip magic number
                return json.loads(gzip.decompress(data).decode('utf-8'))
        except (gzip.BadGzipFile, EOFError, OSError):
            pass

        # 尝试其他编码（按常见编码逐个尝试）
        for encoding in ['latin-1', 'utf-16', 'utf-16-le', 'utf-16-be']:
            try:
                return json.loads(data.decode(encoding))
            except UnicodeDecodeError:
                continue

        # 显示前16字节帮助调试
        hex_prefix = ' '.join(f'{b:02x}' for b in data[:16])
        raise ValueError(f"无法解码数据，前16字节: {hex_prefix}...")


    # 最终解析
    json_data = try_decode(unpadded_data)
    pprint(json_data)
    return json_data


# 单个达人直播数据
def get_parse_live_data(author_id, nickname, start_date, end_date):
    url = 'https://api-service.chanmama.com/v2/author/detail/liveAnalysisV2?'
    params = {
        'author_id': author_id,
        'start_date': start_date,
        'end_date': end_date,
        'is_contain_today': 'true',
    }
    res = requests.get(url, params=params, headers=headers)
    data = decrypt(res.json()['data']['data'])  # 解码data密文

    gpm = pd.DataFrame(data['gpm'])  # 提取gpm模块数据
    trends = pd.DataFrame(data['trends'])  # 提取trends模块数据

    url_traffic = 'https://api-service.chanmama.com/v1/author/detail/authorLiveTraffic'
    post_data = {"pk_author_id_arr":[],
                 "author_id":author_id,
                 "start_date":start_date,
                 "end_date":end_date,
                 "need_day_chart":1}
    traffic_res = requests.post(url_traffic, json=post_data, headers=headers)
    day_self_traffic = pd.DataFrame(traffic_res.json()['data']['day_self_traffic'])
    day_self_traffic['date_str'] = pd.to_datetime(day_self_traffic['day'], format='%Y%m%d').dt.strftime('%Y-%m-%d')


    pe_url = 'https://api-service.chanmama.com/v2/author/detail/livePenetrationTrend?'
    pe_res = requests.get(url=pe_url, params=params, headers=headers)
    pe_data = decrypt(pe_res.json()['data']['data'])
    exposed = pd.DataFrame(pe_data['list'])
    exposed['date_str'] = pd.to_datetime(exposed['date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')

    df_dict = {'gpm': gpm,
               'trends': trends,
               'day_self_traffic': day_self_traffic,
               'exposed': exposed}

    for name, df in df_dict.items():  # 表名+dataframe
        df['达人昵称'] = nickname  # 每张表添加达人昵称和ID字段
        df['达人ID'] = author_id
        df.to_excel(rf'./达人数据/{nickname}_{name}_{start_date}_{end_date}.xlsx', index=False)  # 每个达人导出4张表

# 多个达人直播数据
def job():
    # yesterday = date.today() - timedelta(days=1)
    # start_date = yesterday.strftime('%Y-%m-%d')
    # end_date = yesterday.strftime('%Y-%m-%d')
    start_date = '2025-02-01'
    end_date = '2025-03-31'

    author_dict = {'_ISK2rs8iAP3gowCHnHIGy4iu5oITwXf': '应季物语官方旗舰店',
                   'D9ZEcvDTS0HlGfXU0mULfv9ipkbiwZD1': '新边界食品旗舰店',
                   'FRa9mDjpDah5GyNLBDDCrlN9AYrhM3yx': '马小养食品优选',
                   '9dLMU0nPCftPs_6uTVXBiQ': '牧果人旗舰店',
                   'hLH4NhPh1jtLL6f0xrDOAw': '臻味官方旗舰店'
                   }

    #  获取并存储：给定日期区间 所有达人4张主题表
    for author_id, nickname in author_dict.items():
        get_parse_live_data(author_id=author_id, nickname=nickname, start_date=start_date, end_date=end_date)

    name_list = ['gpm', 'trends', 'day_self_traffic', 'exposed']  # 4张主题表名
    excel_list = os.listdir(r'./达人数据')  # 文件夹中所有表名

    # 4张主题表整合：每张主题表整合所有达人该主题数据
    for name in name_list:
        empty_df = pd.DataFrame()

        for excel in excel_list:
            if name in excel:  # 如果excel表名中包含主题表名，则读取该表并追加到empty_df
                temp_df = pd.read_excel(r'./达人数据/' + excel)
                empty_df = pd.concat([empty_df, temp_df])

        empty_df.to_excel(f'./达人整合数据/{name}.xlsx', index=False)

if __name__ == '__main__':
    # e = "VMftTMf+Rdynw5YuJ22on6Ve64YCCMEs8jFju/+9UKPROhggJI03V0eQOF10/Yl8Yjb4DvVwGfBc6/HpFR1dJxN75RCSg3NcC2hXPtYVfalBYzyX55lLdQqEeTvQiC0BTBLwcAiMrrRMjKDwPFhnKLZlf5PtqUPpS3JwQl8HMHgcF8YAC5cmtlqoqAS3CG1TaWQ9hXT/84NX40jSymt3JTQQz0vh2LrTOPaBQJ++LukU+8jcM19OwZXhOXnETnPM4vfNg8QY264A29uAqtBFyfrgN6u3DhqAZekH1ieUd6eJEm8RRlNKgrPYOtY9Qf9ufLEwQg8GcqpAByE2HBoloRLVMA7sHX/DNXo2+hBHwwnjO7QCQ9BI94F3JYyJogBxjVqph6o+OD1hWfEpWEeGcqPiXWSgQ2bt8wXaga0GkOQ+0aE1NenZahVZrXrr6esQ+sNO1A/PlsZMuIa69uc9GeTPhAkjFwMQe3g29BuBYT9bpP1snk714ssGNWX3ZKdHJjmH24mAbEBMlmBWoKDw0eSDEnbsUdRoh27xgQ24NAc4fNVoFX1zztAcWc4XtK3wNoGAjLeVW8Azi21GzcJv/suddBuO7ALF+lttYYI5hhjgggbRgoPZpAE8HRV40A5UZTOrZWKeeSkuHgwPpoYnLR9uVgrzz7e1KZ3RO/2TCZ093jIRKRgh5jFUneKpuqDKaKLfYBs4ytZRH6H7Q8r5k0pec17FjWNfglg90WdeC+tGd3d3Qge7ZczjsZY33eQWA6oUmUHuL6n021AxoCJFZ4KjKVFkzNMAQ2vM9flblE3LJB4E4p/G5PzqowVeMEMFQ1hBdI+PJ3OCKQ/BaQq9MQBs3GQxwwcPj12nJluq88NloRGA5MMKgwnLaEhLCivXl5UeM0NjiLb03Db1A+1tmcvZnMrTDm3bPvf6OYx0vi+6CZVZCybwdW6iaauAyWTgFlJp5r9CVCaPK2Hx7QZM405Jb6BCwC83B7jQLuPDGd6esyalNKHYgTq44HMm8KsJGC5WdttC5Qc2b+v88EVIvmvSbQsWNiNpQzWkELWaYfd32FvYSTK/9JOTS0YKaMPUnhYJEdfkqQ4br9ebbkqUW9uI6WXGSEwwnoYqf2fa2i4="
    # decrypt(e)

    # schedule.every().day.at("10:00").do(job)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    job()


