from hytest import *
from lib.classAPI import yjyxAPI
from lib.WebUI import *
from time import sleep
import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains


class tc000002:
    name = '班级API_添加班级2 - tc000002'

    def teardown(self):
        INFO('开始执行用例清除操作：删除用例中创建的班级')
        yjyxAPI.deleteClass(self.newID)

    def teststeps(self):
        STEP(1,'调用创建班级API，创建一个系统中不存在同年级的同名班级')
        r1 = yjyxAPI.addClass('2','七年级1班','80')
        retlist1 = r1.json()
        self.newID = retlist1['id']
        newIncode = retlist1['invitecode']
        newRetcode = retlist1['retcode']

        CHECK_POINT('检查创建API返回信息',newRetcode == 0)


        STEP(2,'调用列出班级API')
        r2 = yjyxAPI.getClass()
        retlist2 = r2.json()['retlist']
        exceplist = {
            "name": "七年级1班",
            "grade__name": "八年级",
            "invitecode": newIncode,
            "studentlimit": 80,
            "studentnumber": 0,
            "id": self.newID,
            "teacherlist": []
        }

        CHECK_POINT('检查返回结果是否包含STEP1中创建的信息',exceplist in retlist2)


class tc000003:
    name = '班级API_添加班级3 - tc000003'

    def setup(self):
        INFO('执行用例级初始化操作：调用列出班级API，获取已有班级信息')

        r_setup = yjyxAPI.getClass().json()
        self.retlist_setup = r_setup['retlist']
        INFO(self.retlist_setup)

    def teststeps(self):

        STEP(1,'调用创建班级API，创建一个已存在同年级的同名班级')

        r1 = yjyxAPI.addClass('1','七年级1班','80')
        retlist1 = r1.json()
        exceptlist1 = {
            "retcode": 1,
            "reason": "duplicated class name"
        }
        INFO(f'实际返回的结果：{retlist1}')
        INFO(f'预期返回的结果：{exceptlist1}')

        CHECK_POINT('检查返回结果是否为失败，消息体内容是否符合预期', retlist1 == exceptlist1)


        STEP(3,'调用列出班级API')

        r2 = yjyxAPI.getClass()
        retlist2 = r2.json()['retlist']

        CHECK_POINT('检查返回结果是否有STEP1中的班级信息,若有且仅有初始化中的信息则通过', self.retlist_setup == retlist2)


class tc000051:
    name = '班级API_修改班级1 - tc000051'

    def teardown(self):
        INFO('执行用例级清除操作：将数据环境还原(七年级2班改回1班)')
        r_teardown = yjyxAPI.editClass(self.r_classid,'七年级1班',80).json()
        INFO(r_teardown)


    def teststeps(self):
        STEP(1,'调用列出班级API，获取classid')

        r = yjyxAPI.getClass()
        retlist0 = r.json()['retlist']
        for i in retlist0:
            self.r_classid = i['id']

        STEP(2,'调用修改班级API，使班级名为新名字且无同名')

        r1 = yjyxAPI.editClass(self.r_classid,'七年级2班',80)
        retcode1 = r1.json()['retcode']

        CHECK_POINT('检查返回结果是否为0', retcode1 == 0)

        STEP(3,'调用列出班级API')

        r2 = yjyxAPI.getClass()
        retlist2 = r2.json()['retlist']
        for n in retlist2:
            newname = n['name']

        CHECK_POINT('检查返回结果中班级名是否修改',newname == '七年级2班')


