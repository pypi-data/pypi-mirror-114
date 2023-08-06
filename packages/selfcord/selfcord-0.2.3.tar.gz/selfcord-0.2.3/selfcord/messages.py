"""
COPYRIGHT BENNY 2021

ALL RIGHTS RESERVED TO THE 
DEVELOPER OF THIS PROJECT.
"""

from .wrapper import Wrapper
from .utils import Utils

class Messages:

    def sendMessage(channelId, message=None, embed=None):
        """
        Send a message to channel.

        Parameters:
            - message: The message content.
            - channelId: The channel's ID.
        """

        data = {}
        url = "channels/"+str(channelId)+"/messages"
        if message != None:
            data["content"] = message
        if embed != None:
            data["embed"] = embed

        Utils.Logger.log(f"Sent '{message}' to '{channelId}'.")
        return Wrapper.sendDiscordRequest(method="post", urlAddon=url, headers={}, payload=data)

    def editMessage(messageId, newMessage, channelId):
        """
        Edit a message in a channel.

        Parameters:
            - messageId: The message's ID.
            - channelId: The channel's ID.
        """

        url = "channels/"+str(channelId)+"/messages/"+str(messageId)
        Utils.Logger.log(f"Edited '{messageId}' content to be '{newMessage}' in '{channelId}'.")
        return Wrapper.sendDiscordRequest(method="patch", urlAddon=url, headers={}, payload={"content": newMessage})

    def deleteMessage(messageId, channelId):
        """
        Delete a message from a channel.

        Parameters:
            - messageId: The message's ID.
            - channelId: The channel's ID.
        """

        url = "channels/"+str(channelId)+"/messages/"+str(messageId)
        Utils.Logger.log(f"Deleted '{messageId}' in '{channelId}'.")
        return Wrapper.sendDiscordRequest(method="delete", urlAddon=url, headers={}, payload={})