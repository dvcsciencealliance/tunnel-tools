
class TelegramHandler:
    def postInit(self):
        pass

    def __init__(self, bot=None, config=None):
        self.bot = bot
        if config != None:
            self.config = config
        else:
            self.config = {}

    def update(self, update):
        """called when update is recieved"""
        pass
