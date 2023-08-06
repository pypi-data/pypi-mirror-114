"""
COPYRIGHT BENNY 2021

ALL RIGHTS RESERVED TO THE 
DEVELOPER OF THIS PROJECT.
"""

from .wrapper import Wrapper
from .utils import TokenInfo

class Messages:

    def sendMessage(message, channelId):
        """
        Send a message to channel.

        Parameters:
            - message: The message content.
            - channelId: The channel's ID.
        """

        url = "channels/"+str(channelId)+"/messages"
        return Wrapper.sendDiscordRequest(method="post", urlAddon=url, headers={}, payload={"content": message})

    def editMessage(messageId, newMessage, channelId):
        """
        Delete a message from a channel.

        Parameters:
            - messageId: The message's ID.
            - channelId: The channel's ID.
        """

        url = "channels/"+str(channelId)+"/messages/"+messageId
        return Wrapper.sendDiscordRequest(method="patch", urlAddon=url, headers={}, payload={"content": newMessage})

    def deleteMessage(messageId, channelId):
        """
        Delete a message from a channel.

        Parameters:
            - messageId: The message's ID.
            - channelId: The channel's ID.
        """

        url = "channels/"+str(channelId)+"/messages/"+messageId
        return Wrapper.sendDiscordRequest(method="delete", urlAddon=url, headers={}, payload={})