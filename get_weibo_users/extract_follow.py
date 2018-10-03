#coding:utf-8
#抽取关注关系网络
import happybase


def follow():
    f = open('uid.txt')
    uid_list = []
    for line in f:
        uid_list.append(line.strip())
    f.close()
    uid_set = set(uid_list)
    table = happybase.Connection('beihang7').table('users201411')
    out_file = open('10w_follow', 'w')
    step = 100
    for i in range(0, len(uid_list), step):
        slice_uid_list = uid_list[i:i + step]
        for uid, data in table.rows(slice_uid_list):
            for key in data:
                follow_uid = key.split(':')[1]
                if follow_uid.isdigit() and follow_uid in uid_set:
                    out_file.write('%s\t%s\n' % (uid, follow_uid))
    out_file.close()


def validate():
    f = open('uid.txt')
    uid_list = []
    for line in f:
        uid_list.append(line.strip())
    f.close()
    uid_set = set(uid_list)
    table = happybase.Connection('beihang7').table('users201411')
    for uid, data in table.rows(uid_list[:10]):
        follow_cnt = 0
        cnt = 0
        for key in data:
            follow_uid = key.split(':')[1]
            if follow_uid.isdigit() and follow_uid in uid_set:
                cnt += 1
            follow_cnt += 1
        print follow_cnt, '\t', cnt, '\t', follow_cnt - cnt


if __name__=='__main__':
    follow()