class tc000052:
    name = '班级API_修改班级2 - tc000052'

    def setup(self):
        INFO('执行用例初始化操作1：调用列出班级API，获取修改前班级信息')
        r_setup1 = yjyxAPI.getClass().json()
        self.oldretlist = r_setup1['retlist']

        INFO('执行用例级初始化操作2：新增一个班级，用于修改')
        r_setup2 = yjyxAPI.addClass(1,'七年级2班',80).json()
        if 'id' in r_setup2:
            self.classID = r_setup2['id']
        else:
            raise KeyError("'id' not found")

    def teardown(self):
        INFO('执行用例级清除操作：删除初始化操作中新增的班级')
        yjyxAPI.deleteClass(self.classID)

    def teststeps(self):
        STEP(1,'调用修改班级API，使班级名为一个新名字且和已有的班级同名')
        r_STEP1 = yjyxAPI.editClass(self.classID,'七年级1班',80).json()
        exceptr = {
            "retcode": 1,
            "reason": "duplicated class name"
        }

        STEP(2,'检查返回结果是否符合预期')
        INFO(f'预期返回的结果：{exceptr}')
        INFO(f'实际返回的结果：{r_STEP1}')
        CHECK_POINT('检查返回结果', r_STEP1 == exceptr)

        STEP(3,'调用列出班级API')
        r_STEP3 = yjyxAPI.getClass().json()
        retlist_STEP3 = r_STEP3['retlist']

        STEP(4,'检查返回结果是否未发生改变')
        INFO(f'预期返回的结果：{self.oldretlist}')
        INFO(f'实际返回的结果：{retlist_STEP3}')
        CHECK_POINT('检查返回结果',self.oldretlist == retlist_STEP3)


class tc000053:
    name = '修改班级API_修改班级3 - tc000053'

    def teststeps(self):
        STEP(1,'调用修改班级API，classID为不存在的班级ID')

        r = yjyxAPI.editClass('123456789','修改班级为不存在的ID号',80).json()
        exceptresponse = {
            "retcode": 404,
            "reason": "id 为`123456789`的班级不存在"
        }
        INFO(f'实际返回结果：{r}')
        INFO(f'预期返回结果：{exceptresponse}')

        CHECK_POINT('检查返回结果是否符合预期',r == exceptresponse)


class tc000081:
    name = '班级API_删除班级1 - tc000081'

    def teststeps(self):
        STEP(1,'调用删除班级API，使用一个不存在的classID')

        r = yjyxAPI.deleteClass(114514).json()
        exceptr = {
            "retcode": 404,
            "reason": "id 为`114514`的班级不存在"
        }
        INFO(f'实际返回结果：{r}')
        INFO(f'预期返回结果：{exceptr}')

        CHECK_POINT('检查返回消息是否符合预期',r == exceptr)


class tc000082:
    name = '班级API_删除班级2 - tc000082'

    def __init__(self):
        self.classid_setup = None

    def setup(self):
        INFO('开始执行用例初始化操作：新增一个班级用于用例的删除')

        r_setup = yjyxAPI.addClass(1,'tc000082',80).json()
        self.classid_setup = r_setup['id']

    def teststeps(self):
        STEP(1,'调用删除班级API，使用已存在的classID')

        r1 = yjyxAPI.deleteClass(self.classid_setup).json()
        exceptr1 = {
            "retcode": 0
        }

        INFO(f'预期返回的结果：{exceptr1}')
        INFO(f'实际返回的结果：{r1}')
        CHECK_POINT('检查返回结果是否符合预期',r1 == exceptr1)

        STEP(2,'调用列出班级API')

        IDlist = []
        r2 = yjyxAPI.getClass().json()
        retlist2 = r2['retlist']
        for i in retlist2:
            IDlist.append(i['id'])

        INFO(f'预期返回的结果：{IDlist}中不包含{self.classid_setup}')
        INFO(f'实际返回的结果：{IDlist}')
        CHECK_POINT('检查返回信息是否符合预期',self.classid_setup not in IDlist)


