"""
COPYRIGHT BENNY 2021

ALL RIGHTS RESERVED TO THE 
DEVELOPER OF THIS PROJECT.
"""

from .wrapper import Wrapper
from .utils import TokenInfo

class User:

    def sendFriendRequest(user):
        """
        Sends a user a friend request.

        Parameters:
            - user: The user's username and discriminator.
        """

        if "#" in user:
            url = "users/@me/relationships"
            payload = {"username": user.split("#")[0], "discriminator": int(user.split("#")[1])}
        else:
            url = "users/@me/relationships/"+user
            payload = {}
        return Wrapper.sendDiscordRequest(method="put", urlAddon=url, headers={}, payload=payload)

    def acceptFriendRequest(userId):
        """
        Accept a user's friend request.
        You must give the ID of the user.

        Parameters:
            - userId: The user's user ID.
        """

        url = "users/@me/relationships/"+userId
        payload = {}
        return Wrapper.sendDiscordRequest(method="put", urlAddon=url, headers={}, payload=payload)

    def blockUser(userId):
        """
        Blocks a user/
        You must give the ID of the user.

        Parameters:
            - userId: The user's user ID.
        """

        url = "users/@me/relationships/"+userId
        payload = {"type": 2}
        return Wrapper.sendDiscordRequest(method="put", urlAddon=url, headers={}, payload=payload)

    def setUsername(username, password):
        """
        Set your username to something new.

        Parameters:
            - username: The new username.
            - password: Your current password.
        """

        url = "users/@me"
        payload = {"username": username, "password": password}
        return Wrapper.sendDiscordRequest(method="patch", urlAddon=url, headers={}, payload=payload)

    def setEmail(email, password):
        """
        Set your email to something new.

        Parameters:
            - email: The new email.
            - password: Your current password.            
        """

        url = "users/@me"
        payload = {"email": email, "password": password}
        return Wrapper.sendDiscordRequest(method="patch", urlAddon=url, headers={}, payload=payload)  

    def setPassword(newPassword, password):
        """
        Set your password to something new.

        Parameters:
            - newPassword: The new password.
            - password: Your current password.
        """    

        url = "users/@me"
        payload = {"password": password, "new_password": newPassword}
        return Wrapper.sendDiscordRequest(method="patch", urlAddon=url, headers={}, payload=payload)

    def setAboutMe(text):
        """
        Set your about me text.

        Parameters:
            - text: The about me text.
        """

        url = "users/@me"
        payload = {"bio": text}
        return Wrapper.sendDiscordRequest(method="patch", urlAddon=url, headers={}, payload=payload) 

    def setCustomStatus(text):
        """
        Set your custom status text.

        Parameters:
            - text: The custom status text.
            - emoji: The custom status emoji.
        """

        url = "users/@me/settings"
        payload = {"custom_status": {"text": text}}
        return Wrapper.sendDiscordRequest(method="patch", urlAddon=url, headers={}, payload=payload) 

    def setTheme(theme):
        """
        Change your discord client theme.

        Parameters:
            - theme: The client theme, dark or light.
        """

        url = "users/@me/settings"
        payload = {"theme": theme.lower()}
        return Wrapper.sendDiscordRequest(method="patch", urlAddon=url, headers={}, payload=payload)                     

    def getUsername():
        """
        Gets the username of the logged in account.
        """

        url = "users/@me"
        request = Wrapper.sendDiscordRequest(method="get", urlAddon=url, headers={}, payload={})
        return request.json()["username"]

    def getDiscriminator():
        """
        Gets the discriminator of the logged in account.
        """

        url = "users/@me"
        request = Wrapper.sendDiscordRequest(method="get", urlAddon=url, headers={}, payload={})
        return request.json()["disciminator"]       

    def getId():
        """
        Gets the id of the logged in account.
        """

        url = "users/@me"
        request = Wrapper.sendDiscordRequest(method="get", urlAddon=url, headers={}, payload={})
        return request.json()["id"]       

    def getAvatar():
        """
        Gets the avatar of the logged in account.
        """

        url = "users/@me"
        request = Wrapper.sendDiscordRequest(method="get", urlAddon=url, headers={}, payload={})
        return request.json()["avatar"] 

    def getFriends():
        """
        Gets the friends of the logged in account.
        """

        friends = []
        request = Wrapper.sendDiscordRequest("get", "users/@me/relationships", headers={}, payload={})
        for item in request.json():
            if item["type"] == 1:
                friends.append({"username": item["user"]["username"], "id": item["user"]["id"], "avatar": item["user"]["avatar"], "discriminator": item["user"]["discriminator"], "public_flags": item["user"]["public_flags"]})

        return friends              