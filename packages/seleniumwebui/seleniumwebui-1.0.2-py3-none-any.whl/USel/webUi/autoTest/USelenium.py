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
from USel.webUi.autoTest.USeleniumImplement import USeleniumImplement


class USelenium(USeleniumImplement):
    
    def __init__(self):
        '''
        
        '''
#         self.driver = webdriver.Chrome()
        self.windowHandles = []
        self.driver = ''
    
    
    def initDriver(self, driverType, options=None, timeout=10):
        '''
        
        :param driverType:
        :param timeout:
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
            self.driver.implicitly_wait(timeout)
        except:
            print('initDriver：初始化webdriver失败')
            return False
    
    
    def getPageSource(self, timeout=10):
        try:
            page_source = self.driver.page_source
            self.driver.implicitly_wait(timeout)
            return page_source
        except:
            print('getPageSource：获取界面源码失败')
            return False
        
    
    def openUrl(self, url, timeout=10):
        '''
        
        :param url:
        :param timeout:
        '''
        if ('http://' not in url) and ('https://' not in url):
            url = 'http://' + url
        try:
            get_url = self.driver.get(url)
            self.driver.implicitly_wait(time_to_wait=timeout)
            return get_url
        except:
            print('openUrl：打开目标网址失败')
            return False
    
    
    def getTitle(self):
        '''
        
        '''
        try:
            return self.driver.title
        except:
            print('getTitle：获取窗口title失败')
            return False
    
    
    def currentUrl(self, timeout=10):
        '''
        
        :param timeout:
        '''
        try:
            self.driver.implicitly_wait(timeout)
            return self.driver.current_url
        except:
            print('currentUrl：获取窗口url失败')
            return False
    
    def elementIsEnabled(self, att_type, attribute, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param timeout:
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
        
        :param att_type:
        :param attribute:
        :param timeout:
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
        
        :param att_type:
        :param attribute:
        :param timeout:
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
        
        :param att_type:
        :param attribute:
        :param attributeValue:    textContent, innerHTML, outerHTML, id, name, class and so on.
        :param timeout:
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
        
        :param att_type:
        :param attribute:
        :param timeout:
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
        
        :param forBack:
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
        
        :param timeout:
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
        
        :param att_type:
        :param attribute:
        :param timeout:
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
        
        :param figName:
        :param timeout:
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
         
        :param cookieName:
        :param timeout:
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
         
        :param cookieDict:
        :param timeout:
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
         
        :param timeout:
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
         
        :param windowName:  也可使用handler
        :param timeout:
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
         
        :param att_type:
        :param attribute:
        :param pareDefault:
        :param timeout:
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
        
        :param timeout:
        '''
        try:
            self.driver.implicitly_wait(timeout)
            return self.driver.switch_to_alert().accept()
        except:
            print('alertAccept：alert弹窗接受失败')
            return False 
    
    
    def alertDismiss(self, timeout=10):
        '''
        
        :param timeout:
        '''
        try:
            self.driver.implicitly_wait(timeout)
            return self.driver.switch_to_alert().dismiss()
        except:
            print('alertDismiss：alert弹窗取消失败')
            return False 
    
    
    def alertGetText(self, timeout=10):
        '''
        
        :param timeout:
        '''
        try:
            self.driver.implicitly_wait(timeout)
            return self.driver.switch_to_alert().text
        except:
            print('alertGetText：alert弹窗内容获取失败')
            return False 
        
        
    def alertSetText(self, alert_text, timeout=10):
        '''
        
        :param alert_text:
        :param timeout:
        '''
        try:
            self.driver.implicitly_wait(timeout)
            return self.driver.switch_to_alert().send_keys(alert_text)
        except:
            print('alertSetText：alert弹窗填写内容失败')
            return False 
             
     
    def copyText(self, att_type, attribute, timeout=2):
        '''
         
        :param att_type:
        :param attribute:
        :param timeout:
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
        except Exception as e:
            print('copyText：元素定位失败，或复制文本失败。', e)
            return False 
     
     
    def pasteText(self, att_type, attribute, timeout=2):
        '''
         
        :param att_type:
        :param attribute:
        :param timeout:
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
        except:
            print('pasteText：元素定位失败，或粘贴文本失败。')
            return False 
     
     
    def enterKey(self, att_type, attribute, timeout=10):
        '''
         
        :param att_type:
        :param attribute:
        :param timeout:
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
        
        :param att_type:
        :param attribute:
        :param text_value:
        :param timeout:
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
        
        :param att_type:
        :param attribute:
        :param timeout:
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
        
        :param att_type:
        :param attribute:
        :param select_obj:
        :param select_type:
        :param select_text:
        :param timeout:
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
        
        :param att_type:
        :param attribute:
        :param deselect_type:
        :param select_text:
        :param timeout:
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
        
        :param att_type:
        :param attribute:
        :param timeout:
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
        
        :param att_type:
        :param attribute:
        :param option_type:
        :param timeout:
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
            print('selectText：选择下拉列表元素失败。')
            return False 
        
    
    def selectFun(self, att_type, attribute, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param timeout:
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
                
#             self.selectFun(s, select_type, select_text, timeout)
            self.driver.implicitly_wait(timeout)
            return select
        except:
            print('selectFun：元素定位失败，或获取文本信息失败。')
            return False 
        
    
    def btnClick(self, att_type, attribute, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param timeout:
        '''
        try:
            if att_type == 'id':
                self.driver.find_element_by_id(attribute).textclick()
            if att_type == 'xpath':
                self.driver.find_element_by_xpath(attribute).textclick()
            if att_type == 'css':
                self.driver.find_element_by_css_selector(attribute).textclick()
            if att_type == 'text':
                self.driver.find_element_by_link_text(attribute).textclick()
            if att_type == 'name':
                self.driver.find_element_by_name(attribute).textclick()
        
            self.driver.implicitly_wait(timeout)
            return True
        except Exception as e:
            print('btnClick：元素定位失败，或点击事件失败。', e)
            return False  
    
    
    def doubleClick(self, att_type, attribute, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param timeout:
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
        
        :param att_type:
        :param attribute:
        :param timeout:
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
        
        :param att_type:
        :param attribute:
        :param timeout:
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
        
        :param att_type:
        :param attribute:
        :param timeout:
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
        
        :param att_type:
        :param attribute:
        :param filePath:
        :param timeout:
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
            webEle.textclick()  # 点击上传图片按钮
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
        
        :param timeout:
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
        
        :param timeout:
        '''
        try:
            time.sleep(timeout)
            return self.driver.window_handles
        except:
            print('getWindowHandle：获取窗口尺寸失败')
            return False  
    
    
    def setWindowSize(self, windowSize, timeout=1):
        '''
        
        :param windowSize:
        :param timeout:
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
        
        :param timeout:
        '''
        try:
            self.driver.implicitly_wait(timeout)
            return self.driver.get_window_size('current')
        except Exception as e:
            print('获取浏览器窗口大小失败', e)
            return False
        
    
    def quit(self):
        '''
        
        '''
        try:
            self.driver.quit()
            return True
        except:
            print('退出浏览器失败')
            return False
        
        
    def close(self):
        '''
        
        '''
        try:
            self.driver.close()
            return True
        except:
            print('关闭窗口失败')
            return False
        
if __name__ == "__main__":
    us = USelenium()