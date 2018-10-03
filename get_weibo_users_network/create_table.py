#coding:utf-8
import happybase
con=happybase.Connection('beihang2')
def create_table(table_name):
    con=happybase.Connection('beihang2')
    families={
        'u': {'max_versions':5,'in_memory':False}
    }   
    con.create_table(table_name,families)

def main():
    '''
    for month in range(1,7):
        table_name='search_idtweets2014%s' % str(month).zfill(2)
        create_table(table_name)
        table_name='search_keytweets2014%s' % str(month).zfill(2)
        create_table(table_name)
    '''
    create_table('users201411')
#    create_table('userstamp_tweets2014')
if __name__=='__main__':
    main()
