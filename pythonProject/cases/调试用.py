import requests,json
from lib.classAPI import yjyxAPI
from lib.WebUI import *
from lib.cfg import target_host,vcode,teacherurl
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

# wd = webdriver.Chrome()
# wd.get(teacherurl)
# sleep(1)
#
# open_browser()
# teacher_login('阿茂老师')
# sleep(1)
#
# wd = GSTORE['wd']
#
# ac = ActionChains(wd)
#
# ac.move_to_element(
#     wd.find_element(By.XPATH,'//div/ul/li[4]/a')
# ).perform()
#
# wd.find_element(By.XPATH,'//li[4]/ul/a[2]/li/span').click()
# sleep(1)