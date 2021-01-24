from django import forms
from .models import Lead

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
        )

# Обычная модель формы


class LeadForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    age = forms.IntegerField(min_value=0)
