from hytest import *
from lib.classAPI import yjyxAPI
import json


# 定义一个模块级变量
classid = None
studentid = None

def suite_setup():
    global classid,studentid      # 声明使用模块级变量classid

    INFO('开始执行目录初始化操作：列出已有的班级，获取classid')
    r1 = yjyxAPI.getClass().json()
    retlist_r1 = r1['retlist']
    for cid in retlist_r1:
        classid = cid['id']

    INFO('开始执行目录初始化操作：新增1个学生，获取studentid')
    r2 = yjyxAPI.addStudent('阿茂学生','阿茂学生',1,classid,'13451813456').json()
    studentid = r2['id']


def suite_teardown():
    global classid, studentid  # 声明使用模块级变量classid,studentid

    INFO('开始执行目录清除操作：删除初始化中新增的学生')
    yjyxAPI.deleteStudent(studentid)