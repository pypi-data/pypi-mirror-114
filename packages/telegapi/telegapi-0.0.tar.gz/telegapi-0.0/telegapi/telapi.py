import json
from . import reqs


######################### CLASS #########################
class telapi():

    URL   = 'https://api.telegram.org/bot{}/'     # Telegram bot API url + TOKEN

    def __init__(self, TOKENFILE:str=None):
        # print('Initializing the class!')
        if TOKENFILE == None:
            raise Exception("Cannot access api without the token.")

        f = open(TOKENFILE, "r")
        contents = []
        if f.mode == 'r':
            contents = f.read().split('\n')

        TOKEN = contents[0]
        self.URL.format(TOKEN)
        gtm = self.getme()
        if gtm:
            print('connection successfull to the API')
        else:
            raise Exception('Failed to test API connectivity!')

    def getme(self):
        try:
            resp  = reqs._get(self.URL + 'getme')                       # 
            return resp
        except Exception as Err:
            print(Err)
            return None

    def getupdates(self, uid:int=None):
        if uid:
            resp = reqs._get(self.URL + 'getUpdates', {'offset': uid + 1})      # Giving the offset Telegram forgets all those messages before this update id
        else:
            resp = reqs._get(self.URL + 'getUpdates')                           # reading the url to get the current updates
        upds     = resp
        newuid   = None                                             # converting the content to JSON
        if upds['result']:
            newuid = upds['result'][0]['update_id']               # Read the update id          
        return upds, newuid
    
    def sendmessage(self, chid, txt, repkey:dict=None):
        if repkey:
            replykey = json.dumps(repkey)
            data =  {'chat_id': chid, 'text': txt, 'reply_markup': replykey}
        else:
            data = {'chat_id': chid, 'text': txt}
        resp = reqs._post(self.URL + 'sendMessage', data = data)
        return resp

    def delmsg(self, chid, msgid):
        data = {'chat_id': chid, 'message_id': msgid}
        resp = reqs._post(self.URL + 'deleteMessage', data = data)
        return resp
    
    def sendoc(self, chid, pathtodoc, caption:str=None, repkey:dict=None):
        if repkey:
            replykey = json.dumps(repkey)
            data  = {'chat_id': chid, 'reply_markup': replykey}
        else:
            data  = {'chat_id': chid}
        data['caption'] = caption
        files           = {'document': (pathtodoc, open(pathtodoc, 'rb'))}
        resp            = reqs._post(self.URL + 'sendDocument', files = files, data = data)
        return resp

if __name__=='__main__':
    TOKENFILE = "/home/pj/Documents/Github Repos/telapi/tokenfile.txt" # Here you need to path to your token file
    inst      = telapi(TOKENFILE)
    inst.getme()