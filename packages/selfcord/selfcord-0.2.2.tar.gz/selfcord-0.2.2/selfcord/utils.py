"""
COPYRIGHT BENNY 2021

ALL RIGHTS RESERVED TO THE 
DEVELOPER OF THIS PROJECT.
"""

from .wrapper import Wrapper

class Utils:

    class Logger:
        def log(message):
            if Wrapper.getLogging():
                print(f"[SELFCORD] {message}")   
            else:
                return   

    class Colour:
        def __init__(self):
            self.red = 0xF93A2F
            self.gold = 0xCC7900
            self.yellow = 0xF8C300
            self.green = 0x00D166
            self.blue = 0x0099E1
            self.purple = 0xA652BB
            self.pink = 0xFD0061

    class TokenInfo:
        def getUsername(token):
            """
            Get the username of a token.

            Parameters:
                - token: The account token.
            """

            Utils.Logger.log(f"Returned fetched username from `{token}`.")
            return Wrapper.sendDiscordRequestCustomToken("get", "users/@me", headers={}, payload={}, token=token).json()["username"]

        def getId(token):
            """
            Get the ID of a token.

            Parameters:
                - token: The account token.
            """

            Utils.Logger.log(f"Returned fetched id from `{token}`.")
            return Wrapper.sendDiscordRequestCustomToken("get", "users/@me", headers={}, payload={}, token=token).json()["id"]  

        def getDiscriminator(token):
            """
            Get the discriminator of a token.

            Parameters:
                - token: The account token.
            """

            Utils.Logger.log(f"Returned fetched discriminator from `{token}`.")
            return Wrapper.sendDiscordRequestCustomToken("get", "users/@me", headers={}, payload={}, token=token).json()["discriminator"]
            
        def getAvatar(token):
            """
            Get the avatar of a token.

            Parameters:
                - token: The account token.
            """

            Utils.Logger.log(f"Returned fetched avatar from `{token}`.")
            return Wrapper.sendDiscordRequestCustomToken("get", "users/@me", headers={}, payload={}, token=token).json()["avatar"]                              

        def getEmail(token):
            """
            Get the email of a token.

            Parameters:
                - token: The account token.
            """

            Utils.Logger.log(f"Returned fetched email from `{token}`.")
            return Wrapper.sendDiscordRequestCustomToken("get", "users/@me", headers={}, payload={}, token=token).json()["email"]

        def getBanner(token):
            """
            Get the banner of a token.

            Parameters:
                - token: The account token.
            """

            Utils.Logger.log(f"Returned fetched banner from `{token}`.")
            return Wrapper.sendDiscordRequestCustomToken("get", "users/@me", headers={}, payload={}, token=token).json()["banner"]

        def getBio(token):
            """
            Get the bio of a token.

            Parameters:
                - token: The account token.
            """

            Utils.Logger.log(f"Returned fetched bio from `{token}`.")
            return Wrapper.sendDiscordRequestCustomToken("get", "users/@me", headers={}, payload={}, token=token).json()["bio"]

        def getCustomStatusText(token):
            """
            Get the custom status text of a token.

            Parameters:
                - token: The account token.
            """

            Utils.Logger.log(f"Returned fetched custom status text from `{token}`.")
            return Wrapper.sendDiscordRequestCustomToken("get", "users/@me/settings", headers={}, payload={}, token=token).json()["custom_status"]["text"]

        def getCustomStatusEmoji(token):
            """
            Get the custom status emoji of a token.

            Parameters:
                - token: The account token.
            """

            Utils.Logger.log(f"Returned fetched custom status emoji from `{token}`.")
            return Wrapper.sendDiscordRequestCustomToken("get", "users/@me/settings", headers={}, payload={}, token=token).json()["custom_status"]["emoji_name"]

        def getStatus(token):
            """
            Get the status of a token.
            Online,Idle,DND,Invisible

            Parameters:
                - token: The account token.
            """

            Utils.Logger.log(f"Returned fetched status from `{token}`.")
            return Wrapper.sendDiscordRequestCustomToken("get", "users/@me/settings", headers={}, payload={}, token=token).json()["status"]

        def getFriends(token):
            """
            Get a list of friends from the token.

            Parameters:
                - token: The account token.
            """

            friends = []
            request = Wrapper.sendDiscordRequestCustomToken("get", "users/@me/relationships", headers={}, payload={}, token=token)
            Utils.Logger.log(f"Fetched friends from `{token}`.")
            for item in request.json():
                if item["type"] == 1:
                    Utils.Logger.log("Appended friend to new list.")
                    friends.append({"username": item["user"]["username"], "id": item["user"]["id"], "avatar": item["user"]["avatar"], "discriminator": item["user"]["discriminator"], "public_flags": item["user"]["public_flags"]})

            Utils.Logger.log("Returned a list of friends.")
            return friends     