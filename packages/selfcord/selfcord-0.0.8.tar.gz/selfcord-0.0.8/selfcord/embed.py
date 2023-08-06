class Embed:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        return {
            "title": self.title,
            "description": self.description
            }     