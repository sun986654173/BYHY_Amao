from hytest import *
from lib.classAPI import yjyxAPI

# 定义一个模块级变量
suite_classid = None

def suite_setup():
    global suite_classid  # 声明使用模块级变量

    INFO('开始执行目录初始化：系统中已有班级（七年级1班）')

    r_suitesetup = yjyxAPI.addClass('1', '七年级1班', '80').json()
    suite_classid = r_suitesetup['id']

    return suite_classid

def suite_teardown():
    global suite_classid  # 声明使用模块级变量

    INFO('开始执行目录清除：删除套件初始化中新建的班级')

    yjyxAPI.deleteClass(suite_classid).json()




