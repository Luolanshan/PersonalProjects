# 巨量创意 投放视频 图表数据+视频文件
import pandas as pd
import requests
from pprint import pprint
import os
import re

# 请求标头 - 要加cookie
headers = {
    'accept':'application/json, text/plain, */*',
    'accept-encoding':'gzip, deflate, br, zstd',
    'accept-language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control':'no-cache',
    'caller':'cc',
    'cookie':'_tea_utm_cache_4031=undefined; passport_csrf_token=49fccbd31c770c1cb765d1db656b78d4; passport_csrf_token_default=49fccbd31c770c1cb765d1db656b78d4; ttwid=1%7CfxEQM03gYF453aioSTkh-wNmPiq58g0ddLqvidEk1tc%7C1760099069%7C6d9e6748921c8c39ea3781ba0d34ef9f00d33f041b7a5a089fe2889e0b023473; ttcid=96364305052745b085417e427b40ba4142; passport_mfa_token=CjfolJ01TM%2BMJOvhcrjReJlBZfOhRes1wSrYnj9C%2BZC1efv6BDtH9WAB%2FSiui25A3C%2BeqKkcJqsJGkoKPAAAAAAAAAAAAABPk%2Bcb0GsAxfTmPFqfHzpLchNbTf5ag6d%2F3NpcWBvR2vxUexz2I9LKe2f22rKdmjKnfRCTuv4NGPax0WwgAiIBA6lLFDo%3D; d_ticket=23de329884dbfb400148c5da532b2bac02b26; odin_tt=547b9fa5b83bf81ec9d16be5e3e7182eb54f716933a505ade318a83c75634b48701798c31cbb3049d56fb0d7b5742df40db78450d69671a96fbaab16d17e314f; n_mh=mFdR03_24x1Y0fTXKGYfIrxfLXcieDOIiPNikIrn2w8; passport_auth_status=4ab959b0edcb0f35a5966fd2b1e0fba3%2C; passport_auth_status_ss=4ab959b0edcb0f35a5966fd2b1e0fba3%2C; sid_guard=fbf3a5e78b57699c629e9d90ba8783d6%7C1760099085%7C5184000%7CTue%2C+09-Dec-2025+12%3A24%3A45+GMT; uid_tt=717c6b74bc7b7d0b2eb754125b485cb8; uid_tt_ss=717c6b74bc7b7d0b2eb754125b485cb8; sid_tt=fbf3a5e78b57699c629e9d90ba8783d6; sessionid=fbf3a5e78b57699c629e9d90ba8783d6; sessionid_ss=fbf3a5e78b57699c629e9d90ba8783d6; session_tlb_tag=sttt%7C12%7C-_Ol54tXaZxinp2QuoeD1v_________xYgi08BY9S_zsnMfejWF-IeKtPVifYG6sCO0xOkMVfwQ%3D; is_staff_user=false; sid_ucp_v1=1.0.0-KGJkMGVhOTM2ZDg2OTc1ZDcyYjVjMmQ5ZGMxYTZmYzY1NjIzZmQ4NDMKHwj7hpDZoM29AhCN9qPHBhiyDCAMMJ3mgrUGOAJA8QcaAmxmIiBmYmYzYTVlNzhiNTc2OTljNjI5ZTlkOTBiYTg3ODNkNg; ssid_ucp_v1=1.0.0-KGJkMGVhOTM2ZDg2OTc1ZDcyYjVjMmQ5ZGMxYTZmYzY1NjIzZmQ4NDMKHwj7hpDZoM29AhCN9qPHBhiyDCAMMJ3mgrUGOAJA8QcaAmxmIiBmYmYzYTVlNzhiNTc2OTljNjI5ZTlkOTBiYTg3ODNkNg; csrftoken=6FG1e40YBVqcFY2_ZUU0c9sM; gd_random=eyJtYXRjaCI6dHJ1ZSwicGVyY2VudCI6MC4yMDQ0ODY0MDczMzIyNzIwOH0=.RBokesXNmcu3BV5zjkSdLzsrKfKii1xddiu2eB3ekPs=; tt_scid=k6wsF2WRbpdQZFauabonAFAJ6VAR7Xsktrwdx5Mj.47.XJ4rKHCgVHrv2qm0.8Vh7365; msToken=UpIinELQ2iXIH6CvL2lUUD8_etdOl4XOjN1_CiWg7_HirsfvacaqFYHQy0bSdfK88A3C-mNMz8WNKYYBmN_p08RFnenjZPlFKuTuvQxD6WBnK7eigRxcdVbkfQ==',
    'pragma':'no-cache',
    'priority':'u=1, i',
    'referer':'https://cc.oceanengine.com/inspiration/creative-hot/ad/detail/7486476564335706122?appCode=999&period=7&listType=10&materialType=3',
    'sec-ch-ua':'"Microsoft Edge";v="141", "Not?A_Brand";v="8", "Chromium";v="141"',
    'sec-ch-ua-mobile':'?0',
    'sec-ch-ua-platform':"Windows",
    'sec-fetch-dest':'empty',
    'sec-fetch-mode':'cors',
    'sec-fetch-site':'same-origin',
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0',
    'x-csrftoken':'6FG1e40YBVqcFY2_ZUU0c9sM'
}

