from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from django.views.generic.list import ListView
from .models import (Schema, Column, DataTypes)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (ColumnForm)
# Create your views here.


class SchemaListView(ListView):
    model = Schema

class SchemaDetailView(DetailView):
    model = Schema

class SchemaCreateView(LoginRequiredMixin, CreateView):
    model = Schema
    fields = ["name"]

class SchemaUpdateView(LoginRequiredMixin, UpdateView):
    model = Schema
    fields = ["name"]

class SchemaDeleteView(LoginRequiredMixin, DeleteView):
    model = Schema
    success_url = reverse_lazy('schemas:schema_list')

class ColumnCreateView(LoginRequiredMixin, CreateView):
    model = Column
    form_class = ColumnForm

    def form_valid(self, form):
        schema = Schema.objects.get(slug=self.kwargs["schema"])
        form.instance.schema = schema
        return super().form_valid(form)


class ColumnUpdateView(LoginRequiredMixin, UpdateView):
    model = Column
    fields = ["name", "order", "data_types"]

class ColumnDeleteView(LoginRequiredMixin, DeleteView):
    model = Column
    # todo update reverse url
    success_url = reverse_lazy('schemas')