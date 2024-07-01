from hytest import *
from lib.classAPI import yjyxAPI

def suite_setup():
    INFO('开始执行目录初始化：系统中没有教师')
    r_clearteacher = yjyxAPI.getTearcher().json()
    if r_clearteacher['retlist'] == []:
        print('系统中已无教师')
    else:
        r_teacherlist = r_clearteacher['retlist']
        for tid in r_teacherlist:
            yjyxAPI.deleteTeacher(tid['id'])

    INFO('开始执行目录初始化：系统中没有班级')
    r_clearclass = yjyxAPI.getClass().json()
    if r_clearclass['retlist'] == []:
        print('系统已无班级')
    else:
        oldrlist = r_clearclass['retlist']
        for i in oldrlist:
            yjyxAPI.deleteClass(i['id'])



def suite_teardown():
    INFO('开始执行目录清除：检查环境中是否存在教师，若有则删除')
    r1 = yjyxAPI.getTearcher().json()
    if r1['retlist'] == []:
        print('环境中已无教师')
    else:
        yjyxAPI.deleteAllTeacher()

    INFO('开始执行目录清除：检查环境中是否存在班级，若有则删除')
    r2 = yjyxAPI.getClass().json()
    if r2['retlist'] == []:
        print('环境中已无班级')
    else:
        yjyxAPI.deleteAllClass()