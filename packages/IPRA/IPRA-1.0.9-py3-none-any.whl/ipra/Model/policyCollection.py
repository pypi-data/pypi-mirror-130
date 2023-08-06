
class PolicyCollection:
        
    def __init__(self):
        self.AIA = ['AIA']
        self.AXA = ['AXA']
        self.BOCG = ['BOCG']
        self.CHINALIFE = ['CHINA LIFE']
        self.PRU = ['PRU']
        self.FWD = ['FWD']
        self.MANULIFE = ['MANU LIFE']
        self.YFLIFE = ['YF LIFE']
        self.totalInsurranceList = [
            self.AIA,
            self.AXA,
            self.BOCG,
            self.CHINALIFE,
            self.PRU,
            self.FWD,
            self.MANULIFE,
            self.YFLIFE
        ]
        self.supportedList = ['AIA','AXA','BOCG','CHINA LIFE','PRU','FWD','MANU LIFE','YF LIFE']
        pass
    
    def cleanAllPolicy(self):
        self.AIA = ['AIA']
        self.AXA = ['AXA']
        self.BOCG = ['BOCG']
        self.CHINALIFE = ['CHINA LIFE']
        self.PRU = ['PRU']
        self.FWD = ['FWD']
        self.MANULIFE = ['MANU LIFE']
        self.YFLIFE = ['YF LIFE']
        self.totalInsurranceList = [
            self.AIA,
            self.AXA,
            self.BOCG,
            self.CHINALIFE,
            self.PRU,
            self.FWD,
            self.MANULIFE,
            self.YFLIFE
        ]
    
    def getTotalList(self):
        return self.totalInsurranceList

    def getSupportedList(self):
        return self.supportedList