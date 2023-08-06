import selfcord
import sys

from .wrapper import Wrapper

sys.setrecursionlimit(10000)

class Channel:
    def __init__(self, id):
        selfcord.Utils.Logger.log("Requesting more data for channel object from Discord...")
        request = Wrapper.sendDiscordRequest(method="get", urlAddon=f"channels/{id}", headers={}, payload={}).json()
        self.id = id
        selfcord.Utils.Logger.log("Got name of channel.")
        self.name = request["name"]
        selfcord.Utils.Logger.log("Got topic of channel.")
        self.topic = request["topic"]
        selfcord.Utils.Logger.log("Got guild of channel.")
        self.guild = selfcord.Guild(request["guild_id"])
        selfcord.Utils.Logger.log("Got type of channel.")
        self.type = request["type"]
    def send(self, message=None, embed=None):
        data = {}
        url = "channels/"+str(self.id)+"/messages"
        if message != None:
            data["content"] = message
        if embed != None:
            data["embed"] = embed

        selfcord.Utils.Logger.log(f"Sending message to #{self.name}")
        request = Wrapper.sendDiscordRequest(method="post", urlAddon=url, headers={}, payload=data).json()
        return selfcord.Message(request["id"], request["content"], request["embeds"], request["channel_id"], selfcord.User(request["author"]["id"]))