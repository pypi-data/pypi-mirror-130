from typing import overload
from ipra.Model.Robot.baseRobot import BaseRobot
from ipra.Model.Robot.bocgRobot import BOCGRobot
from ipra.Model.Robot.manulifeRobot import ManulifeRobot
from ipra.Model.Robot.pruRobot import PruRobot
from ipra.Model.Robot.axaRobot import AxaRobot
from ipra.Model.robotThread import robotThread
from ipra.Model.Robot.fwdRobot import FwdRobot
from ipra.Model.Robot.chinaLifeRobot import ChinaLifeRobot
from ipra.Model.Robot.aiaRobot import AiaRobot
from src.ipra.Model.Robot.yflifeRobot import YFLifeRobot

class reportThread (robotThread):
    def __init__(self, type , policyList , frame, reportPath,inputPath):
        robotThread.__init__(self,type,policyList,frame, reportPath,inputPath)
        pass

    def createRobotClass(self):
        if self.type == 'AIA':
            self.robotInstance = AiaRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execReport()
        elif self.type == 'AXA':
            self.robotInstance = AxaRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execReport()
        elif self.type == 'BOCG':
            self.robotInstance = BOCGRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execReport()
        elif self.type == 'CHINA LIFE':
            self.robotInstance = ChinaLifeRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execReport()
        elif self.type == 'PRU':
            self.robotInstance = PruRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execReport()
        elif self.type == "FWD":
            self.robotInstance = FwdRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execReport()
        elif self.type == "MANU LIFE":
            self.robotInstance = ManulifeRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execReport()
        elif self.type == 'YF LIFE':
            self.robotInstance = YFLifeRobot(self.policyList,self.frame,self.reportPath,self.inputPath)
            self.robotInstance.execReport()

    