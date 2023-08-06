import selfcord

from .wrapper import Wrapper

class User:
    def __init__(self, id):
        selfcord.Utils.Logger("Requesting more data for user object from Discord...")
        request = Wrapper.sendDiscordRequest("get", urlAddon=f"users/{id}", headers={}, payload={}).json()
        self.id = id
        selfcord.Utils.Logger("Got username of user.")
        self.username = request["username"]
        selfcord.Utils.Logger("Got avatar of user.")
        self.avater = request["avatar"]
        selfcord.Utils.Logger("Got deiscriminator of user.")
        self.discriminator = request["discriminator"]
        selfcord.Utils.Logger("Got public flags of user.")
        self.public_flags = request["public_flags"]
        selfcord.Utils.Logger("Got banner of user.")
        self.banner = request["banner"]