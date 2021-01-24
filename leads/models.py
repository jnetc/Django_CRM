from django.db import models
# Импортируем авторизацию пользователя
# Лучше не использовать, отсутствие гибкости
# from django.contrib.auth import get_user_model

# Импорт готового пользователя DJANGO
from django.contrib.auth.models import AbstractUser

# Модель авторизированого пользователя
# User = get_user_model() - лучше не делать так!!!


class User(AbstractUser):
    pass


class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    # Зависимость от агента
    # При удалении агента, удаляются все "вести"
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name


class Agent(models.Model):
    # Зависимость от пользователя
    # Поля имени и т.д. наследуются от модели пользователя!
    # При удалении пользователя, удаляются "агент" и все "вести"
    # !!! OneToOne - 1 пользователь = 1 агенту
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