# 获取单个视频的图表数据
def get_data(mid):
    url = 'https://cc.oceanengine.com/creative_radar_api/v1/material/user_interact?'
    payload = {
        'material_id': mid,
        'app_code': '999',
        'past_days': '7',
        'list_type': '10',
        'msToken': '_B3tHmYkbyPgVqrlgtF64bRQhkZ6nD6hxygDPWz7FryvrWNCO-8hQXOuVSI1x2xgj0iqqvPr9rXm23LyT-CM8hbEKf4LgCTM_7BfykHf0VIn6HutaHI-DP4=',
        'X-Bogus': 'DFSzswVLhYTANazAtgQCG0kX95zi',
        '_signature': '_02B4Z6wo00001HFW6cAAAIDARnItnqr-XIRxVu1AAHurfGe99VsVYhR91VCEhmResf1SoSRz9SuXiRbuVGG.PhmzniArhquZ5SYvaHUiwdpFoDL4109xy3Dnj2eBjJR9UumN9TPfBIhDhPi679'
    }

    res = requests.get(url, params=payload, headers=headers)
    # pprint(res.json())
    return res.json()

# 清理文件名中的非法字符
def clean_filename(filename):
    """
    清理文件名中的非法字符，确保其可以安全用于保存文件。
    参数:
        filename: 原始文件名
    返回:
        str: 清理后的安全文件名
    """
    # 定义在Windows系统中文件名不能包含的非法字符
    illegal_chars = r'[<>:"/\\|?*]'  # 包括问号?和感叹号!
    # 使用正则表达式将所有非法字符替换为下划线或直接移除
    safe_name = re.sub(illegal_chars, '_', filename)
    # 你也可以选择直接移除，例如：re.sub(illegal_chars, '', filename)
    return safe_name

