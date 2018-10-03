#coding:utf-8
import happybase
con = happybase.Connection('localhost')
table = con.table('test_user_relation')
'''
for i in range(101):
    table.put('1',{'w:':str(i)})
'''
#table.put('1',{'w:1':'1111'})
#table.put('1',{'w:2':'2222'})
#table.put('1',{'w:2':'3333'})
#table.put('1',{'w:':'2'})
values=table.cells('1','w:2',versions=101,include_timestamp=True)
values=table.cells('1','w:1',versions=101,include_timestamp=True)
print values
