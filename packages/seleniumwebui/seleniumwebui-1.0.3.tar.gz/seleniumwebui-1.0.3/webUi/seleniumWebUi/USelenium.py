#-*- coding:utf8 -*-
'''
Created on 2021年7月26日

@author: perilong
'''
import time

import pyperclip
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import win32api
import win32con


class USelenium():
    
    def __init__(self):
        '''
        方法名称： init
        USelenium类初始化，包含driver和windowHandle变量初始化
        '''
        self.windowHandles = []
        self.driver = ''
    
    
    def initDriver(self, driverType, options=None, timeout=10):
        '''
        方法名称： initDriver
            Driver初始化，区分driver浏览器，如：谷歌-chrome， 火狐-firefox，edge，ie等浏览器
            ps： 需要将浏览器驱动程序放到path路径下，如windows目录下、python目录下等
        :param driverType: 浏览器驱动类型，谷歌、火狐等 
        :param options: 浏览器选项，设置浏览器参数，默认为空
        :param timeout: 超时等待时间
        :return 返回true或false 当前浏览器打开状态
        '''
        try:
            if driverType == 'chrome':
                if options != None:
                    option = webdriver.ChromeOptions()
                    option.add_argument(options)
                    self.driver = webdriver.Chrome(chrome_options=option)
                else:
                    self.driver = webdriver.Chrome()
            if driverType == 'firefox':
                if options != None:
                    option = webdriver.FirefoxProfile(options)
                    self.driver = webdriver.Chrome(firefox_options=option)
                else:
                    self.driver = webdriver.Firefox(firefox_options=option)
            if driverType == 'edge':
                self.driver = webdriver.Edge()
            if driverType == 'ie':
                self.driver = webdriver.Ie() 
            if driverType == 'opera':
                self.driver = webdriver.Opera()
            if driverType == 'phantom':
                self.driver = webdriver.PhantomJS()
            return True
            self.driver.implicitly_wait(timeout)
        except:
            print('initDriver：初始化webdriver失败')
            return False
    
    
    def getPageSource(self, timeout=10):
        '''
        方法名称： getPageSource
            通过此方法获取当前界面源码
        :param timeout: 超时等待时间
        '''
        try:
            page_source = self.driver.page_source
            self.driver.implicitly_wait(timeout)
            return page_source
        except:
            print('getPageSource：获取界面源码失败')
            return False
        
    
    def openUrl(self, url, timeout=10):
        '''
        方法名称： openUrl
            通过url打开网页界面
        :param url: 待访问网址
        :param timeout: 超时等待时间
        :return 返回True或false，代表网址打开成功或失败
        '''
        if ('http://' not in url) and ('https://' not in url):
            url = 'http://' + url
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(time_to_wait=timeout)
            return True
        except:
            print('openUrl：打开目标网址失败')
            return False
    
    
    def getTitle(self):
        '''
        方法名称： getTitle
            获取当前网页标题名称
        :return 返回当前网页title
        '''
        try:
            return self.driver.title
        except:
            print('getTitle：获取窗口title失败')
            return False
    
    
    def currentUrl(self, timeout=10):
        '''
        方法名称： currentUrl
            获取当前界面url地址
        :param timeout: 超时等待时间
        :return 返回当前网页url地址
        '''
        try:
            self.driver.implicitly_wait(timeout)
            return self.driver.current_url
        except:
            print('currentUrl：获取窗口url失败')
            return False
        
    
    def elementIsEnabled(self, att_type, attribute, timeout=10):
        '''
        方法名称： elementIsEnabled
            查询当前界面元素是否使能
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param timeout: 超时等待时间
        :return 返回当前界面元素是否使能
        '''
        try:
            if att_type == 'id':
                element_enable = self.driver.find_element_by_id(attribute).is_enabled()
            if att_type == 'xpath':
                element_enable = self.driver.find_element_by_xpath(attribute).is_enabled()
            if att_type == 'css':
                element_enable = self.driver.find_element_by_css_selector(attribute).is_enabled()
            if att_type == 'text':
                element_enable = self.driver.find_element_by_link_text(attribute).is_enabled()
            if att_type == 'name':
                element_enable = self.driver.find_element_by_name(attribute).is_enabled()
            
            self.driver.implicitly_wait(timeout)
            return element_enable
        except:
            print('elementIsEnabled：查询元素是否可编辑状态失败')
            return False
        
    
    def elementIsDisplay(self, att_type, attribute, timeout=10):
        '''
        方法名称： elementIsDisplay
            判断当前界面元素是否处于显示状态
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param timeout: 超时等待时间
        :return 返回当前界面元素是否处于显示状态
        '''
        try:
            if att_type == 'id':
                element_display = self.driver.find_element_by_id(attribute).is_displayed()
            if att_type == 'xpath':
                element_display = self.driver.find_element_by_xpath(attribute).is_displayed()
            if att_type == 'css':
                element_display = self.driver.find_element_by_css_selector(attribute).is_displayed()
            if att_type == 'text':
                element_display = self.driver.find_element_by_link_text(attribute).is_displayed()
            if att_type == 'name':
                element_display = self.driver.find_element_by_name(attribute).is_displayed()
            
            self.driver.implicitly_wait(timeout)
            return element_display
        except:
            print('elementIsDisplay：查询元素是否显示状态失败')
            return False 
        
    
    def getTagName(self, att_type, attribute, timeout=10):
        '''
        方法名称： getTagName
            获取当前界面元素的标签名称，如：div、a、input、p等
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param timeout: 超时等待时间
        :return 返回当前界面元素的标签值，如：div、a、input、p等
        '''
        try:
            if att_type == 'id':
                tag_name = self.driver.find_element_by_id(attribute).tag_name
            if att_type == 'xpath':
                tag_name = self.driver.find_element_by_xpath(attribute).tag_name
            if att_type == 'css':
                tag_name = self.driver.find_element_by_css_selector(attribute).tag_name
            if att_type == 'text':
                tag_name = self.driver.find_element_by_link_text(attribute).tag_name
            if att_type == 'name':
                tag_name = self.driver.find_element_by_name(attribute).tag_name
            
            self.driver.implicitly_wait(timeout)
            return tag_name
        except:
            print('getTagName：获取元素的tag-name失败')
            return False 
        
    
    def getAttribute(self, att_type, attribute, attributeValue, timeout=10):
        '''
        方法名称： getAttribute
            获取当前界面元素的属性值，如：name、class、value等
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param attributeValue:    textContent, innerHTML, outerHTML, id, name, class and so on.
        :param timeout: 超时等待时间
        :return 返回当前界面元素的属性值，如：name、class、value等
        '''
        try:
            if att_type == 'id':
                element = self.driver.find_element_by_id(attribute)
            if att_type == 'xpath':
                element = self.driver.find_element_by_xpath(attribute)
            if att_type == 'css':
                element = self.driver.find_element_by_css_selector(attribute)
            if att_type == 'text':
                element = self.driver.find_element_by_link_text(attribute)
            if att_type == 'name':
                element = self.driver.find_element_by_name(attribute)
            
            attr_value = element.get_attribute(attributeValue)
            self.driver.implicitly_wait(timeout)
            return attr_value
        except:
            print('getAttribute：获取元素属性值失败')
            return False 
        
    
    def getElementSize(self, att_type, attribute, timeout=10):
        '''
        方法名称： getElementSize
            获取当前浏览器元素尺寸大小，如：{'height': 28, 'width': 88}
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param timeout: 超时等待时间
        :return 返回当前浏览器元素尺寸大小，如：{'height': 28, 'width': 88}
        '''
        try:
            if att_type == 'id':
                element_exist = self.driver.find_element_by_id(attribute).size
            if att_type == 'xpath':
                element_exist = self.driver.find_element_by_xpath(attribute).size
            if att_type == 'css':
                element_exist = self.driver.find_element_by_css_selector(attribute).size
            if att_type == 'text':
                element_exist = self.driver.find_element_by_link_text(attribute).size
            if att_type == 'name':
                element_exist = self.driver.find_element_by_name(attribute).size
            
            self.driver.implicitly_wait(timeout)
            return element_exist
        except:
            print('getElementSize：获取元素尺寸大小失败')
            return False 
            
    
    def windowForBack(self, forBack, timeout=10):
        '''
        方法名称： windowForBack
            浏览器前进和后退按钮，可根据浏览器访问使用前进后退参数
        :param forBack: 浏览器前进、后退，参数值： forward、back
        :return 返回true或false，表示浏览器前进（后退）成功或失败
        '''
        try:
            if forBack == 'forward':
                self.driver.forward()
            if forBack == 'back':
                self.driver.back()
            self.driver.implicitly_wait(timeout)
            return True
        except:
            print('windowForBack：窗口前进或后退失败')
            return False
    
    
    def refresh(self, timeout=10):
        '''
        方法名称： refresh
            浏览器刷新当前界面
        :param timeout: 超时等待时间
        :return 返回true或false，表示浏览器刷新成功或失败
        '''
        try:
            self.driver.refresh()
            self.driver.implicitly_wait(timeout)
            return True
        except:
            print('refresh：窗口刷新失败')
            return False        
    
    
    def elementIsExist(self, att_type, attribute, timeout=10):
        '''
        方法名称： elementIsExist
            判断浏览器界面是否存证该元素
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param timeout: 超时等待时间
        :return 返回true或false，成功访问到该元素或没有访问到
        '''
        element_exist = ''
        try:
            if att_type == 'id':
                element_exist = self.driver.find_element_by_id(attribute)
            if att_type == 'xpath':
                element_exist = self.driver.find_element_by_xpath(attribute)
            if att_type == 'css':
                element_exist = self.driver.find_element_by_css_selector(attribute)
            if att_type == 'text':
                element_exist = self.driver.find_element_by_link_text(attribute)
            if att_type == 'name':
                element_exist = self.driver.find_element_by_name(attribute)
            
            self.driver.implicitly_wait(timeout)
            return element_exist
        except:
            return False 
        
    
    def saveScreenShot(self, figName, timeout=10):
        '''
        方法名称： saveScreenShot
            浏览器当前界面截图
        :param figName: 界面截图保存图片名称
        :param timeout: 超时等待时间
        :return 返回true或false，浏览器界面截图成功或失败
        '''
        try:
            self.driver.save_screenshot(figName)
            self.driver.implicitly_wait(timeout)
            return True
        except:
            print('saveScreenShot：窗口截屏失败')
            return False        
    
    
    def getCookie(self, cookieName='', timeout=10):
        '''
        方法名称： getCookie
            获取网页cookie，通过cookiename获取对应的key值，如果cookiename为空，
            则获取所有的cookie。
        :param cookieName: cookie名称-获取对应cookie值
        :param timeout: 超时等待时间
        :return 返回所获取到的cookie值
        '''
        try:
            self.driver.implicitly_wait(timeout)
            if cookieName == '':
                return self.driver.get_cookie()
            else:
                return self.driver.get_cookie(cookieName)
        except:
            print('getCookie：获取cookie失败')
            return False   
         
       
    def addCookie(self, cookieDict, timeout=10):
        '''
        方法名称： addCookie
            添加网页cookie，通过key:value键值对方式添加
        :param cookieDict: cookie列表，包含name、value
        :param timeout: 超时等待时间
        :return 返回true或false，来表示添加cookie成功或失败
        '''
        try:
            self.driver.add_cookie(cookieDict)
            self.driver.implicitly_wait(timeout)
            return True 
        except:
            print('addCookie：添加cookie失败')
            return False   
     
     
    def deleteAllCookie(self, timeout=10):
        '''
        方法名称： deleteAllCookie
            删除网页所有cookie，清空完网页所有cookie值
        :param timeout: 超时等待时间
        :return 返回true或false，来表示清空cookie成功或失败
        '''
        try:
            self.driver.delete_all_cookies()
            self.driver.implicitly_wait(timeout)
            return True
        except:
            print('deleteAllCookie：删除所有cookie失败')
            return False 
         
     
    def switchWindow(self, windowName, timeout=10):
        '''
        方法名称： switchWindow
            通过浏览器窗口的handler切换浏览器window
        :param windowName:  也可使用handler
        :param timeout: 超时等待时间
        :return 返回true或false，来表示切换window成功或失败
        '''
        try:
            self.driver.switch_to_window(windowName)
            self.driver.implicitly_wait(timeout)
            return True
        except:
            print('deleteAllCookie：删除所有cookie失败')
            return False 
     
     
    def switchFrame(self, att_type, attribute, pareDefault='', timeout=10):
        '''
        方法名称： switchFrame
            通过给定的frame（通过元素定位frame）跳转frame
            default： 跳转到最顶层frame
            parent： 跳转父frame
            给定值：  跳转指定的frame
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param pareDefault: frame跳转方式、包含顶层、上层
        :param timeout: 超时等待时间
        :return 返回true或false，来表示切换frame成功或失败
        '''
        try:
            if pareDefault == 'default':
                self.driver.switch_to_default_content()
                self.driver.implicitly_wait(timeout)
                return True
            if pareDefault == 'parent':
                self.driver.switch_to.parent_frame()
                self.driver.implicitly_wait(timeout)
                return True
        except:
            print('deleteAllCookie：删除所有cookie失败')
            return False 
         
        try:
            if att_type == 'id':
                switch_frame = self.driver.find_element_by_id(attribute)
                self.driver.switch_to.frame(switch_frame)
            if att_type == 'xpath':
                switch_frame = self.driver.find_element_by_xpath(attribute)
                self.driver.switch_to.frame(switch_frame)
            if att_type == 'css':
                switch_frame = self.driver.find_element_by_css_selector(attribute)
                self.driver.switch_to.frame(switch_frame)
            if att_type == 'text':
                switch_frame = self.driver.find_element_by_link_text(attribute)
                self.driver.switch_to.frame(switch_frame)
            if att_type == 'name':
                switch_frame = self.driver.find_element_by_name(attribute)
                self.driver.switch_to.frame(switch_frame)
          
            self.driver.implicitly_wait(timeout)
            return True
        except Exception as e:
            print('switchFrame：元素定位失败，或切换frame失败。', e)
            return False
    
    
    def alertAccept(self, timeout=10):
        '''
        方法名称： alertAccept
            弹窗确定，通过点击弹窗确定按钮结束弹窗
        :param timeout: 超时等待时间
        :return 返回true或false，来表示弹窗alert确定点击成功或失败
        '''
        try:
            self.driver.switch_to_alert().accept()
            self.driver.implicitly_wait(timeout)
            return True
        except:
            print('alertAccept：alert弹窗接受失败')
            return False 
    
    
    def alertDismiss(self, timeout=10):
        '''
        方法名称： alertDismiss
            弹窗取消，通过点击弹窗取消按钮结束弹窗
        :param timeout: 超时等待时间
        :return 返回true或false，来表示弹窗alert取消点击成功或失败
        '''
        try:
            self.driver.implicitly_wait(timeout)
            return self.driver.switch_to_alert().dismiss()
        except:
            print('alertDismiss：alert弹窗取消失败')
            return False 
    
    
    def alertGetText(self, timeout=10):
        '''
        方法名称： alertGetText
            获取弹窗提示内容
        :param timeout: 超时等待时间
        :return 返回获取回来的弹窗提示内容
        '''
        try:
            self.driver.implicitly_wait(timeout)
            return self.driver.switch_to_alert().text
        except:
            print('alertGetText：alert弹窗内容获取失败')
            return False 
        
        
    def alertSetText(self, alert_text, timeout=10):
        '''
        方法名称： alertSetText
            弹窗文本框中内容填写
        :param alert_text:
        :param timeout: 超时等待时间
        :return 返回true或false，来表示弹窗alert弹窗内容填写成功或失败
        '''
        try:
            self.driver.switch_to_alert().send_keys(alert_text)
            self.driver.implicitly_wait(timeout)
            return True
        except:
            print('alertSetText：alert弹窗填写内容失败')
            return False 
             
     
    def copyText(self, att_type, attribute, timeout=2):
        '''
        方法名称： copyText
            复制文本框内容： 支持复制input框和多文本框中内容
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param timeout: 超时等待时间
        :return 返回true或false，来表示复制内容成功或失败
        '''
        cpText = ''
        try:
            if att_type == 'id':
                cpText = self.driver.find_element_by_id(attribute)
            if att_type == 'xpath':
                cpText= self.driver.find_element_by_xpath(attribute)
            if att_type == 'css':
                cpText= self.driver.find_element_by_css_selector(attribute)
            if att_type == 'text':
                cpText= self.driver.find_element_by_link_text(attribute)
            if att_type == 'name':
                cpText= self.driver.find_element_by_name(attribute)
          
            cpText.send_keys(Keys.CONTROL, 'a')
            time.sleep(timeout)
            cpText.send_keys(Keys.CONTROL, 'c')
            time.sleep(timeout)
            return True
        except Exception as e:
            print('copyText：元素定位失败，或复制文本失败。', e)
            return False 
     
     
    def pasteText(self, att_type, attribute, timeout=2):
        '''
        方法名称： pasteText
            粘贴内容： 支持粘贴input框和多文本框中内容
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param timeout: 超时等待时间
        :return 返回true或false，来表示粘贴内容成功或失败
        '''
        try:
            if att_type == 'id':
                cpText = self.driver.find_element_by_id(attribute)
            if att_type == 'xpath':
                cpText= self.driver.find_element_by_xpath(attribute)
            if att_type == 'css':
                cpText= self.driver.find_element_by_css_selector(attribute)
            if att_type == 'text':
                cpText= self.driver.find_element_by_link_text(attribute)
            if att_type == 'name':
                cpText= self.driver.find_element_by_name(attribute)
          
            cpText.send_keys(Keys.CONTROL, 'v')
            time.sleep(timeout)
            return True
        except:
            print('pasteText：元素定位失败，或粘贴文本失败。')
            return False 
     
     
    def enterKey(self, att_type, attribute, timeout=10):
        '''
        方法名称： enterKey
            模拟回车键点击元素
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param timeout: 超时等待时间
        :return 返回true或false，来表示点击元素成功或失败
        '''
        try:
            if att_type == 'id':
                self.driver.find_element_by_id(attribute).send_keys(Keys.RETURN)
            if att_type == 'xpath':
                self.driver.find_element_by_xpath(attribute).send_keys(Keys.RETURN)
            if att_type == 'css':
                self.driver.find_element_by_css_selector(attribute).send_keys(Keys.RETURN)
            if att_type == 'text':
                self.driver.find_element_by_link_text(attribute).send_keys(Keys.RETURN)
            if att_type == 'name':
                self.driver.find_element_by_name(attribute).send_keys(Keys.RETURN)
            self.driver.implicitly_wait(timeout)
            return True
        except:
            print('enterKey：输入回车e失败')
            return False 
        
     
    def setText(self, att_type, attribute, text_value, timeout=10):
        '''
        方法名称： setText
            输入框填写内容，首先清除输入框已有内容，再在其中填写内容
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param text_value:
        :param timeout: 超时等待时间
        :return 返回true或false，来表示内容填写成功或失败
        '''
        try:
            if att_type == 'id':
                self.driver.find_element_by_id(attribute).clear()
                self.driver.find_element_by_id(attribute).send_keys(text_value)
            if att_type == 'xpath':
                self.driver.find_element_by_xpath(attribute).clear()
                self.driver.find_element_by_xpath(attribute).send_keys(text_value)
            if att_type == 'css':
                self.driver.find_element_by_css_selector(attribute).clear()
                self.driver.find_element_by_css_selector(attribute).send_keys(text_value)
            if att_type == 'text':
                self.driver.find_element_by_link_text(attribute).clear()
                self.driver.find_element_by_link_text(attribute).send_keys(text_value)
            if att_type == 'name':
                self.driver.find_element_by_name(attribute).clear()
                self.driver.find_element_by_name(attribute).send_keys(text_value)
         
            self.driver.implicitly_wait(timeout)
            return True
        except Exception as e:
            print('setText：元素定位失败，或文本输入失败。', e)
            return False 
     
     
    def getText(self, att_type, attribute, timeout=10):
        '''
        方法名称： getText
            获取元素内文本text值
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param timeout: 超时等待时间
        :return 返回值为获取回来的text值
        '''
        try:
            if att_type == 'id':
                getText = self.driver.find_element_by_id(attribute).text
            if att_type == 'xpath':
                getText = self.driver.find_element_by_xpath(attribute).text
            if att_type == 'css':
                getText = self.driver.find_element_by_css_selector(attribute).text
            if att_type == 'text':
                getText = self.driver.find_element_by_link_text(attribute).text
            if att_type == 'name':
                getText = self.driver.find_element_by_name(attribute).text
         
            self.driver.implicitly_wait(timeout)
            return getText
        except:
            print('getText：元素定位失败，或获取文本信息失败。')
            return False  
    
    
    def selectText(self, att_type, attribute, select_type, select_text, timeout=10):
        '''
        方法名称： selectText
            选择下拉框值，可通过index、value、text值来选择下拉框
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param select_obj: 待选择的元素
        :param select_type: 选择类型，分为：index， value， text
        :param select_text: 选择的实际值
        :param timeout: 超时等待时间
        :return 返回true或false，来表示下拉框内容选择成功或失败
        '''
        
        try:
            select = self.selectFun(att_type, attribute, timeout)
            
            if select_type == 'index':
                Select(select).select_by_index(select_text)
            if select_type == 'value':
                Select(select).select_by_value(select_text)
            if select_type == 'text':
                Select(select).select_by_visible_text(select_text)
            
            self.driver.implicitly_wait(timeout)
            return True
        except:
            print('selectText：选择下拉列表元素失败。')
            return False 
        
    
    def unselectText(self, att_type, attribute, deselect_type, select_text, timeout=10):
        '''
        方法名称： unselectText
            取消所选内容，取消单选框或复选框内容的选择，可取消单个或者所有选择
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param deselect_type: 反选类型， 
                            all： 取消所有选择
                            index： 通过index取消选择内容
                            value: 通过value取消选择内容
                            text： 通过文本内容取消选择
        :param select_text:
        :param timeout: 超时等待时间
        :return 返回true或false，来表示单项或复选框取消选择成功或失败
        '''
        try:
            select = self.selectFun(att_type, attribute, timeout)
            
            if deselect_type == 'all':
                Select(select).deselect_all()
            if deselect_type == 'index':
                Select(select).deselect_by_index(select_text)
            if deselect_type == 'value':
                Select(select).deselect_by_value(select_text)
            if deselect_type == 'text':
                Select(select).deselect_by_visible_text(select_text)
            
            self.driver.implicitly_wait(timeout)
            return True
        except:
            print('selectText：选择下拉列表元素失败。')
            return False 
    
    
    def elementIsSelect(self, att_type, attribute, timeout=10):
        '''
        方法名称： elementIsSelect
            判断元素是否被选中-针对单项或复选框
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param timeout: 超时等待时间
        :return 返回判断结果，结果判断是否被选中
        '''
        try:
            is_select = ''
            if att_type == 'id':
                is_select = self.driver.find_element_by_id(attribute).is_selected()
            if att_type == 'xpath':
                is_select = self.driver.find_element_by_xpath(attribute).is_selected()
            if att_type == 'css':
                is_select = self.driver.find_element_by_css_selector(attribute).is_selected()
            if att_type == 'text':
                is_select = self.driver.find_element_by_link_text(attribute).is_selected()
            if att_type == 'name':
                is_select = self.driver.find_element_by_name(attribute).is_selected()
         
            self.driver.implicitly_wait(timeout)
            return is_select
        except:
            print('elementIsSelect：元素定位失败，或元素选择状态查询失败失败。')
            return False 
    
    
    def selectOption(self, att_type, attribute, option_type, timeout=10):
        '''
        方法名称： selectOption
            获取检查选项内容，可检查首选项和所有选项
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param option_type: 支持首选项和所有选项检查
        :param timeout: 超时等待时间
        :return 返回检查结果，首选项值或所有选项的列表合集
        '''
        try:
            options = ''
            select = self.selectFun(att_type, attribute, timeout)
            
            if option_type == 'all':
                options = Select(select).all_selected_options
            if option_type == 'first':
                options = Select(select).first_selected_option
            
            self.driver.implicitly_wait(timeout)
            return options
        except:
            print('selectOption：选择选项值失败。')
            return False 
        
    
    def selectFun(self, att_type, attribute, timeout=10):
        '''
        方法名称： selectFun
            通过元素类型和值，获取到元素对象，并返回
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param timeout: 超时等待时间
        :return 返回下拉框元素对象
        '''
        select = ''
        try:
            if att_type == 'id':
                select = self.driver.find_element_by_id(attribute)
            if att_type == 'xpath':
                select = self.driver.find_element_by_xpath(attribute)
            if att_type == 'css':
                select = self.driver.find_element_by_css_selector(attribute)
            if att_type == 'text':
                select = self.driver.find_element_by_link_text(attribute)
            if att_type == 'name':
                select = self.driver.find_element_by_name(attribute)
                
            self.driver.implicitly_wait(timeout)
            return select
        except:
            print('selectFun：元素定位失败，或获取文本信息失败。')
            return False 
        
    
    def click(self, att_type, attribute, timeout=10):
        '''
        方法名称： click
            模拟鼠标左键点击，并返回点击结果
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param timeout: 超时等待时间
        :return 返回true或false，来表示鼠标左键点击成功或失败
        '''
        try:
            if att_type == 'id':
                self.driver.find_element_by_id(attribute).click()
            if att_type == 'xpath':
                self.driver.find_element_by_xpath(attribute).click()
            if att_type == 'css':
                self.driver.find_element_by_css_selector(attribute).click()
            if att_type == 'text':
                self.driver.find_element_by_link_text(attribute).click()
            if att_type == 'name':
                self.driver.find_element_by_name(attribute).click()
        
            self.driver.implicitly_wait(timeout)
            return True
        except Exception as e:
            print('click：元素定位失败，或点击事件失败。', e)
            return False  
    
    
    def doubleClick(self, att_type, attribute, timeout=10):
        '''
        方法名称： doubleClick
            模拟鼠标左键双击，并返回点击结果
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param timeout: 超时等待时间
        :return 返回true或false，来表示鼠标左键双击成功或失败
        '''
        try:
            if att_type == 'id':
                element = self.driver.find_element_by_id(attribute)
                ActionChains(self.driver).double_click(element).perform()
            if att_type == 'xpath':
                element = self.driver.find_element_by_xpath(attribute)
                ActionChains(self.driver).double_click(element).perform()
            if att_type == 'css':
                element = self.driver.find_element_by_css_selector(attribute)
                ActionChains(self.driver).double_click(element).perform()
            if att_type == 'text':
                element = self.driver.find_element_by_link_text(attribute)
                ActionChains(self.driver).double_click(element).perform()
            if att_type == 'name':
                element = self.driver.find_element_by_name(attribute)
                ActionChains(self.driver).double_click(element).perform()
        
            self.driver.implicitly_wait(timeout)
            return True
        except Exception as e:
            print('doubleClick：元素定位失败，或双击事件失败。', e)
            return False  
    
    
    def rightClick(self, att_type, attribute, timeout=10):
        '''
        方法名称： rightClick
            模拟鼠标右键双击，并返回点击结果
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param timeout: 超时等待时间
        :return 返回true或false，来表示鼠标右键单击成功或失败
        '''
        try:
            if att_type == 'id':
                element = self.driver.find_element_by_id(attribute)
                ActionChains(self.driver).context_click(element).perform()
            if att_type == 'xpath':
                element = self.driver.find_element_by_xpath(attribute)
                ActionChains(self.driver).context_click(element).perform()
            if att_type == 'css':
                element = self.driver.find_element_by_css_selector(attribute)
                ActionChains(self.driver).context_click(element).perform()
            if att_type == 'text':
                element = self.driver.find_element_by_link_text(attribute)
                ActionChains(self.driver).context_click(element).perform()
            if att_type == 'name':
                element = self.driver.find_element_by_name(attribute)
                ActionChains(self.driver).context_click(element).perform()
        
            self.driver.implicitly_wait(timeout)
            return True
        except Exception as e:
            print('rightClick：元素定位失败，或右键点击事件失败。', e)
            return False  
        
    
    def mouseDown(self, att_type, attribute, timeout=10):
        '''
        方法名称： mouseDown
            模拟鼠标左键按下操作，并返回按下结果
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param timeout: 超时等待时间
        :return 返回true或false，来表示鼠标左键按下成功或失败
        '''
        try:
            if att_type == 'id':
                element = self.driver.find_element_by_id(attribute)
                ActionChains(self.driver).click_and_hold(element).perform()
            if att_type == 'xpath':
                element = self.driver.find_element_by_xpath(attribute)
                ActionChains(self.driver).click_and_hold(element).perform()
            if att_type == 'css':
                element = self.driver.find_element_by_css_selector(attribute)
                ActionChains(self.driver).click_and_hold(element).perform()
            if att_type == 'text':
                element = self.driver.find_element_by_link_text(attribute)
                ActionChains(self.driver).click_and_hold(element).perform()
            if att_type == 'name':
                element = self.driver.find_element_by_name(attribute)
                ActionChains(self.driver).click_and_hold(element).perform()
        
            self.driver.implicitly_wait(timeout)
            return True
        except Exception as e:
            print('mouseDown：元素定位失败，或鼠标按下事件失败。', e)
            return False  
    
    
    def dragAndDrop(self, source_att_type, source_attribute, target_att_type, target_attribute, timeout=10):
        '''
        方法名称： dragAndDrop
            模拟鼠标左键拖动操作，从A元素拖动到B元素，并返回按下结果
        :param source_att_type: 源元素定位类型，如id、xpath、css等
        :param source_attribute: 源元素定位值（包含id、xpath等等我方式的实际值）
        :param target_att_type: 目的元素定位类型，如id、xpath、css等
        :param target_attribute: 目的元素定位值（包含id、xpath等等我方式的实际值）
        :param timeout: 超时等待时间
        :return 返回true或false，来表示鼠标左键拖动成功或失败
        '''
        drag = drop = ''
        try:
            if source_att_type == 'id':
                drag = self.driver.find_element_by_id(source_attribute)
            if source_att_type == 'xpath':
                drag = self.driver.find_element_by_xpath(source_attribute)
            if source_att_type == 'css':
                drag = self.driver.find_element_by_css_selector(source_attribute)
            if source_att_type == 'text':
                drag = self.driver.find_element_by_link_text(source_attribute)
            if source_att_type == 'name':
                drag = self.driver.find_element_by_name(source_attribute)
                
            if target_att_type == 'id':
                drop = self.driver.find_element_by_id(target_attribute)
            if target_att_type == 'xpath':
                drop = self.driver.find_element_by_xpath(target_attribute)
            if target_att_type == 'css':
                drop = self.driver.find_element_by_css_selector(target_attribute)
            if target_att_type == 'text':
                drop = self.driver.find_element_by_link_text(target_attribute)
            if target_att_type == 'name':
                drop = self.driver.find_element_by_name(target_attribute)
            
            ActionChains(self.driver).drag_and_drop(drag, drop)
            self.driver.implicitly_wait(timeout)
            return True
        except:
            print('dragAndDrop：元素定位失败，或拖动元素失败。')
            return False 
    
    def mouseOver(self, att_type, attribute, timeout=10):
        '''
        方法名称： mouseOver
            模拟鼠标悬浮操作，并返回悬浮结果
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param timeout: 超时等待时间
        :return 返回true或false，来表示鼠标悬浮成功或失败
        '''
        over = ''
        try:
            if att_type == 'id':
                over = self.driver.find_element_by_id(attribute)
            if att_type == 'xpath':
                over = self.driver.find_element_by_xpath(attribute)
            if att_type == 'css':
                over = self.driver.find_element_by_css_selector(attribute)
            if att_type == 'text':
                over = self.driver.find_element_by_link_text(attribute)
            if att_type == 'name':
                over = self.driver.find_element_by_name(attribute)
            
            ActionChains(self.driver).move_to_element(over).perform()
        
            self.driver.implicitly_wait(timeout)
            return True
        except:
            print('mouseOver：元素定位失败，或鼠标悬浮失败。')
            return False  
    
    
    
    def upload_file(self, att_type, attribute, filePath, timeout=60):
        '''
        方法名称： upload_file
            文件上传模拟（非input文本框），模拟桌面按键，并返回结果
        :param att_type: 元素定位类型，如id、xpath、css等
        :param attribute: 元素定位值（包含id、xpath等等我方式的实际值）
        :param filePath: 待上传文件路径
        :param timeout: 超时等待时间
        :return 返回true或false，来表示文件上传成功或失败
        '''
        upAttr = ''
        try:
            if att_type == 'id':
                upAttr = self.driver.find_element_by_id(attribute)
            if att_type == 'xpath':
                upAttr = self.driver.find_element_by_xpath(attribute)
            if att_type == 'css':
                upAttr = self.driver.find_element_by_css_selector(attribute)
            if att_type == 'text':
                upAttr = self.driver.find_element_by_link_text(attribute)
            if att_type == 'name':
                upAttr = self.driver.find_element_by_name(attribute)
                
            self.upLoad_file_no_input(upAttr, filePath)
            self.driver.implicitly_wait(timeout)
            return True
        except Exception as e:
            print('upload_file：元素定位失败，或上传文件失败。', e)
            return False 
    

    def upLoad_file_no_input(self, webEle, filePath, check_Input=''):
        """
        使用 python 的 win32api，win32con 模拟按键输入，实现文件上传操作。
        :param webEle: 页面中的上传文件按钮,是已经获取到的对象
        :param filePath: 要上传的文件地址，绝对路径。如：D:\\timg (1).jpg
        :param check_Input:检查input标签中是否有值 #仅用来检查，在return 处调用一次，多余可删除
        :return: 成功返回：上传文件后的地址，失败返回：""
        """
        try:
            pyperclip.copy(filePath)  # 复制文件路径到剪切板
            webEle.click()  # 点击上传图片按钮
            time.sleep(3)  # 等待程序加载 时间 看你电脑的速度 单位(秒)
            # 发送 ctrl（17） + V（86）按钮
            win32api.keybd_event(17, 0, 0, 0)
            win32api.keybd_event(86, 0, 0, 0)
            win32api.keybd_event(86, 0, win32con.KEYEVENTF_KEYUP, 0)  # 松开按键
            win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(1)
            win32api.keybd_event(13, 0, 0, 0)  # (回车)
            win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)  # 松开按键
            win32api.keybd_event(13, 0, 0, 0)  # (回车)
            win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(2)
        except:
            print('upLoad_file_no_input：元素定位失败，或上传文件失败。')
            return False  
    
    
    def getWindowHandle(self, timeout=1):
        '''
        方法名称： getWindowHandle
            获取当前窗口句柄（handler），同时将窗口句柄添加到windowHandles列表中，并返回
        :param timeout: 超时等待时间
        :return 返回当前窗口句柄值
        '''
        try:
            self.windowHandles.append(self.driver.current_window_handle)
            time.sleep(timeout)
            return self.driver.current_window_handle
        except:
            print('getWindowHandle：获取窗口尺寸失败')
            return False  
    
    
    def getAllWindowHandles(self, timeout=1):
        '''
        方法名称： getAllWindowHandles
            获取所有窗口句柄（handlers），列表形式，并返回
        :param timeout: 超时等待时间
        :return 返回所有窗口句柄列表值
        '''
        try:
            time.sleep(timeout)
            return self.driver.window_handles
        except:
            print('getWindowHandle：获取窗口尺寸失败')
            return False  
    
    
    def setWindowSize(self, windowSize, timeout=1):
        '''
        方法名称： setWindowSize
            设置窗口大小：
                max： 窗口最大化--全屏
                min： 窗口最小化--隐藏
                实际值： ['width','height','handle']
        :param windowSize: 浏览器窗口大小， 格式：['width','height','handle']
        :param timeout: 超时等待时间
        :return 返回true或false，来表示窗口尺寸成功或失败
        '''
        try:
            if isinstance(windowSize, list) and len(windowSize) >=3:
                self.driver.set_window_size(windowSize[0], windowSize[1], windowSize[2])
                time.sleep(timeout)
                return True
        except:
            print('setWindowSize：设置窗口尺寸失败')
            return False    
        
        try:
            if windowSize == 'max':
                self.driver.maximize_window()
                time.sleep(timeout)
                return True
        except:
            print('设置窗口最大化失败')
            return False
        
        try:
            if windowSize == 'min':
                self.driver.minimize_window()
                time.sleep(timeout)
                return True
        except:
            print('设置窗口最小化失败')
            return False
        
    
    def getWindowSize(self,timeout=3):
        '''
        方法名称： getWindowSize
            获取当前窗口的尺寸，并返回
        :param timeout: 超时等待时间
        :return 返回当前窗口尺寸大小
        '''
        try:
            self.driver.implicitly_wait(timeout)
            return self.driver.get_window_size('current')
        except Exception as e:
            print('获取浏览器窗口大小失败', e)
            return False
        
    
    def quit(self):
        '''
        方法名称： quit
            浏览器退出并结束程序
        :return 返回true或false，来表示程序结束成功或失败
        '''
        try:
            self.driver.quit()
            return True
        except:
            print('退出浏览器失败')
            return False
        
        
    def close(self):
        '''
        方法名称： close
            关闭当前浏览器界面，程序未结束
        :return 返回true或false，来表示浏览器界面关闭成功或失败
        '''
        try:
            self.driver.close()
            return True
        except:
            print('关闭窗口失败')
            return False
        
if __name__ == "__main__":
    us = USelenium()