import requests
from lib.cfg import target_host,vcode

class YJYXAPI:

    def printResponse(self,response):
        print('\n\n-------- HTTP response * begin -------')
        print(response.status_code)

        for k, v in response.headers.items():
            print(f'{k}: {v}')

        print('')

        print(response.json())
        print('-------- HTTP response * end -------\n\n')


    def getClass(self,gradeid=None):
        urlpara = {
            "vcode":f'{vcode}',
            "action": 'list_classes_by_schoolgrade'
        }

        if gradeid is not None:
            urlpara["gradeid"] = gradeid

        response = requests.get(f'{target_host}api/3school/school_classes', params=urlpara)
        self.printResponse(response)

        return response


    def addClass(self,grade,name,studentlimt):

        payload = {
            "vcode":f'{vcode}',
            "action":'add',
            "grade":grade,
            "name":name,
            "studentlimit":studentlimt
        }

        response = requests.post(f'{target_host}api/3school/school_classes',data=payload)
        self.printResponse(response)

        return response


    def editClass(self,classid,name,studentlimit):

        payload = {
            "vcode":f'{vcode}',
            "action":'modify',
            "name":name,
            "studentlimit":studentlimit
        }

        response = requests.put(f'{target_host}api/3school/school_classes/{classid}',data=payload)
        self.printResponse(response)

        return response


    def deleteClass(self,classid):

        payload = {
            "vcode":f'{vcode}'
        }

        response = requests.delete(f'{target_host}api/3school/school_classes/{classid}',data=payload)
        self.printResponse(response)

        return response


    def getTearcher(self,subjectid=None):

        urlpara = {
            'vcode': f'{vcode}',
            'action': 'search_with_pagenation'
            }

        if subjectid is not None:
            urlpara["subjectid"] = subjectid


        response = requests.get(f'{target_host}api/3school/teachers',params=urlpara)
        self.printResponse(response)

        return response



    def addTeacher(self,username,realname,subjectid,classlist,phonenumber,email,idcardnumber):

        payload = {
            "vcode": f'{vcode}',
            "action": 'add',
            "username": username,
            "realname": realname,
            "subjectid": subjectid,
            "classlist": classlist,
            "phonenumber": phonenumber,
            "email": email,
            "idcardnumber": idcardnumber
        }

        response = requests.post(f'{target_host}api/3school/teachers', data=payload)
        self.printResponse(response)

        return response


    def editTeacher(self,teacherid,realname=None,subjectid=None,classlist=None,phonenumber=None,email=None,idcardnumber=None):

        payload = {
            "vcode": f'{vcode}',
            "action": 'modify',
        }

        if realname is not None:
            payload["realname"] = realname
        if subjectid is not None:
            payload["subjectid"] = subjectid
        if classlist is not None:
            payload["classlist"] = classlist
        if phonenumber is not None:
            payload["phonenumber"] = phonenumber
        if email is not None:
            payload["email"] = email
        if idcardnumber is not None:
            payload["idcardnumber"] = idcardnumber

        response = requests.put(f'{target_host}api/3school/teachers/{teacherid}', data=payload)
        self.printResponse(response)

        return response


    def deleteTeacher(self,teacherid):

        payload = {
            "vcode": f'{vcode}'
        }

        response = requests.delete(f'{target_host}api/3school/teachers/{teacherid}', data=payload)
        self.printResponse(response)

        return response


    def getStudent(self):

        urlpara = {
            "vcode": f'{vcode}',
            "action": 'search_with_pagenation'
        }

        response = requests.get(f'{target_host}api/3school/students',params=urlpara)
        self.printResponse(response)

        return response


    def addStudent(self,username,realname,gradeid,classid,phonenumber):

        payload = {
            "vcode": f'{vcode}',
            "action": 'add',
            "username": username,
            "realname": realname,
            "gradeid": gradeid,
            "classid": classid,
            "phonenumber": phonenumber
        }

        response = requests.post(f'{target_host}api/3school/students',data=payload)
        self.printResponse(response)

        return response


    def editStudent(self,studentid,realname=None,phonenumber=None):

        payload = {
            "vcode": f'{vcode}',
            "action": 'modify'
        }

        if realname is not None:
            payload["realname"] = realname
        if phonenumber is not None:
            payload["phonenumber"] = phonenumber

        response = requests.put(f'{target_host}api/3school/students/{studentid}',data=payload)
        self.printResponse(response)

        return response


    def deleteStudent(self,studentid):

        payload = {
            "vcode": f'{vcode}'
        }

        response = requests.delete(f'{target_host}api/3school/students/{studentid}',data=payload)
        self.printResponse(response)

        return response


    def deleteAllTeacher(self):
        r = yjyxAPI.getTearcher().json()
        retlist = r['retlist']
        for tid in retlist:
            yjyxAPI.deleteTeacher(tid['id'])


    def deleteAllClass(self):
        r = yjyxAPI.getClass().json()
        retlist = r['retlist']
        for cid in retlist:
            yjyxAPI.deleteClass(cid['id'])


    def deleteAllStudent(self):
        r = yjyxAPI.getStudent().json()
        retlist = r['retlist']
        for sid in retlist:
            yjyxAPI.deleteStudent(sid['id'])

yjyxAPI = YJYXAPI()