# 图表数据&视频文件 获取+存储
# 视频ID	视频标题	进度	点击	评论	关注	点赞	分享	流失
def parse_data(mid, raw_data):
    video_interact = pd.DataFrame(raw_data['data']['video_interact'])
    # 提取嵌套数据
    metrics_expanded = pd.json_normalize(video_interact['metrics'])
    # 筛选字段：只需要每个指标的.data数据
    metrics_data_only = metrics_expanded.filter(like='.data').copy()  # 在创建 metrics_data_only 时显式创建副本，明确其独立性
    # 修改字段名
    new_col = {
        'click_cnt.data': '点击指数',
        'dy_comment.data': '评论指数',
        'dy_follow.data': '关注指数',
        'dy_like.data': '点赞指数',
        'dy_share.data': '分享指数',
        'user_lose_cnt.data': '流失指数'
    }
    metrics_data_only.rename(columns=new_col, inplace=True)
    # 合并表格：duration字段和提取出的.data字段合并
    final_df = pd.concat([video_interact, metrics_data_only], axis=1)
    # 添加mid字段
    final_df['视频ID'] = mid
    final_df['视频ID'] = final_df['视频ID'].astype(str)  # mid转换为字符串格式，防止excel打开后科学计数法显示

    # 获取视频标题数据
    url = 'https://cc.oceanengine.com/creative_radar_api/v1/material/info?'
    payload = {
        'material_id': mid,
        'list_type': '10',
        'msToken': '_B3tHmYkbyPgVqrlgtF64bRQhkZ6nD6hxygDPWz7FryvrWNCO-8hQXOuVSI1x2xgj0iqqvPr9rXm23LyT-CM8hbEKf4LgCTM_7BfykHf0VIn6HutaHI-DP4=',
        'X-Bogus': 'DFSzswVLhYTANazAtgQCG0kX95zi',
        '_signature': '_02B4Z6wo00001HFW6cAAAIDARnItnqr-XIRxVu1AAHurfGe99VsVYhR91VCEhmResf1SoSRz9SuXiRbuVGG.PhmzniArhquZ5SYvaHUiwdpFoDL4109xy3Dnj2eBjJR9UumN9TPfBIhDhPi679'
    }
    res = requests.get(url, params=payload, headers=headers)
    title = res.json()['data']['title']
    final_df['视频标题'] = title

    # 分标题存储到Excel
    clean_title = clean_filename(title)  # 调用函数，清理标题中的非法字符
    final_df.to_excel(f'./投放数据/{clean_title}.xlsx', index=False)

    # 获取视频mp4文件
    vid = res.json()['data']['material_uri']  # material info中提取 vid，作为视频地址post请求参数
    url = 'https://cc.oceanengine.com/creative_radar_api/v1/video/info?'
    payload = {
        'msToken': '_B3tHmYkbyPgVqrlgtF64bRQhkZ6nD6hxygDPWz7FryvrWNCO-8hQXOuVSI1x2xgj0iqqvPr9rXm23LyT-CM8hbEKf4LgCTM_7BfykHf0VIn6HutaHI-DP4=',
        'X-Bogus': 'DFSzswVLhYTANazAtgQCG0kX95zi',
        '_signature': '_02B4Z6wo00001HFW6cAAAIDARnItnqr-XIRxVu1AAHurfGe99VsVYhR91VCEhmResf1SoSRz9SuXiRbuVGG.PhmzniArhquZ5SYvaHUiwdpFoDL4109xy3Dnj2eBjJR9UumN9TPfBIhDhPi679'
    }  # get请求参数
    data = {"video_infos": [{"vid": vid,
                             "mid": mid}], "water_mark": "creative_center", "queryParams": {}}  # post请求参数
    res = requests.post(url, headers=headers, params=payload, json=data)
    video_url = res.json()['data'][mid]['video_url']  # 获取视频地址

    res = requests.get(video_url)  # 获取视频文件
    with open(f'./投放数据/{clean_title}.mp4', 'wb') as f:  # 视频的二进制数据写入mp4文件
        f.write(res.content)

# 批量数据获取
def patch_data(number):
    url = f'https://cc.oceanengine.com/creative_radar_api/v1/material/list?list_type=10&material_type=3&order_by=total_play&video_duration_types=%5B5%5D&label_ids=%5B%5D&video_type=%5B%5D&landing_type=%5B999%5D&limit={number}&offset=0&period_type=1&aggr_app_code=999&aggr_category_list=%5B%5D&page=1&msToken=2kHIZjjS4hCDpv8Fu5ne5eyjJui8c_6RsgXomlD789ZX2MpU6vnValNzbXErwNdv77a-VrtZn-KtypcZNfynX-qlimDOj-vKkmdxTYkbPcTK_tpL4ZM6FQmYDiM=&X-Bogus=DFSzswVOie2AN9yZCxcv9ra9JzVT&_signature=_02B4Z6wo00001qaz5hgAAIDBKxtfkPDaJQams-KAAMFSfRRdv0x0wIUM.2uv-MRGzbupH2iCWTSwR2ujuFAMXEjmAQ-hTU-.t-XMnpKh2yow6ftrHvCLuKRd5WfUJqsb8lIRAnMF2d-vJiqd5b'

    res = requests.get(url, headers=headers)
    # print(res.url)
    # pprint(res.json())

    mid_list = res.json()['data']['materials']
    for mid in mid_list:
        material_id = mid['material_id']
        data = get_data(material_id)
        parse_data(material_id, data)  # 存储文件表名中不能带特殊字符

# 所有视频数据合并到一张表
def merge_data():
    excel_list = os.listdir('./投放数据') # 获取文件夹下的所有文件列表
    # pprint(excel_list)

    empty_df = pd.DataFrame()
    for excel in excel_list:
        if '.xlsx' in excel:
            temp_df = pd.read_excel('./投放数据/' + excel, converters={'视频ID': str})
            empty_df = pd.concat([empty_df, temp_df])

    empty_df.to_excel('./整合数据/总表.xlsx', index=False)


if __name__ == '__main__':

    patch_data(20)
    merge_data()



