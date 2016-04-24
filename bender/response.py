class Response():
    def __init__(self, text, repeat=None):
        self.text = text
        self.repeat = repeat

class TextResponse(Response):
    def __init__(self, text, repeat=None):
        Response.__init__(self, text, repeat)

class PictureResponse(Response):
    def __init__(self, text, picture, repeat=None):
        Response.__init__(self, text, repeat)
        self.picture = picture
