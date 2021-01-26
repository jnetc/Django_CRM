from django.core.mail import send_mail
from django.http import request
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from django.urls import reverse
from .forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin
from random import randint


class AgentListView(OrganisorAndLoginRequiredMixin, ListView):
    template_name = "agent_list.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentDetailView(OrganisorAndLoginRequiredMixin, DetailView):
    template_name = "agent_detail.html"
    queryset = Agent.objects.all()

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(OrganisorAndLoginRequiredMixin, CreateView):
    template_name = "agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organisor = False
        user.set_password(f"{randint(0, 1000000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile
        )
        send_mail(
            subject="You are invited to be an agent",
            message="You are added as an agent on DJCRM. Please come login to start working",
            from_email="admin@admin.com",
            recipient_list=[user.email]
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentUpdateView(OrganisorAndLoginRequiredMixin, UpdateView):
    template_name = "agent_update.html"
    queryset = Agent.objects.all()
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")


class AgentDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = "agent_delete.html"
    queryset = Agent.objects.all()

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
