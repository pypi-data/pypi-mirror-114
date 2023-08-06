from .wrapper import Wrapper
from .utils import TokenInfo, Logger
from message import Message

class Channel:
    def __init__(self, id):
        request = Wrapper.sendDiscordRequest(method="get", urlAddon=f"channels/{id}", headers={}, payload={})
        self.id = id
        self.name = request["name"]
        self.topic = request["topic"]
        self.guild = request["guild_id"]
        self.type = request["type"]
    def send(self, message=None, embed=None):
        data = {}
        url = "channels/"+str(self.id)+"/messages"
        if message != None:
            data["content"] = message
        if embed != None:
            data["embed"] = embed

        request = Wrapper.sendDiscordRequest(method="post", urlAddon=url, headers={}, payload=data)
        return Message(request["id"], request["content"], request["embeds"], request["channel_id"], request["author"])