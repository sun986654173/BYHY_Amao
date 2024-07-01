from hytest import *
from lib.classAPI import yjyxAPI
import json


class tc002002:
    name = '学生API_添加学生2 - tc002002'

    def __init__(self):
        self.classid = None
        self.studentid = None

    def teardown(self):
        INFO('开始执行用例清除操作：删除用例中新建的学生')
        yjyxAPI.deleteStudent(self.studentid)

    def teststeps(self):
        STEP(1,'调用列出班级API，获取classid')
        r_step1 = yjyxAPI.getClass().json()
        retlist_step1 = r_step1['retlist']
        for cid in retlist_step1:
            self.classid = cid['id']

        STEP(2,'调用创建学生API')
        r_step2 = yjyxAPI.addStudent('阿茂学生2002','阿茂学生2002',1,self.classid,'1234562002').json()
        self.studentid = r_step2['id']

        r_except = {
            "retcode": 0,
            "id": self.studentid
        }

        INFO(f'预期的返回结果：{r_except}')
        INFO(f'实际的返回结果：{r_step2}')
        CHECK_POINT('检查返回结果是否符合预期',r_except == r_step2)

        STEP(3,'调用列出学生API')
        r_step3 = yjyxAPI.getStudent().json()
        retlist_step3 = r_step3['retlist']

        retlist_except = {
            "classid": self.classid,
            "realname": '阿茂学生2002',
            "username": '阿茂学生2002',
            "phonenumber": '1234562002',
            "id": self.studentid
        }

        INFO(f'预期的返回结果需包含：{retlist_except}')
        INFO(f'实际的返回结果：{retlist_step3}')
        CHECK_POINT('检查返回结果是否符合预期', retlist_except in retlist_step3)


class tc002081:
    name = '学生API_删除学生1 - tc002081'

    def __init__(self):
        self.classid = None
        self.studentid = None

    def setup(self):
        INFO('开始执行初始化操作：新增一个学生用于删除')
        rget_setup = yjyxAPI.getClass().json()
        rlistget_setup = rget_setup['retlist']
        for cid in rlistget_setup:
            self.classid = cid['id']

        radd_setup = yjyxAPI.addStudent('tc002081','tc002081',1,self.classid,'111222333').json()
        self.studentid = radd_setup['id']

    def teststeps(self):
        STEP(1,'调用删除学生API')
        r1 = yjyxAPI.deleteStudent(self.studentid).json()
        exceptr1 = {
            "retcode": 0
        }

        INFO(f'预期返回的结果：{exceptr1}')
        INFO(f'实际返回的结果：{r1}')
        CHECK_POINT('检查返回结果是否符合预期',exceptr1 == r1)

        STEP(2,'调用列出学生API')
        stuidlist = []
        r2 = yjyxAPI.getStudent().json()
        retlist_r2 = r2['retlist']
        for sid in retlist_r2:
            stuidlist.append(sid['id'])

        INFO(f'预期返回结果中不应含有：{self.studentid}')
        INFO(f'实际返回结果：{stuidlist}')
        CHECK_POINT('检查返回结果，不应包含已删除的学生',self.studentid not in stuidlist)