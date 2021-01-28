from django import forms
from django.db.models import fields
from .models import Lead, Agent
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

User = get_user_model()

# Модель формы из уже готовой медели
# Дает возможность сократить обработчик формы методом save()


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'first_name',
            'last_name',
            'age',
            'agent',
            "description",
            "phone_number",
            'email'
        )

# Форма для входа в систему
# -------------------------


class CustomCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}


class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        agents = Agent.objects.filter(organisation=request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents


class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'category',
        )

# Обычная модель формы
# -------------------


class LeadForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    age = forms.IntegerField(min_value=0)
