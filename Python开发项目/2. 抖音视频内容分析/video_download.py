import requests
import re

# 抖音请求标头
douyin_headers = {
'accept':'application/json, text/plain, */*',
'accept-encoding':'gzip, deflate, br, zstd',
'accept-language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
'cache-control':'no-cache',
'cookie':'',
'pragma':'no-cache',
'priority':'u=1, i',
'referer':'https://www.douyin.com/video/7420017646491520290',
'sec-ch-ua':'"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
'sec-ch-ua-mobile':'?0',
'sec-ch-ua-platform':"Windows",
'sec-fetch-dest':'empty',
'sec-fetch-mode':'cors',
'sec-fetch-site':'same-origin',
'uifid':'a6000b6bd0597977c28c1dbb751d8a8c80ef4c078dbea6da280536e6f6924b82d0e0143103ae6bb0d7f4ab0e876243663f6a43c11589e166d1672b78c2b6b24cf96224efff8976ecd6a90a4c11c804f0ec4a4cd2d4ee070b35aebe661d279d999bd71b9fc15f8218febcbce80a86f0758c6618410f0ab83a13d602237401f3a85efaf0204ae5b504bc244dc1640c73176013b45131fcc2fb88687b0fe366dcef',
'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0'
}
# 小红书请求标头
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


# 下载抖音视频，返回视频存储路径
def douyin_video(mid):
    url = f'https://www.douyin.com/jingxuan?modal_id={mid}'
    res = requests.get(url, headers=douyin_headers)
    # print(res.text)

    matches = re.findall(r'\[\{\\"src\\":\\"(.*?)\\"}', res.text)  # 正则匹配视频链接，返回所有匹配值的list
    print(matches[0])

    res = requests.get(matches[0],headers=douyin_headers)
    with open(f'./视频下载/{mid}.mp4', 'wb') as f:  # 视频存储
        f.write(res.content)

    return f'./视频下载/{mid}.mp4'


# 下载小红书视频，返回视频存储路径
def xhs_video(url):
    res = requests.get(url, headers=xhs_headers)
    # print(res.text)

    video_url = re.search(r'<meta name="og:video" content="(.*?)">', res.text)  # 正则匹配视频链接，返回首个匹配值
    title = re.search(r'<meta name="og:title" content="(.*?)">', res.text)

    res = requests.get(video_url.group(1))
    print(res.content)
    with open(f'./视频下载/{title.group(1)}.mp4', 'wb') as f:
        f.write(res.content)

    return f'./视频下载/{title.group(1)}.mp4'


if __name__ == '__main__':
    mid = '7552144381940796735'
    douyin_video(mid)
    # url = 'https://www.xiaohongshu.com/explore/68ea32790000000004017e03?xsec_token=AB67sFBzuHF9r-jCpdeQXrKJEHBAXFD9WjMaKw1nUv8J0=&xsec_source=pc_feed&source=404'
    # xhs_video(url)

