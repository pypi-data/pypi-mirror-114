import selfcord

from .wrapper import Wrapper

class Message:
    def __init__(self, id, content, embed, channelId, author):
        self.id = id
        self.content = content
        self.channel = selfcord.Channel(channelId)
        self.embed = embed
        self.author = author
    def edit(self, content=None, embed=None):
        url = "channels/"+str(self.channel.id)+"/messages/"+str(self.id)
        request = Wrapper.sendDiscordRequest(method="patch", urlAddon=url, headers={}, payload={"content": content, "embed": embed}).json()
        return Message(request["id"], request["content"], request["embeds"], request["channel_id"], request["author"])        