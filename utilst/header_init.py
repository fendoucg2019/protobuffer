class HeaderInit:
    def __init__(self):
        self.platformType = 0
        self.businessType = 0
        self.subType1 = 0
        self.subType2 = 0
        self.msgID = 0
        self.dataLen = 0
        self.checkFlag = 0
        self.devID = 0
        self.word1 = 0
        self.packetTime = 0

    def AddCheckFlag(self):
        temp=self.packetTime//5000
        self.checkFlag=self.platformType*1+self.businessType*2+self.msgID*3+self.devID*4+temp
