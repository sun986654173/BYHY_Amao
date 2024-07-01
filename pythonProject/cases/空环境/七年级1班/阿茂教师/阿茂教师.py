from hytest import *
from lib.classAPI import yjyxAPI
import json


class tc001002:
    name = '老师API_添加老师2 - tc001002'

    def setup(self):
        INFO('执行初始化操作：新增一个班级，再通过json.dump方法获取含classID的json字符串')
        r0 = yjyxAPI.addClass(1,'七年级2班',80).json()
        self.classID = r0['id']

        str_json = [{"id": self.classID}]
        self.classlist = json.dumps(str_json)


    def teardown(self):
        INFO('执行清除操作：删除用例中新建的教师')
        yjyxAPI.deleteTeacher(self.teacherID)

        INFO('执行清除操作：删除初始化中新建的班级')
        yjyxAPI.deleteClass(self.classID)


    def teststeps(self):
        STEP(1, '调用创建老师API，创建1个系统中不存在同登录名的老师')

        r1 = yjyxAPI.addTeacher('阿茂老师001002','阿茂老师001002',1,self.classlist,'1234567891','amao001002@qq.com','411412555236633653').json()
        self.teacherID = r1['id']
        r_retcode = r1['retcode']

        CHECK_POINT('检查是否返回创建成功',r_retcode == 0)

        STEP(2,'调用列出老师API,获取所有老师的ID并保存至空列表中')

        r2 = yjyxAPI.getTearcher().json()
        req = []
        retlist = r2['retlist']
        for i in retlist:
            req.append(i)

        exceptlist = [{
            'username': '阿茂老师001002',
            'teachclasslist': [self.classID],
            'realname': '阿茂老师001002',
            'id': self.teacherID,
            'phonenumber': '1234567891',
            'email': 'amao001002@qq.com',
            'idcardnumber': '411412555236633653'
        }]

        INFO(f'预期的结果是：{exceptlist}')
        INFO(f'实际的结果是：{req}')

        CHECK_POINT('检查STEP1中新建的老师信息是否存在',exceptlist[0] in req)


class tc001003:
    name = '老师API_添加老师3 - tc001003'

    def __init__(self):
        self.newclassid = None
        self.classlist = None

    def setup(self):
        INFO('开始执行用例初始化操作：新建1个班级')
        r = yjyxAPI.addClass(1,'七年级2班',80).json()
        self.newclassid = r['id']
        str_json = [{"id": self.newclassid}]
        self.classlist = json.dumps(str_json)

    def teardown(self):
        INFO('开始执行用例清除操作：删除初始化操作中新建的班级')
        yjyxAPI.deleteClass(self.newclassid).json()

    def teststeps(self):
        STEP(1,'调用列出老师API，获取已有老师的ID及其用户名，用于后续检查点验证')

        r_step1 = yjyxAPI.getTearcher().json()
        retlist_step1 = r_step1['retlist']
        oldtid = []
        username_step1 = None
        for i  in retlist_step1:
            oldtid.append(i['id'])
        for n in retlist_step1:
            username_step1 = n['username']

        STEP(2,'调用创建老师API，创建一个存在同登录名的老师')

        r_step2 = yjyxAPI.addTeacher(username_step1,'阿茂老师3',1,self.classlist,'12345678911','amao3@qq.com','411412555236633653').json()
        exceptr = {
            "retcode": 1,
            "reason": f"登录名 {username_step1} 已经存在"
        }

        INFO(f'预期返回的结果：{exceptr}')
        INFO(f'实际返回的结果：{r_step2}')
        CHECK_POINT('检查返回结果是否符合预期',r_step2 == exceptr)

        STEP(3,'调用列出老师API')

        r_step3 = yjyxAPI.getTearcher().json()

        INFO(f'预期返回的结果：{r_step1}')
        INFO(f'实际返回的结果：{r_step3}')
        CHECK_POINT('检查返回结果是否符合预期',r_step3 == r_step1)


class tc001051:
    name = '老师API_修改老师1 - tc001051'

    def teststeps(self):
        STEP(1,'调用修改老师API，是url中的ID为一个不存在的老师ID')

        r_step1 = yjyxAPI.editTeacher(123321).json()
        r_except = {
            "retcode": 1,
            "reason": "id 为`123321`的老师不存在"
            }

        STEP(2,'检查返回结果是否符合预期')

        INFO(f'预期返回的结果：{r_except}')
        INFO(f'实际返回的结果：{r_step1}')
        CHECK_POINT('检查返回结果是否符合预期',r_step1 == r_except)


