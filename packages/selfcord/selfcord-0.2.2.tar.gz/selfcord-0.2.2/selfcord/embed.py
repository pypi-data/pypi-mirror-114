class Embed:
    def __init__(self, title, description="", colour="", url=""):
        if description != "" and colour != "" and url != "":
            self.embed = {"title": title, "description": description, "color": colour, "url": url, "fields": []}
        
        elif description != "" and colour != "" and url == "":
            self.embed = {"title": title, "description": description, "color": colour, "fields": []}

        elif description != "" and colour == "" and url == "":
           self.embed = {"title": title, "description": description, "fields": []}
        
        elif description == "" and colour != "" and url != "":
            self.embed = {"title": title, "color": colour, "url": url, "fields": []}
        
        elif description == "" and colour == "" and url != "":
            self.embed = {"title": title, "url": url, "fields": []}

        elif description == "" and colour == "" and url == "":
             self.embed = {"title": title, "fields": []}
        
    def read(self):
        return self.embed
    def set_footer(self, text, icon_url=""):
        self.embed.update({"footer": {"icon_url": icon_url, "text": text}})
    def set_image(self, url):
        self.embed.update({"image": {"url": url}})
    def set_thumbnail(self, url):
        self.embed.update({"thumbnail": {"url": url}})
    def set_author(self, name, url="", icon_url=""):
        self.embed.update({"author": {"name": name, "url": url, "icon_url": icon_url}})
    def add_field(self, name, value, inline=False):
        self.embed["fields"].append({"name": name, "value": value, "inline": inline})
    