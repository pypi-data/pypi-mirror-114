import selfcord

from .wrapper import Wrapper

class Guild:
    def __init__(self, id):
        request = Wrapper.sendDiscordRequest(method="get", urlAddon=f"guilds/{id}", headers={}, payload={}).json()
        channelsrequest = Wrapper.sendDiscordRequest(method="get", urlAddon=f"guilds/{id}/channels", headers={}, payload={}).json()
        channels = []
        self.id = id
        self.name = request["name"]
        self.icon = request["icon"]
        self.description = request["description"]
        self.owner = request["owner_id"]
        self.region = request["region"]
        self.system_channel = selfcord.Channel(request["system_channel_id"])
        self.premium_tier = request["premium_tier"]
        self.rules_channel = selfcord.Channel(request["rules_channel_id"])
        self.public_updates_channel = selfcord.Channel(request["public_updates_channel_id"])

        for channel in channelsrequest:
            channels.append(selfcord.Channel(channel["id"]))

        self.channels = channels