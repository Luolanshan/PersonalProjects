import requests
import re, os

# xhs请求标头
xhs_headers = {
'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'accept-encoding':'gzip, deflate, br, zstd',
'accept-language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
'cache-control':'no-cache',
'cookie':"",
'pragma':'no-cache',
'priority':'u=0, i',
'referer':'https://www.xiaohongshu.com/web-login/captcha?redirectPath=https%3A%2F%2Fwww.xiaohongshu.com%2Fexplore%2F67f774ac000000001d000218%3Fxsec_token%3DABSyE42tZWthMC7UWgI2L6T7ssBZp9pFO3Lf2uu85x1VU%3D%26xsec_source%3Dpc_feed&callFrom=web&biz=sns_web&verifyUuid=87aae138-1534-4a3a-8b44-fcd016502ea5&verifyType=102&verifyBiz=461',
'sec-ch-ua':'"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
'sec-ch-ua-mobile':'?0',
'sec-ch-ua-platform':"Windows",
'sec-fetch-dest':'document',
'sec-fetch-mode':'navigate',
'sec-fetch-site':'same-origin',
'sec-fetch-user':'?1',
'upgrade-insecure-requests':'1',
'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0'
}

# 清理文件名中的非法字符
def clean_filename(filename: str) -> str:
    """
    清理文件名中的非法字符，替换为下划线
    """
    # 替换Windows非法字符为下划线
    illegal_chars = r'[\\/:"*?<>|]'
    clean_name = re.sub(illegal_chars, '_', filename)

    # 可选：移除首尾空格和多余空格
    clean_name = clean_name.strip().replace('  ', ' ')

    return clean_name


# xhs图片下载，返回图片路径列表 + 小红书图片存储路径（占位函数）
def xhs_img(url):
    res = requests.get(url, headers=xhs_headers)
    # print(res.text)
    img_url = re.findall(r'<meta name="og:image" content="(.*?)">', res.text)
    title = re.search(r'<meta name="og:title" content="(.*?)">', res.text)

    i = 1
    img_path_list = []
    for img in img_url:
        res = requests.get(img)
        clean_name = clean_filename(title.group(1))

        path = f'./图片下载/{clean_name}'
        os.makedirs(path, exist_ok=True)  # 创建目录（如果不存在）

        with open(f'{path}/{clean_name}_{i}.png', 'wb') as f:
            f.write(res.content)

        img_path_list.append(f'{path}/{clean_name}_{i}.png')
        i += 1

    return img_path_list


if __name__ == '__main__':
    url = 'https://www.xiaohongshu.com/explore/68dbe54c0000000007030fa5?xsec_token=AB1ogeFlRkvNjnIscQAi_sIB2kYnCaIRVqvuxh7rDc_sY=&xsec_source=pc_feed'
    xhs_img(url)

