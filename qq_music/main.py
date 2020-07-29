import re
import json
import requests
from urllib.request import urlretrieve
import tkinter.messagebox
import tkinter as tk
import jsonpath

def download(path,mid,title,singer):
    # 解析网站
    link = 'http://www.douqq.com/qqmusic/qqapi.php'
    # 请求头
    headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '65',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.douqq.com',
            'Origin': 'http://www.douqq.com',
            'Referer': 'http://www.douqq.com/qqmusic/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
    data = {'mid': 'https://y.qq.com/n/yqq/song/{}.html'.format(mid)}
    req = requests.post(link, data=data, headers=headers).text
    req = json.loads(req)
    req = req.replace('\/', '/')
    res = re.compile('"m4a":"(.*?)",')
    res = re.findall(res, req)
    music = res[0]
    title = title.replace('\\', '').replace('/', '').replace(':', '').replace('：', '') \
                    .replace('*', '').replace('?', '').replace('？', '').replace('“', '') \
                    .replace('"', '').replace('<', '').replace('>', '').replace('|', '_').replace('【', '').replace('】', '') \
                    .replace(' ', '')
    # 歌曲保存
    urlretrieve(music, r'{}\{}__{}.mp3'.format(path, title, singer))
    tk.messagebox.showinfo(title='QQ音乐下载器', message='下载完成')

if __name__ == "__main__":
    name = input("输入要下载的歌名：")
    path = input("输入歌曲的保存路径：")
    kw = name
    # 分析网页数据
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=60454714197220159&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=10&w={}&g_tk_new_20200303=811282280&g_tk=811282280&loginUin=1103637169&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0'.format(
        kw)
    response = requests.get(url)
    # 获取json数据
    html = response.json()
    # 创建列表
    mids = []
    titles = []
    singers = []
    for n in range(0, 10):
        # 获取歌曲id
        mid = jsonpath.jsonpath(html, "$..list[{}]".format(n))[0]['mid']
        # 获取歌名
        title = jsonpath.jsonpath(html, "$..list[{}]".format(n))[0]['title']
        # 获取歌手
        singer = jsonpath.jsonpath(html, "$..list[{}]".format(n))[0]['singer'][0]['name']
        # 添加至列表
        mids.append(mid)
        titles.append(title)
        singers.append(singer)

    print(
        """
——————————————————————————————————
        QQ音乐下载器
——————————————————————————————————
        """
    )
    for a in range(10):
        print(str(a) + '.....' + singers[a] + '——' + titles[a])
    comment = int(input("输入歌区前的序号下载对应歌曲："))
    download(path, mids[comment], titles[comment], singers[comment])
