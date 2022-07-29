class Person():
    def __init__(self, id, per_name, position, history_name):
        self.id = id
        self.per_name = per_name
        self.position = position
        self.history_name = history_name

    def getId(self):
        return self.id

    def getPerName(self):
        return self.per_name

    def getPosition(self):
        return self.position

    def getHistoryName(self):
        return self.history_name

    def setPerName(self, per_name):
        self.per_name = per_name

    def setPosition(self, Position):
        self.position = Position

    def setHistoryName(self, history_name):
        self.history_name = history_name




