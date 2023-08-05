import itchat
from itchat.content import *
from collections import defaultdict

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE,
    RECORDING, VOICE, ATTACHMENT, VIDEO, FRIENDS, SYSTEM])
def request_handler(msg):
    if msg['Content'] == 'Progress':
        pass
    elif msg['Content'] == 'Current Tasks':
        pass

class WeChatAssistant(object):

    def __init__(self):
        itchat.auto_login(hostReload=True, enableCmdQR=2)
        self.contact_map = defaultdict(list)
        friends = itchat.get_friends()
        for friend in friends:
            self.contact_map[friend.NickName] = friend
            self.contact_map[friend.UserName] = friend
        
    def send_to_filehelper(self, msg):
        itchat.send_msg(msg, "filehelper")
    
    def send_to_friend(self, toUserName, msg):
        friend = self.contact_map[toUserName]
        itchat.send_msg(msg, friend.UserName)
    
    def boardcast(self, msg, toUsers):
        for user in toUsers:
            friend = self.contact_map[user]
            itchat.send_msg(msg, friend.UserName)