class ServerError(Exception):
    '''Класс - исключение, для обработки ошибок сервера.'''
    def __init__(self, text):
        super().__init__()
        self.text = text

    def __str__(self):
        return self.text
