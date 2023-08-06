# 设备唯一识别码验证
import wmi
import uuid
import hashlib
import requests
import json


class getAuth(object):
    def __init__(self):
        self.c = wmi.WMI()

    def getCpuId(self):
        for cpu in self.c.Win32_Processor():
            return cpu.ProcessorId.strip()

    def getBoardId(self):
        for board_id in self.c.Win32_BaseBoard():
            return board_id.SerialNumber

    def getMacId(self):
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])

    def getBiosId(self):
        for bios_id in self.c.Win32_BIOS():
            return bios_id.SerialNumber.strip()

    def getMd5(self):
        macId = self.getMacId()
        boardId = self.getBoardId()
        cpuId = self.getCpuId()
        string = str(macId) + str(boardId) + str(cpuId) + "helei"
        hl = hashlib.md5()
        hl.update(string.encode(encoding='utf-8'))
        return hl.hexdigest()

    def checkPost(self):
        checkUrl = "http://webhook.phpnbw.com/check/"
        data = {'unId': self.getMd5()}
        checkRes = json.loads(requests.post(checkUrl, data=data).text)
        if checkRes["code"] == 1:
            return 1
        else:
            return self.getMd5()
