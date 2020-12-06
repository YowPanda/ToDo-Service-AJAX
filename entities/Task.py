from .User import User

class Task:
    """Класс задачи
    :param id: идентификатор
    :type id: int
    :param title: заголовок задачи
    :type title: str
    :param description: описание задачи
    :type description: str
    :param user: пользователь
    :type user: User"""   
    def __init__(self, id: int, title: str, description: str, status: bool, user: User):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.user = user