class Embed:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self):
        return {
            "title": self.title,
            "description": self.description
            }

    def __str__(self):
        return {
            "title": self.title,
            "description": self.description
            }            