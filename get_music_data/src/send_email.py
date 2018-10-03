#coding:utf-8
import os


def local_send(mailto, title, text):
    for m in mailto:
        command = "echo '%s' | mail -s '%s' %s" % (text, title, m)
        print(command)
        os.system(command)
    return True


def alert(info):
    command = "echo '%s' | mail -s '程序异常提醒' 304003319@qq.com" % (info)
    print(command)
    os.system(command)


if __name__ == '__main__':

    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    mailto_list=["304003319@qq.com"]

    # if send(mailto_list, "服务器全面宕机！", text, html):
    #    print "发送成功"
    # else:
    #    print "发送失败"

    if not local_send(mailto_list, "服务器全面宕机！", text):
        print("发送成功")
    else:
        print("发送失败")
