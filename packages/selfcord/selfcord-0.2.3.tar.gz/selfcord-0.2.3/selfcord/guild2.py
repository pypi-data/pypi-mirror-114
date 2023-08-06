import selfcord

from .wrapper import Wrapper

class Guild:
    def __init__(self, id):
        selfcord.Utils.Logger("Requesting more data for guild object from Discord...")
        request = Wrapper.sendDiscordRequest(method="get", urlAddon=f"guilds/{id}", headers={}, payload={}).json()
        selfcord.Utils.Logger("Requesting list of channels in guild...")
        channelsrequest = Wrapper.sendDiscordRequest(method="get", urlAddon=f"guilds/{id}/channels", headers={}, payload={}).json()
        channels = []
        self.id = id
        selfcord.Utils.Logger("Got name of guild")
        self.name = request["name"]
        selfcord.Utils.Logger("Got icon of guild")
        self.icon = request["icon"]
        selfcord.Utils.Logger("Got description of guild")
        self.description = request["description"]
        selfcord.Utils.Logger("Got owner of guild")
        self.owner = selfcord.User(request["owner_id"])
        selfcord.Utils.Logger("Got region of guild")
        self.region = request["region"]
        selfcord.Utils.Logger("Got system channel of guild")
        self.system_channel = selfcord.Channel(request["system_channel_id"])
        selfcord.Utils.Logger("Got premium tier of guild")
        self.premium_tier = request["premium_tier"]
        selfcord.Utils.Logger("Got rules channel of guild")
        self.rules_channel = selfcord.Channel(request["rules_channel_id"])
        selfcord.Utils.Logger("Got public updates channel of guild")
        self.public_updates_channel = selfcord.Channel(request["public_updates_channel_id"])

        for channel in channelsrequest:
            channels.append(selfcord.Channel(channel["id"]))

        selfcord.Utils.Logger("Got list of channels of guild")
        self.channels = channels