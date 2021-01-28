# Импорт моделей из базыданных
from django.db import models
#
from django.db.models.signals import post_save
# Импортируем авторизацию пользователя
# Лучше не использовать, отсутствие гибкости
# from django.contrib.auth import get_user_model
# Импорт готового пользователя DJANGO
from django.contrib.auth.models import AbstractUser


# Модель авторизированого пользователя
# User = get_user_model() - лучше не делать так!!!
class User(AbstractUser):
    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    # Зависимость от агента
    # При удалении агента, удаляются все "вести"
    # Опциаональна!!
    agent = models.ForeignKey(
        "Agent", null=True, blank=True, on_delete=models.SET_NULL)
    # Зависимость от агента
    # При удалении агента, удаляются все "вести"
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(
        "Category", related_name="leads", blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.first_name


class Agent(models.Model):
    # Зависимость от пользователя
    # Поля имени и т.д. наследуются от модели пользователя!
    # При удалении пользователя, удаляются "агент" и все "вести"
    # !!! OneToOne - 1 пользователь = 1 агенту
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    # New, Contected, Converted, Unconverted
    name = models.CharField(max_length=30)
    organisation = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# instance - объект данных пользователя
# created - логическое / был ли создан пользователь
def post_user_created_signal(sender, instance, created, **kwargs):
    print(instance, created)
    # если создан
    if created:
        # Записываем в базу
        UserProfile.objects.create(user=instance)


# Используем фунцию post_user_created_signal в момент сохранения пользователя при регистрации
post_save.connect(post_user_created_signal, sender=User)
