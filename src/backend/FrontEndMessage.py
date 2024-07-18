class FrontEndMessage:
    def __init__(self, text, images, role, id = None, timestamp = None):
        self.id = id
        self.text = text
        self.images = images
        self.role = role
        self.timestamp = timestamp

    def get_fem(self):
        return {
            "id": self.id,
            "text": self.text,
            "images": self.images,
            "role": self.role,
            "timestamp": self.timestamp
        }