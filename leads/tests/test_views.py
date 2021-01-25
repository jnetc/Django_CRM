from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class HomePageTest(TestCase):
    def test_status_code_and_template(self):
        # Проверка статис кода
        # Записывем ссылку на шаблон из views.py
        response = self.client.get(reverse("landing-page"))
        # Сравниваем статусы
        self.assertEqual(response.status_code, 200)
        # Проверяем название шаблона
        self.assertTemplateUsed(response, "landing.html")
