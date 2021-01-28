# Почтовая форма отправки
from django.core.mail import send_mail
# Проверяем, если пользователь зашел под учетной записью
# Похоже на middleware в express.js
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
# Переадресация
from django.shortcuts import redirect, render
from django.urls import reverse
# Генерирует готовые шаблоны / CRUD+L
# ListView, DetailView, DeleteView, UpdateView
# TemplateView - без использования моделей
from django.views import generic
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from .models import Category, Lead, Agent
from .forms import LeadForm, LeadModelForm, CustomCreationForm, AssignAgentForm, LeadCategoryUpdateForm
# Импортируем миксин из agents, да бы при создании lead была привязка
from agents.mixins import OrganisorAndLoginRequiredMixin


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
class LandingPageView(generic.base.TemplateView):
    # Указываем шаблон который подключаем
    template_name = "landing.html"

# def landing_page(req):
#     return render(req, "landing.html")


# КОТРОЛЛЕР СПИСКА ЛИДОВ
# -----------------------------
class LeadListView(LoginRequiredMixin, generic.list.ListView):
    template_name = "lead_list.html"
    # Подхватывает нашу модель со всеми leads
    # По умолчанию присваивает имя object_list
    # queryset = Lead.objects.all()
    # Присваиваим своё имя объекту
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        # Первоначальный набор лидов для всей организации
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation)
            # Откуда взяли agent__user?
            # agent - из модели класса Lead через который привязан сам агент класс
            # user - ключ в классе агента по которому и будет фильтрация
            # agent__user - фильтруем по Lead'ам с правами агента
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True)
            context.update({
                "unassigned_leads": queryset
            })
        return context
# def lead_list(req):
#     leads = Lead.objects.all()
#     context = {
#         "leads": leads
#     }
#     return render(req, "lead_list.html", context)


# КОТРОЛЛЕР ОДНОГО ЛИДА
# -----------------------------
class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = "lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        # Первоначальный набор лидов для всей организации
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation)
            # Откуда взяли agent__user?
            # agent - из модели класса Lead через который привязан сам агент класс
            # user - ключ в классе агента по которому и будет фильтрация
            # agent__user - фильтруем по Lead'ам с правами агента
            queryset = queryset.filter(agent__user=user)
        return queryset

# def lead_detail(req, pk):
#     lead = Lead.objects.get(id=pk)
#     context = {
#         "lead": lead
#     }
#     return render(req, "lead_detail.html", context)


# КОТРОЛЛЕР СОЗДАНИЯ ЛИДА
# -----------------------------
class LeadCreateView(OrganisorAndLoginRequiredMixin, CreateView):
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
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile
        lead.save()
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
class LeadUpdateView(OrganisorAndLoginRequiredMixin, UpdateView):
    template_name = "lead_update.html"
    # Подхватывает нашу модель со всеми leads
    #queryset = Lead.objects.all()
    # Форм класс для получения данных с формы
    # LeadModelForm - не вызываем!!! т.к. она уже содержит всю информацию
    form_class = LeadModelForm
    # Метод успешной отправки формы, чтоб сделать переадресацию
    # Для динамической ссылки используем метод reverse()

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)

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
class LeadDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = "lead_delete.html"

    def get_success_url(self):
        return reverse("leads:lead-list")

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organisation=user.userprofile)


# def lead_delete(req, pk):
#     lead = Lead.objects.get(id=pk)
#     lead.delete()
#     return redirect('/leads')


# КОТРОЛЛЕР НАЗНАЧЕНИЯ АГЕНТА
# -----------------------------
class AssignAgentView(OrganisorAndLoginRequiredMixin, FormView):
    template_name = "assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.list.ListView):
    template_name = "category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation
            )

        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })
        return context

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        # Первоначальный набор лидов для всей организации
        if user.is_organisor:
            queryset = Category.objects.filter(organisation=user.userprofile)
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation)
        return queryset


class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "lead_category_update.html"

    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        # Первоначальный набор лидов для всей организации
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "category_update.html"

    # def get_queryset(self):
    #     user = self.request.user
    #     # Первоначальный набор лидов для всей организации
    #     if user.is_organisor:
    #         queryset = Category.objects.filter(organisation=user.userprofile)
    #     else:
    #         queryset = Category.objects.filter(
    #             organisation=user.agent.organisation)
    #     return queryset


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "category_delete.html"

    # def get_queryset(self):
    #     user = self.request.user
    #     # Первоначальный набор лидов для всей организации
    #     if user.is_organisor:
    #         queryset = Category.objects.filter(organisation=user.userprofile)
    #     else:
    #         queryset = Category.objects.filter(
    #             organisation=user.agent.organisation)
    #     return queryset

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
