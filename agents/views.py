from django.http import request
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from django.urls import reverse
from .forms import AgentModelForm


class AgentListView(LoginRequiredMixin, ListView):
    template_name = "agent_list.html"

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentDetailView(LoginRequiredMixin, DetailView):
    template_name = "agent_detail.html"
    queryset = Agent.objects.all()

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentCreateView(LoginRequiredMixin, CreateView):
    template_name = "agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        agent = form.save(commit=False)
        agent.organisation = self.request.user.userprofile
        agent.save()
        return super(AgentCreateView, self).form_valid(form)


class AgentUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "agent_update.html"
    queryset = Agent.objects.all()
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")


class AgentDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "agent_delete.html"
    queryset = Agent.objects.all()

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
