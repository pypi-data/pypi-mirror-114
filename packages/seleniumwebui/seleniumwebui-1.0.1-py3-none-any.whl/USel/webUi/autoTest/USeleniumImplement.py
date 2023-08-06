#-*- coding:utf8 -*-
'''
Created on 2021年7月26日

@author: perilong
'''
from abc import ABCMeta, abstractmethod

class USeleniumImplement(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        '''
        
        '''
        pass
    
    @abstractmethod
    def initDriver(self, driverType, timeout=10):
        '''
        
        :param driverType:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def getPageSource(self, timeout=10):
        '''
        
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def openUrl(self, url, timeout=10):
        '''
        
        :param url:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def currentUrl(self, timeout=10):
        '''
        
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def refresh(self, timeout=10):
        '''
        
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def elementIsEnabled(self, att_type, attribute, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def elementIsDisplay(self, att_type, attribute, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def getTagName(self, att_type, attribute, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def getAttribute(self, att_type, attribute, attributeValue, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param attributeValue:    textContent, innerHTML, outerHTML, id, name, class and so on.
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def elementIsExist(self, att_type, attribute, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def copyText(self, att_type, attribute, timeout=2):
        '''
        
        :param att_type:
        :param attribute:
        :param timeout:
        '''
        pass
    
    
    @abstractmethod
    def pasteText(self, att_type, attribute, timeout=2):
        '''
        
        :param att_type:
        :param attribute:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def enterKey(self, att_type, attribute, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def getTitle(self):
        '''
        
        '''
        pass
    
    @abstractmethod
    def getElementSize(self, att_type, attribute, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def windowForBack(self, forBack, timeout=10):
        '''
        
        :param forBack:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def saveScreenShot(self, figName, timeout=10):
        '''
        
        :param figName:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def getCookie(self, cookieName, timeout=10):
        '''
        
        :param cookieName:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def addCookie(self, cookieDict, timeout=10):
        '''
        
        :param cookieDict:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def deleteAllCookie(self, timeout=10):
        '''
        
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def switchWindow(self, windowName, timeout=10):
        '''
        
        :param windowName:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def switchFrame(self, att_type, attribute, pareDefault='', timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param pareDefault:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def alertAccept(self, timeout):
        '''
        
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def alertDismiss(self, timeout):
        '''
        
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def alertGetText(self, timeout=10):
        '''
        
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def alertSetText(self, alert_text, timeout=10):
        '''
        
        :param alert_text:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def elementIsSelect(self, att_type, attribute, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def setText(self, att_type, attribute, text_value, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param text_value:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def getText(self, att_type, attribute, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def selectFun(self, att_type, attribute, timeout=10):
        '''
        
        :param select_obj:
        :param select_type:
        :param select_text:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def selectText(self, att_type, attribute, select_type, select_text, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param select_type:
        :param select_text:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def unselectText(self, att_type, attribute, deselect_type, select_text, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param deselect_type:
        :param select_text:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def selectOption(self, att_type, attribute, option_type, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param option_type:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def btnClick(self, att_type, attribute, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def doubleClick(self, att_type, attribute, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def rightClick(self, att_type, attribute, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def mouseDown(self, att_type, attribute, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def dragAndDrop(self, source_att_type, source_attribute, target_att_type, target_attribute, timeout=10):
        '''
        
        :param source_att_type:
        :param source_attribute:
        :param target_att_type:
        :param target_attribute:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def mouseOver(self, att_type, attribute, timeout=10):
        '''
        
        :param att_type:
        :param attribute:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def upload_file(self, att_type, attribute, filePath, timeout=60):
        '''
        
        :param att_type:
        :param attribute:
        :param filePath:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def getWindowHandle(self, timeout=1):
        '''
        
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def getAllWindowHandles(self, timeout=1):
        '''
        
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def setWindowSize(self, windowSize, timeout=1):
        '''
        
        :param windowSize:
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def getWindowSize(self,timeout=3):
        '''
        
        :param timeout:
        '''
        pass
    
    @abstractmethod
    def quit(self):
        '''
        
        '''
        pass
    
    @abstractmethod
    def close(self):
        '''
        
        '''
        pass