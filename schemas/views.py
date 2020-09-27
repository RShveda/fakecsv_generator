from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from django.views.generic.list import ListView
from .models import (Schema, Column, DataTypes, DataSet)
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (ColumnForm)
from .csv_generator import CsvFaker
from .tasks import add as test_task
from .tasks import create_task, make_file_async
from django.http import JsonResponse


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
    fields = ["name", "order", "data_type"]


class ColumnDeleteView(LoginRequiredMixin, DeleteView):
    model = Column
    # todo update reverse url
    success_url = reverse_lazy('schemas')


class DataSetListView(ListView):
    model = DataSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schema_list'] = Schema.objects.all()
        return context


class GenerateFileView(View):
    model = DataSet

    def post(self, request, *args, **kwargs):
        print(request.POST["schema"])
        schema = request.POST["schema"]
        rows = request.POST["rows"]
        # make_file_async.delay(schema, rows)
        status = "processing"
        new_data = DataSet.objects.create(title=schema, status=status, url="")
        CsvFaker.make_file(schema, rows, new_data)
        # result = test_task.delay(1,2)
        new_data.save()
        return redirect(reverse("schemas:dataset_list"))


class DataSetStatusView(View):

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        data_set = DataSet.objects.get(pk=pk)
        status = {
            "status":data_set.status
        }
        data_set.status
        return JsonResponse(status, status=200)




