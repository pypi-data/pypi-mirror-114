#-*- coding:utf8 -*-
'''
Created on 2021年7月26日

@author: perilong
'''
import time
from USelenium.webUi.autoTest.USelenium import USelenium


us = USelenium()
us.initDriver('chrome')
us.openUrl('http://192.168.1.166/USelenium/#/login')
us.setWindowSize('max')
us.setText('xpath', '//*[@id="login"]/div/div[1]/input', 'mrray')
us.setText('xpath', '//*[@id="login"]/div/div[2]/input', '123qaz')
time.sleep(2)
us.btnClick('xpath', '//*[@id="login"]/div/button')
time.sleep(5)

# 区块链
us.btnClick('xpath', '//*[@id="asideBox"]/ul/li[2]/div/span')
us.btnClick('xpath', '//*[@id="asideBox"]/ul/li[2]/ul/li[2]')
chainName = us.getText('xpath', '//*[@id="blockManage"]/div[3]/div[1]/div[3]/table/tbody/tr/td[2]/div')
if chainName == 'mrray':
    us.btnClick('xpath', '//*[@id="blockManage"]/div[3]/div[1]/div[3]/table/tbody/tr/td[9]/div/span[1]')
    us.btnClick('xpath', '//*[@id="tab-/BlockManage/BlockPoint"]')
    
    us.btnClick('xpath', '//*[@id="scrollcontract"]/div[1]/div[2]/div[2]/span[1]/div/div/span/span/i')
    us.btnClick('xpath', '/html/body/div[2]/div[1]/div[1]/ul/li[3]/span')
    
us.btnClick('xpath', '//*[@id="tab-/BlockManage/BlockUser"]')
us.btnClick('xpath', '//*[@id="content"]/div[1]/div[2]/div/div[3]/table/tbody/tr/td[4]/div/span[2]')


us.btnClick('xpath', '//*[@id="asideBox"]/ul/li[5]/div')
us.btnClick('xpath', '//*[@id="order"]/div[1]/button[2]')

# 上传
us.upload_file('xpath', '//*[@id="order"]/div[3]/div[3]/div/div[2]/div[1]/form/div[3]/div/div/div/button', 'E:\\性能.xlsx')
us.btnClick('xpath', '//*[@id="order"]/div[3]/div[3]/div/div[2]/div[1]/form/div[1]/div/div/div/span/span/i')
us.btnClick('xpath', '/html/body/div[3]/div[1]/div[1]/ul/li[4]/span')
us.setText('xpath', '//*[@id="order"]/div[3]/div[3]/div/div[2]/div[1]/form/div[2]/div/div[1]/textarea', 'hello USelenium')
us.btnClick('xpath', '//*[@id="order"]/div[3]/div[3]/div/div[2]/div[2]/button[1]')
time.sleep(10)

print(us.getTitle())
us.windowForBack('back')
time.sleep(5)
us.windowForBack('forward')
us.saveScreenShot('d:/screen.png')
time.sleep(3)
 
us.btnClick('xpath', '//*[@id="order"]/div[1]/button[2]')
time.sleep(3)
# us.copyText('xpath', '//*[@id="order"]/div[3]/div[3]/div/div[2]/div[1]/form/div[1]/label/text()')
# time.sleep(3)
us.pasteText('xpath', '//*[@id="order"]/div[3]/div[3]/div/div[2]/div[1]/form/div[2]/div/div[1]/textarea')
time.sleep(5)
us.btnClick('xpath', '//*[@id="order"]/div[3]/div[3]/div/div[2]/div[2]/button[2]')
time.sleep(5)
print('check element = ', us.elementIsExist('xpath', '//*[@id="order"]/div[3]/div[3]/div/div[2]/div[1]/form/div[2]/label'))
time.sleep(5)
print(us.getCookie('JSESSIONID'))
us.refresh()

print(us.getElementSize('xpath', '//*[@id="order"]/div[1]/button[2]'))
print(us.getAttribute('xpath', '//*[@id="nav2"]/div[1]', 'class'))
print(us.getAttribute('xpath', '//*[@id="nav2"]/div[1]', 'textContent'))
print(us.getTagName('xpath', '//*[@id="container"]/main'))
print(us.elementIsDisplay('xpath', '//*[@id="nav2"]/div[1]'))
print(us.elementIsEnabled('xpath', '//*[@id="order"]/div[1]/div[1]/div[1]/input'))
time.sleep(10)

us.quit()