class tc001052:
    name = '老师API_修改老师2 - tc001052'

    def __init__(self):
        self.classid1_setup = None
        self.classid2_setup = None
        self.classlist = None
        self.teacherid_setup = None
        self.forcheckcid = None


    def setup(self):
        INFO('开始执行用例初始化操作：新增2个班级，用于用例中的修改操作')
        r_setup2 = yjyxAPI.addClass(1,'七年级1052班',80).json()
        r_setup3 = yjyxAPI.addClass(1,'七年级1053班',80).json()

        self.classid1_setup = r_setup2['id']
        self.classid2_setup = r_setup3['id']
        self.forcheckcid = [self.classid1_setup,self.classid2_setup] # 用于检查点检查classlist

        str_json1 = [{"id": self.classid1_setup}]
        str_json2 = [{"id": self.classid2_setup}]
        self.classlist = json.dumps(str_json1 + str_json2)

        INFO('开始执行用例初始化操作：新增1个教师，用于用例中的修改操作')
        r_setup3 = yjyxAPI.addTeacher('阿茂老师1052','阿茂老师1052',1,self.classlist,'987654321','amao1052@qq.com','3209251983090987899').json()
        self.teacherid_setup = r_setup3['id']


    def teardown(self):
        INFO('开始执行用例清除操作：删除初始化操作中新增的教师和班级')
        yjyxAPI.deleteTeacher(self.teacherid_setup)
        yjyxAPI.deleteClass(self.classid1_setup)
        yjyxAPI.deleteClass(self.classid2_setup)


    def teststeps(self):
        STEP(1,'调用修改老师API，同时修改真实名和授课班级，班级从1个班修改为2个班')
        r_step1 = yjyxAPI.editTeacher(teacherid=self.teacherid_setup,realname='阿茂老师001052',classlist=self.classlist,subjectid=1).json()
        r_except = {
            "retcode": 0
        }

        INFO(f'预期返回的结果：{r_except}')
        INFO(f'实际返回的结果：{r_step1}')
        CHECK_POINT('检查返回结果是否符合预期', r_step1 == r_except)


        STEP(2,'调用列出老师API')
        realname = []
        teachclasslist = []
        r_step2 = yjyxAPI.getTearcher().json()
        retlist_step2 = r_step2['retlist']
        for i in retlist_step2:
            realname.append(i['realname'])
            teachclasslist.append(i['teachclasslist'])

        realname_except = '阿茂老师001052'
        teachclasslist_except = self.forcheckcid

        INFO(f'realname预期包含的结果：{realname_except}')
        INFO(f'realname实际的结果：{realname}')
        CHECK_POINT('检查返回结果中的realname字段',realname_except in realname)

        INFO(f'teachclasslist预期包含的结果：{teachclasslist_except}')
        INFO(f'teachclasslist实际的结果：{teachclasslist}')
        CHECK_POINT('检查返回结果中的teachclasslist字段', teachclasslist_except in teachclasslist)


class tc001081:
    name = '老师API_删除老师1 - tc001081'

    def teststeps(self):
        STEP(1,'调用删除老师API，删除一个不存在的老师ID')
        r_step1 = yjyxAPI.deleteTeacher(456123).json()

        STEP(2,'检查返回结果')
        r_except = {
            "retcode": 404,
            "reason": "id 为`456123`的老师不存在"
        }

        INFO(f'预期返回的结果：{r_except}')
        INFO(f'实际返回的结果：{r_step1}')
        CHECK_POINT('检查返回结果是否符合预期', r_step1 == r_except)


class tc001082:
    name = '老师API_删除老师2 - tc001082'

    def __init__(self):
        self.classid = None
        self.classlist = None
        self.teacherid = None

    def setup(self):
        INFO('开始执行用例初始化操作：新增1个班级')
        r_setup1 = yjyxAPI.addClass(1,'七年级1082班',80).json()
        self.classid = r_setup1['id']

        str_js = [{"id": self.classid}]
        self.classlist = json.dumps(str_js) # 用于新建教师时对classlist字段传参

        INFO('开始执行用例初始化操作：新增1个教师')
        r_setup2 = yjyxAPI.addTeacher('阿茂老师1082','阿茂老师1082',1,self.classlist,'98765432111','amao1082@qq.com','6220123554515215').json()
        self.teacherid = r_setup2['id']

    def teardown(self):
        INFO('开始执行用例清除操作：删除初始化中新增的班级')
        yjyxAPI.deleteClass(self.classid)

    def teststeps(self):
        STEP(1,'调用删除老师API，删除一个存在的老师ID')
        r_step1 = yjyxAPI.deleteTeacher(self.teacherid).json()
        r_except = {
            "retcode": 0
        }

        INFO(f'预期的返回结果：{r_except}')
        INFO(f'实际的返回结果：{r_step1}')
        CHECK_POINT('检查返回结果：',r_step1 == r_except)

        STEP(2,'调用列出老师API')
        r_step2 = yjyxAPI.getTearcher().json()
        retlist_step2 = r_step2['retlist']

        teacherid_step2 = []
        for tid in retlist_step2:
            teacherid_step2.append(tid['id'])

        INFO(f'预期的返回结果不包含：{self.teacherid}')
        INFO(f'实际的返回结果：{teacherid_step2}')
        CHECK_POINT('检查返回结果', self.teacherid not in  teacherid_step2)


class tc002001:
    name = '学生API_添加学生1 - tc002001'

    def __init__(self):
        self.classid = None
        self.studentid = None

    def setup(self):
        INFO('开始执行初始化操作：调用列出班级API，获取classid')
        r_setup = yjyxAPI.getClass().json()
        retlist_r = r_setup['retlist']
        for cid in retlist_r:
            self.classid = cid['id']

    def teardown(self):
        INFO('开始执行清除操作：删除用例中新增的学生')
        yjyxAPI.deleteStudent(self.studentid)

    def teststeps(self):
        STEP(1,'调用学生API，创建1个不存在同登录名的学生')
        r_step1 = yjyxAPI.addStudent('阿茂学生2001', '阿茂学生2001', 1,self.classid,'123456789').json()
        self.studentid = r_step1['id']

        r_except = {
            "retcode": 0,
            "id": self.studentid
        }
        
        INFO(f'预期返回的结果：{r_except}')
        INFO(f'实际返回的结果：{r_step1}')
        CHECK_POINT('检查返回结果是否符合预期',r_except == r_step1)

        STEP(2,'调用列出学生API')
        r_step2 = yjyxAPI.getStudent().json()
        retlist_step2 = r_step2['retlist']

        retlist_except = [{
            "classid": self.classid,
            "realname": '阿茂学生2001',
            "username": '阿茂学生2001',
            "phonenumber": '123456789',
            "id": self.studentid
        }]

        INFO(f'预期返回的结果：{retlist_except}')
        INFO(f'实际返回的结果：{retlist_step2}')
        CHECK_POINT('检查返回结果是否符合预期', retlist_except == retlist_step2)
