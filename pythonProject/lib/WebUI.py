from selenium import webdriver
from selenium.webdriver.common.by import By
from hytest import *
from lib.cfg import *

def open_browser():
    INFO('打开浏览器')
    wd = webdriver.Chrome()
    wd.implicitly_wait(10)

    GSTORE['wd'] = wd


def teacher_login(username,password='888888'):

    wd = GSTORE['wd']

    wd.get(teacherurl)

    wd.find_element(By.ID, 'username').send_keys(username)
    wd.find_element(By.ID, 'password').send_keys(password)
    wd.find_element(By.ID, 'submit').click()


