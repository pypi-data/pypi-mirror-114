"""
COPYRIGHT BENNY 2021

ALL RIGHTS RESERVED TO THE 
DEVELOPER OF THIS PROJECT.
"""

from .wrapper import Wrapper
from .utils import Utils

class UserInfo:

    def getUsername(id):
        """
        Get the username from an id.

        Parameters:
            - id: The users id.
        """

        Utils.Logger.log(f"Returned fetched username from '{id}'.")
        return Wrapper.sendDiscordRequest(method="get", urlAddon=f"users/{id}", headers={}, payload={}).json()["username"]

    def getId(id):
        """
        Get the id from an id.

        Parameters:
            - id: The users id.
        """

        Utils.Logger.log(f"Returned fetched id from '{id}'.")
        return Wrapper.sendDiscordRequest(method="get", urlAddon=f"users/{id}", headers={}, payload={}).json()["id"]

    def getAvatar(id):
        """
        Get the avatar from an id.

        Parameters:
            - id: The users id.
        """

        Utils.Logger.log(f"Returned fetched avatar from '{id}'.")
        return Wrapper.sendDiscordRequest(method="get", urlAddon=f"users/{id}", headers={}, payload={}).json()["avatar"]

    def getBanner(id):
        """
        Get the banner from an id.

        Parameters:
            - id: The users id.
        """

        Utils.Logger.log(f"Returned fetched banner from '{id}'.")
        return Wrapper.sendDiscordRequest(method="get", urlAddon=f"users/{id}", headers={}, payload={}).json()["banner"]

    def getDiscriminator(id):
        """
        Get the discriminator from an id.

        Parameters:
            - id: The users id.
        """

        Utils.Logger.log(f"Returned fetched discriminator from '{id}'.")
        return Wrapper.sendDiscordRequest(method="get", urlAddon=f"users/{id}", headers={}, payload={}).json()["discriminator"]     

    def getPublicFlags(id):
        """
        Get the public flags from an id.

        Parameters:
            - id: The users id.
        """

        Utils.Logger.log(f"Returned fetched public flags from '{id}'.")
        return Wrapper.sendDiscordRequest(method="get", urlAddon=f"users/{id}", headers={}, payload={}).json()["public_flags"]         

    def isBot(id):
        """
        Is the id a bot

        Parameters:
            - id: The users id.
        """

        Utils.Logger.log(f"Returned fetched bot from '{id}'.")
        return Wrapper.sendDiscordRequest(method="get", urlAddon=f"users/{id}", headers={}, payload={}).json()["bot"]                   