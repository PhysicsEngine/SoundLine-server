import urllib
import requests
from xml.etree import ElementTree

class NetVocaloidRequestLib(object):
    URL = "http://184.73.195.58/vws.php"
    KEY = "mhdt201508"
    VER = "12010101"

    @classmethod
    def getUrl(cls):
        return cls.URL

    @classmethod
    def getParamDict(cls):
        return {'ver':cls.VER, 'key':cls.KEY}

    @classmethod
    def startCreateVocal(cls, xmlFile):
        files = {'vxml': open(xmlFile, 'rb')}
        params = params=cls.getParamDict()
        params['ope'] = 'request'
        try:
            r = requests.post(cls.getUrl(), params=params, files=files)
            e = ElementTree.fromstring(r.text)
        except Exception as e:
            raise NetVocaloidRequestException(e)
        
        if e.find('status').text == 'error':
            raise NetVocaloidRequestException(e.find('message').text)

        try:
            ticketId = e.find('ticketId').text
            print ticketId
            retryAfter = e.find('retryAfter').text
        
            return ticketId, retryAfter
        except Exception as e:
            raise NetVocaloidRequestException(e)


    @classmethod
    def isDoneCreateVocal(cls, ticketId):
        params = cls.getParamDict()
        params['id'] = ticketId
        params['ope'] = 'query'
        try:
            r = requests.get(cls.getUrl(), params=params)
            e = ElementTree.fromstring(r.text)
            status = e.find('status').text
            if status == 'done':
                return True
            elif status == 'working':
                return False
            else:
                raise NetVocaloidRequestException('create vocal has error')
        except Exception as e:
            raise NetVocaloidRequestException(e)

    @classmethod
    def downloadVocalFile(cls, ticketId, output):
        params = cls.getParamDict()
        params['id'] = ticketId
        params['ope'] = 'query'
        try:
            r = requests.get(cls.getUrl(), params=params)
            print r.text
            e = ElementTree.fromstring(r.text)
            status = e.find('status').text
            if status != 'done':
                raise NetVocaloidRequestException('vocal data is not ready')
            urllib.urlretrieve(e.find('url').text, output)

            params['ope'] = 'done'
            r = requests.get(cls.getUrl(), params=params)
            status = e.find('status').text
            
            if status != 'ok':
                raise NetVocaloidRequestException('download vocal file error')
        except Exception as e:
            raise NetVocaloidRequestException(e)

     
class NetVocaloidRequestException(BaseException):
    pass

    
id =  NetVocaloidRequestLib.startCreateVocal('test.xml')
print id
