from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, UpdateView, DeleteView)
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from .models import (Schema, Column, DataTypes, DataSet)
from .forms import (ColumnForm)
from .csv_generator import CsvFaker
from .tasks import make_file_async


# Create your views here.

class SchemaListView(ListView):
    model = Schema


class SchemaDetailView(DetailView):
    model = Schema


class SchemaCreateView(LoginRequiredMixin, CreateView):
    model = Schema
    fields = ["name"]

    def form_valid(self, form):
        slug = slugify(form.instance.name)
        try:
            # Check if this order number is not used by other column
            Schema.objects.get(slug=slug)
            form.add_error('name', 'Some other schema already uses similar name.'
                                    ' Please choose another one.')
            return self.form_invalid(form)
        except:
            pass
        return super().form_valid(form)


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
        order = form.instance.order
        try:
            # Check if this order number is not used by other column
            Column.objects.get(schema=schema, order=order)
            form.add_error('order', 'Some other column already uses this order number.'
                                    ' Please choose another one.')
            return self.form_invalid(form)
        except:
            pass

        try:
            # Check if column name slug is not unique
            slug = slugify(form.instance.name)
            Column.objects.get(slug=slug)
            form.add_error('name', 'Some other column already uses similar name.'
                                   ' Please choose another one.')
            return self.form_invalid(form)
        except:
            pass

        form.instance.schema = schema
        return super().form_valid(form)


class ColumnUpdateView(LoginRequiredMixin, UpdateView):
    model = Column
    form_class = ColumnForm

    def form_valid(self, form):
        order = form.instance.order
        schema = form.instance.schema
        print(self.kwargs["slug"])
        try:
            # Check if this order number is not used by other column
            column = Column.objects.get(schema=schema, order=order)
            if column.slug != self.kwargs["slug"]:
                form.add_error('order', 'Some other column already uses this order number.'
                                        ' Please choose another on.')
                return self.form_invalid(form)
        except:
            pass
        return super().form_valid(form)


class ColumnDeleteView(LoginRequiredMixin, DeleteView):
    model = Column

    def get_success_url(self, **kwargs):
        column = Column.objects.get(slug=self.kwargs["slug"])
        schema = Schema.objects.get(columns=column)
        return reverse_lazy('schemas:schema_detail', kwargs={'slug': schema.slug})


class DataSetListView(ListView):
    model = DataSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['schema_list'] = Schema.objects.all()
        return context


class GenerateFileView(View):
    """
    This view creates a new Dataset (with a file) based on Schema and Rows parameters.
    """
    model = DataSet

    def post(self, request, *args, **kwargs):
        schema = request.POST["schema"]
        rows = request.POST["rows"]
        status = "processing"
        new_data = DataSet.objects.create(title=schema, status=status)
        new_data.save()
        make_file_async.delay(schema, rows, new_data.pk)
        # CsvFaker.make_file(schema, rows, new_data.pk)
        return redirect(reverse("schemas:dataset_list"))


class DataSetStatusView(View):
    """
    This view return file url and status
    """

    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        data_set = DataSet.objects.get(pk=pk)
        status = {
            "status": data_set.status,
            "url": str(data_set.url),
        }
        return JsonResponse(status, status=200)
