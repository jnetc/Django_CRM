# Почтовая форма отправки
from django.core.mail import send_mail
# Переадресация
from django.shortcuts import redirect, render
from django.urls import reverse
# Генерирует готовые шаблоны / CRUD+L
# ListView, DetailView, DeleteView, UpdateView
# TemplateView - без использования моделей
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm, CustomCreationForm


# КОТРОЛЛЕР ДЛЯ ВХОДА В СИСТЕМУ
# -----------------------------
class SignupView(CreateView):
    template_name = "registration/signup.html"
    # Форм класс для получения данных с формы
    # UserCreationForm - не вызываем!!! т.к. она уже содержит всю информацию о пользователе
    form_class = CustomCreationForm
    # Метод успешной отправки формы, чтоб сделать переадресацию
    # Для динамической ссылки используем метод reverse()

    def get_success_url(self):
        return reverse("login")


# КОТРОЛЛЕР ПОСАДОЧНОЙ СТРАНИЦЫ
# -----------------------------
class LandingPageView(TemplateView):
    # Указываем шаблон который подключаем
    template_name = "landing.html"

# def landing_page(req):
#     return render(req, "landing.html")


# КОТРОЛЛЕР СПИСКА ЛИДОВ
# -----------------------------
class LeadListView(ListView):
    template_name = "lead_list.html"
    # Подхватывает нашу модель со всеми leads
    # По умолчанию присваивает имя object_list
    queryset = Lead.objects.all()
    # Присваиваим своё имя объекту
    context_object_name = "leads"


# def lead_list(req):
#     leads = Lead.objects.all()
#     context = {
#         "leads": leads
#     }
#     return render(req, "lead_list.html", context)


# КОТРОЛЛЕР ОДНОГО ЛИДА
# -----------------------------
class LeadDetailView(DetailView):
    template_name = "lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"

# def lead_detail(req, pk):
#     lead = Lead.objects.get(id=pk)
#     context = {
#         "lead": lead
#     }
#     return render(req, "lead_detail.html", context)


# КОТРОЛЛЕР СОЗДАНИЯ ЛИДА
# -----------------------------
class LeadCreateView(CreateView):
    template_name = "lead_create.html"
    # Форм класс для получения данных с формы
    # LeadModelForm - не вызываем!!! т.к. она уже содержит всю информацию
    form_class = LeadModelForm
    # Метод успешной отправки формы, чтоб сделать переадресацию
    # Для динамической ссылки используем метод reverse()

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        # Todo отправка формы при создании
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="admin@mail.com",
            recipient_list=["user@mail.com"]
        )
        return super(LeadCreateView, self).form_valid(form)


# def lead_create(req):
#     form = LeadModelForm()
#     if req.method == "POST":  # Проверяем метод на запрос POST
#         print('Receving a post request')
#         form = LeadModelForm(req.POST)
#         if form.is_valid():  # Проверяем на правильность заполнения формы
#             form.save()  # Сохраняем в базу используя LeadModelForm модель
#             print("The lead has been created")
#             return redirect('/leads')
#     context = {
#         "form": form
#     }
#     return render(req, "lead_create.html", context)


# КОТРОЛЛЕР ОБНОВЛЕНИЯ ЛИДА ПО ID
# -----------------------------
class LeadUpdateView(UpdateView):
    template_name = "lead_update.html"
    # Подхватывает нашу модель со всеми leads
    queryset = Lead.objects.all()
    # Форм класс для получения данных с формы
    # LeadModelForm - не вызываем!!! т.к. она уже содержит всю информацию
    form_class = LeadModelForm
    # Метод успешной отправки формы, чтоб сделать переадресацию
    # Для динамической ссылки используем метод reverse()

    def get_success_url(self):
        return reverse("leads:lead-list")


# def lead_update(req, pk):

#     lead = Lead.objects.get(id=pk)
#     # instance - Применяем нужную модель формы к найденому запросу
#     # Также заполняет все значения в поля формы
#     form = LeadModelForm(instance=lead)

#     if req.method == "POST":  # Проверяем метод на запрос POST
#         print('Receving a post request')
#         form = LeadModelForm(req.POST, instance=lead)
#         if form.is_valid():  # Проверяем на правильность заполнения формы
#             lead.save()
#             print("The lead has been created")
#             return redirect('/leads')

#     context = {
#         "lead": lead,
#         "form": form
#     }
#     return render(req, "lead_update.html", context)


# КОТРОЛЛЕР УДАЛЕНИЯ ЛИДА ПО ID
# -----------------------------
class LeadDeleteView(DeleteView):
    template_name = "lead_delete.html"
    # Подхватывает нашу модель со всеми leads
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")


def lead_delete(req, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')

# def lead_update(req, id):

#     lead = Lead.objects.get(id=id)
#     form = LeadForm()

#     if req.method == "POST":  # Проверяем метод на запрос POST
#         print('Receving a post request')
#         form = LeadForm(req.POST)
#         if form.is_valid():  # Проверяем на правильность заполнения формы
#             print('The form is valid')
#             print(form.cleaned_data)  # Очищаем данные от примесей
#             # Присваиваем значения переменным
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             print("The lead has been created")
#             return redirect('/leads')

#     context = {
#         "lead": lead,
#         "form": form
#     }
#     return render(req, "lead_update.html", context)

# def lead_create(req):
    # form = LeadForm()
    # if req.method == "POST":  # Проверяем метод на запрос POST
    #     print('Receving a post request')
    #     form = LeadForm(req.POST)
    #     if form.is_valid():  # Проверяем на правильность заполнения формы
    #         print('The form is valid')
    #         print(form.cleaned_data)  # Очищаем данные от примесей
    #         # Присваиваем значения переменным
    #         first_name = form.cleaned_data['first_name']
    #         last_name = form.cleaned_data['last_name']
    #         age = form.cleaned_data['age']
    #         agent = Agent.objects.first()
    #         Lead.objects.create(
    #             first_name=first_name,
    #             last_name=last_name,
    #             age=age,
    #             agent=agent
    #         )
    #         print("The lead has been created")
    #         return redirect('/leads')
    # context = {
    #     "form": form
    # }
#     return render(req, "lead_create.html", context)
