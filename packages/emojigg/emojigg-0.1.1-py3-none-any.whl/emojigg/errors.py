
class NotImplemented(Exception):
    def __init__(self, message, *args):
        self.message = message
        self.args = args
    
    def __str__(self) -> str:
        return self.message
    
class WrongType(Exception):
    pass