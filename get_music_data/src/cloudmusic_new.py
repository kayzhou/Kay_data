'''
基于 https://binaryify.github.io/NeteaseCloudMusicApi/#/?id=neteasecloudmusicapi 的python调用实现

爬取网易云音乐数据

需要先启动 /Users/Kay/Project/GitHub/NeteaseCloudMusicApi node app.js
'''

import requests
import time
url = 'http://localhost:3000/'
# url = 'http://192.168.1.151:3000/'

# 代理服务器
proxyHost = "proxy.abuyun.com"
proxyPort = "9020"

# 代理隧道验证信息
'''
proxyUser = "H120UV81U4DG842D"
proxyPass = "53C165A726F8A3F9"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host" : proxyHost,
    "port" : proxyPort,
    "user" : proxyUser,
    "pass" : proxyPass,
}

proxies = {
    "http"  : proxyMeta,
    "https" : proxyMeta,
}
'''

def get_user_playlist(uid):
    '''
    用户歌单
    '''
    for _ in range(3):
        try:
            r = requests.get(url + 'user/playlist?uid={}'.format(uid))
            print('url:' + r.url)
            code = r.status_code
        except:
            code = -1
        print('status:', code)
        if code == 200:
            break
        else:
            time.sleep(10)
    return r.json()


def get_user_fans(uid):
    '''
    用户粉丝
    '''
    for _ in range(3):
        try:
            r = requests.get(url + 'user/followeds?uid={}'.format(uid))
            print('url:' + r.url)
            code = r.status_code
        except:
            code = -1
        print('status:', code)
        if code == 200:
            break
        else:
            time.sleep(10)
    return r.json()


def get_user_follows(uid):
    '''
    用户关注
    '''
    for _ in range(3):
        try:
            r = requests.get(url + 'user/follows?uid={}'.format(uid))
            print('url:' + r.url)
            code = r.status_code
        except:
            code = -1
        print('status:', code)
        if code == 200:
            break
        else:
            time.sleep(10)
    return r.json()


def get_user_record(uid, opt):
    '''
    用户播放记录
    '''
    # r = requests.get(url + 'user/record?uid={}&type={}'.format(uid, opt), proxies=proxies)
    for _ in range(3):
        try:
            r = requests.get(url + 'user/record?uid={}&type={}'.format(uid, opt))
            print('调用：' + r.url)
            code = r.status_code
        except:
            code = -1
        print('状态：', code)
        if code == 200:
            break
        else:
            time.sleep(10)
    return r.json()


def get_playlist(pid):
    '''
    歌单详情
    '''
    for _ in range(3):
        try:
            r = requests.get(url + 'playlist/detail?id={}'.format(pid))
            print('调用：' + r.url)
            code = r.status_code
        except:
            code = -1
        print('状态：', code)
        if code == 200:
            break
        else:
            time.sleep(10)
    return r.json()


def get_mp3_url(sid):
    '''
    获取mp3链接
    '''
    r = requests.get(url + 'music/url?id={}'.format(sid))
    print('调用：' + r.url)
    return r.json()


def get_comment(sid):
    '''
    说明:调用此接口,传入音乐 id和 limit 参数, 可获得该音乐的所有评论(不需要登录)

    必选参数:
    sid: 音乐 id

    可选参数:
    limit: 取出评论数量,默认为20

    offset: 偏移数量,用于分页,如:(评论页数-1)*20, 其中 20 为 limit 的值

    接口地址:
    /comment/music

    调用例子:
    /comment/music?id=186016&limit=1 对应晴天评论
    '''
    r = requests.get(url + 'comment/music?id={}'.format(sid))
    print('相应代码：' + r.status_code)
    print('调用：' + r.url)
    return r.json()


def get_songs_from_artist(aid):
    '''
    说明:调用此接口,传入歌手 id,可获得歌手单曲

    必选参数:
    id: 歌手 id,可由搜索接口获得

    接口地址:
    /artists

    调用例子:
    /artists?id=6452
    '''
    r = requests.get(url + 'artists?id={}'.format(aid))
    print('相应代码：' + r.status_code)
    print('调用：' + r.url)
    return r.json()


def main():
    # print(get_user_playlist('61884303'))
    # print(get_user_fans('61884303'))
    # print(get_user_follows('61884303'))
    print(get_user_record('61884303', 0))


if __name__ == '__main__':
    main()

