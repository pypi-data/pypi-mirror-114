import selfcord

from .wrapper import Wrapper

class User:
    def __init__(self, id):
        request = Wrapper.sendDiscordRequest("get", urlAddon=f"users/{id}", headers={}, payload={}).json()
        self.id = id
        self.username = request["username"]
        self.avater = request["avatar"]
        self.discriminator = request["discriminator"]
        self.public_flags = request["public_flags"]
        self.banner = request["banner"]