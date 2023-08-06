class Embed:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __iter__(self):
        return {
            "title": self.title,
            "description": self.description
            }      