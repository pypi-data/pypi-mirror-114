import selfcord
import sys

from .wrapper import Wrapper

sys.setrecursionlimit(10000)

class Guild:
    def __init__(self, id):
        selfcord.Utils.Logger.log("Requesting more data for guild object from Discord...")
        request = Wrapper.sendDiscordRequest(method="get", urlAddon=f"guilds/{id}", headers={}, payload={}).json()
        selfcord.Utils.Logger.log("Requesting list of channels in guild...")
        channelsrequest = Wrapper.sendDiscordRequest(method="get", urlAddon=f"guilds/{id}/channels", headers={}, payload={}).json()
        channels = []
        self.id = id
        selfcord.Utils.Logger.log("Got name of guild")
        self.name = request["name"]
        selfcord.Utils.Logger.log("Got icon of guild")
        self.icon = request["icon"]
        selfcord.Utils.Logger.log("Got description of guild")
        self.description = request["description"]
        selfcord.Utils.Logger.log("Got owner of guild")
        self.owner = selfcord.User(request["owner_id"])
        selfcord.Utils.Logger.log("Got region of guild")
        self.region = request["region"]
        selfcord.Utils.Logger.log("Got system channel of guild")
        self.system_channel = selfcord.Channel(request["system_channel_id"])
        selfcord.Utils.Logger.log("Got premium tier of guild")
        self.premium_tier = request["premium_tier"]
        selfcord.Utils.Logger.log("Got rules channel of guild")
        self.rules_channel = selfcord.Channel(request["rules_channel_id"])
        selfcord.Utils.Logger.log("Got public updates channel of guild")
        self.public_updates_channel = selfcord.Channel(request["public_updates_channel_id"])

        for channel in channelsrequest:
            channels.append(selfcord.Channel(channel["id"]))

        selfcord.Utils.Logger.log("Got list of channels of guild")
        self.channels = channels