class User:
    """Класс пользователя
    :param id: идентификатор
    :type id: int
    :param email: эдектронная почта
    :type email: str
    :param password: пароль
    :type password: str"""
    def __init__(self, id: int, email: str, password: str):
        self.id = id
        self.email = email
        self.password = password