class tc001001:
    name = '老师API_添加老师1 - tc001001'

    def __init__(self):
        self.setup_classid = None
        self.classlist = None
        self.teacherID = None

    def setup(self):
        INFO('执行初始化操作：获取已有班级的classID，再通过json.dump方法获取含classID的json字符串')
        r_setup = yjyxAPI.getClass().json()
        setup_retlist = r_setup['retlist']
        INFO(setup_retlist)
        for i in setup_retlist:
            self.setup_classid = i['id']

        list_setup = [{"id": self.setup_classid}]
        self.classlist = json.dumps(list_setup)

    def teardown(self):
        INFO('执行清除操作：删除用例中新建的教师')
        yjyxAPI.deleteTeacher(self.teacherID)

    def teststeps(self):
        STEP(1,'调用创建老师API，学科ID为1')

        r1 = yjyxAPI.addTeacher('老师001001','老师001001',1,self.classlist,'123456789','tc001001@123.com','100102100312120311').json()
        INFO(r1)
        self.teacherID = r1['id']
        retcode1 = r1['retcode']
        exceptr1 = 0

        INFO(f'实际的返回结果是：{retcode1}')
        INFO(f'预期的返回结果是：{exceptr1}')
        CHECK_POINT('检查返回结果是否成功创建',retcode1 == exceptr1)

        STEP(2,'调用列出老师API')

        r2 = yjyxAPI.getTearcher(1).json()
        retlist2 = r2['retlist']
        exceptr2 = [{
            "username": "老师001001",
            "teachclasslist": [self.setup_classid],
            "realname": "老师001001",
            "id": self.teacherID,
            "phonenumber": "123456789",
            "email": "tc001001@123.com",
            "idcardnumber": "100102100312120311"
        }]

        INFO(f'实际的返回结果是：{retlist2}')
        INFO(f'预期的返回结果是：{exceptr2}')
        CHECK_POINT('检查返回结果是否与第一步信息相同',retlist2 == exceptr2)


class tc005001:
    name = 'WebUI_老师登陆 - tc005001'

    def __init__(self):
        self.classlist = None
        self.classid = None
        self.teacherid = None

    def setup(self):
        INFO('开始执行用例初始化操作：调用列出班级API，获取classlist')

        r_setup = yjyxAPI.getClass().json()
        retlist_setup = r_setup['retlist']
        for cid in retlist_setup:
            self.classid = cid['id']

        list_setup = [{"id": self.classid}]
        self.classlist = json.dumps(list_setup)

    def teardown(self):
        INFO('开始执行用例清除操作1：关闭浏览器')
        wd = GSTORE['wd']
        wd.quit()

        INFO('开始执行用例清除操作2：删除用例中新建的老师')
        r_teardown = yjyxAPI.deleteTeacher(self.teacherid).json()
        INFO(r_teardown)


    def teststeps(self):
        STEP(1,'调用创建老师API')
        r_step1 = yjyxAPI.addTeacher('tc005001','tc005001',1,self.classlist,'121232321','005001@qq.com','500101222145456512').json()
        INFO(f'创建老师API实际返回的结果：{r_step1}')
        self.teacherid = r_step1['id']


        STEP(2,'以STEP1中的账号登陆Web系统')
        open_browser()
        teacher_login('tc005001')
        sleep(3)

        STEP(3,'获取首页各项信息')
        wd = GSTORE['wd']
        schoolname = wd.find_element(By.XPATH, '//tr[1]/td[2]/a').text
        teachername = wd.find_element(By.XPATH,'//tr[2]/td[2]/a').text
        subject = wd.find_element(By.XPATH,'//tr[3]/td[2]/a').text
        gold = wd.find_element(By.XPATH,'//tr[4]/td[2]/a').text
        minilessons = wd.find_element(By.XPATH,'//div[1]/a/h2/strong').text
        homework = wd.find_element(By.XPATH,'//div[2]/a/h2/strong').text

        teacherdata = {
            '学校名称': schoolname,
            '姓名': teachername,
            '学科': subject,
            '金币': gold,
            '微课': minilessons,
            '作业': homework
        }

        exceptdata = {
            '学校名称': '白月学院00002',
            '姓名': 'tc005001',
            '学科': '初中数学',
            '金币': '0',
            '微课': '0',
            '作业': '0'
        }

        INFO(f'预期的结果是：{exceptdata}')
        INFO(f'实际的结果是：{teacherdata}')
        CHECK_POINT('检查结果是否正确', exceptdata == teacherdata)

        # STEP(4,'点击班级学生菜单')
        # ac = ActionChains(wd)   # 模拟鼠标悬停至目标元素
        # ac.move_to_element(
        #     wd.find_element(By.XPATH, '//div/ul/li[4]/a')
        # ).perform()
        #
        # wd.find_element(By.XPATH, '//li[4]/ul/a[2]/li/span').click() # 点击班级学生
        # sleep(1)
        #
        # wd.find_element(By.XPATH,'//div[1]/div[2]/a').click() # 点击列表中第一行班级