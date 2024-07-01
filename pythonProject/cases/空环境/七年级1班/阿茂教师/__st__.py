from hytest import *
from lib.classAPI import yjyxAPI
import json

# 定义一个模块级变量
teacherid = None
classID = None

def suite_setup():
    global teacherid,classID # 声明使用模块级变量
    INFO('开始执行目录初始化：系统中已经有老师')

    r = yjyxAPI.getClass().json()

    retlist = r['retlist']
    for i in retlist:
        classID = i['id']
    if classID is None:
        INFO('No classID found in response')
    ssetup_list = [{"id": classID}]
    classlist = json.dumps(ssetup_list)

    response = yjyxAPI.addTeacher('阿茂老师','阿茂老师',1,classlist,'123456789','amao@qq.com','411412555236633652').json()
    teacherid = response['id']

    return teacherid


def suite_teardown():
    global teacherid  # 声明使用模块级变量
    INFO('开始执行目录清除：删除初始化操作中新建的老师')

    if teacherid is not None:
        yjyxAPI.deleteTeacher(teacherid)
    else:
        INFO('No teacherid found. Please run suite_setup() first.')


