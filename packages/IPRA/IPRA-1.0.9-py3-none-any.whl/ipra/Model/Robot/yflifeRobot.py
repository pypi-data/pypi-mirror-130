from os import write
import time
from bs4 import BeautifulSoup
import xlsxwriter
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from ipra.Model.Robot.baseRobot import BaseRobot
import threading

class YFLifeRobot(BaseRobot):
    def __init__(self, policyList, frame, reportPath, inputPath):
        super().__init__(policyList, frame, reportPath, inputPath)
        self.logger.writeLogString('YFLIFE-INIT','ROBOT INIT')
        
        self.maxPolicyListSize = len(policyList)
        self.workbook = xlsxwriter.Workbook(self.reportPath+'YFLIFE_report.xlsx')

        self.basicInfo_sheet = self.workbook.add_worksheet(name="General Information")
        self.basicInfo_sheet.write(0, 0, "Policy No.")
                
        self.logger.writeLogString('YFLIFE-INIT','maxPolicyListSize:'+str(self.maxPolicyListSize))

    def waitingLoginComplete(self):
        self.frame.setStatusLableText("Waiting Login")
        self.logger.writeLogString('YFLIFE-LOGIN','START LOGIN')
        
        pass
    
    def scrapPolicy(self):
        pass

    def buildReport(self):
        self.buildReportThread = threading.Thread(target = self.__buildReport)
        self.buildReportThread.start()
        self.buildReportHeaderFullFlow()
        pass

    def buildReportOnly(self):
        self.buildReportThread = threading.Thread(target = self.__buildReportOnly)
        self.buildReportThread.start()
        self.buildReportHeaderHalfFlow()
        pass

    def buildReportHeaderFullFlow(self):
        self.buildHeaderThread = threading.Thread(target = self.__buildReportHeaderFullFlow)
        self.buildHeaderThread.start()
        pass
    
    def buildReportHeaderHalfFlow(self):
        self.buildHeaderThread = threading.Thread(target = self.__buildReportHeaderHalfFlow)
        self.buildHeaderThread.start()
        pass
    
    def __buildReportHeaderFullFlow(self):
        pass
    
    def __buildReportHeaderHalfFlow(self):
        pass
    
    def __buildReport(self):
        pass
    
    def __buildReportOnly(self):
        pass