import selfcord
import sys

from .wrapper import Wrapper

sys.setrecursionlimit(10000)

class User:
    def __init__(self, id):
        selfcord.Utils.Logger.log("Requesting more data for user object from Discord...")
        request = Wrapper.sendDiscordRequest("get", urlAddon=f"users/{id}", headers={}, payload={}).json()
        self.id = id
        selfcord.Utils.Logger.log("Got username of user.")
        self.username = request["username"]
        selfcord.Utils.Logger.log("Got avatar of user.")
        self.avatar = request["avatar"]
        selfcord.Utils.Logger.log("Got discriminator of user.")
        self.discriminator = request["discriminator"]
        selfcord.Utils.Logger.log("Got public flags of user.")
        self.public_flags = request["public_flags"]
        selfcord.Utils.Logger.log("Got banner of user.")
        self.banner = request["banner"]