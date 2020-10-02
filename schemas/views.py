from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, UpdateView, DeleteView, FormView)
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from .models import (Schema, Column, DataTypes, DataSet)
from .forms import (ColumnForm, ColumnSetForm)
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


class SchemaUpdateView(LoginRequiredMixin, UpdateView):
    model = Schema
    fields = ["name"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schema = Schema.objects.get(slug=self.kwargs["slug"])
        if self.request.POST:
            formset = ColumnSetForm(self.request.POST, instance=schema)
        else:
            formset = ColumnSetForm(instance=schema)
        context['formset'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(reverse("schemas:schema_edit", kwargs={"slug":self.object.slug}))
        else:
            print(formset.errors)
            form.add_error("name", "one of the column is invalid")
            return self.form_invalid(form)



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
                                ' Please choose another on.')
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
        try:
            # Check if this order number is not used by other column
            column = Column.objects.get(schema=schema, order=order)
            if (column.slug != self.kwargs["slug"]):
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


class GenerateFileView(LoginRequiredMixin, View):
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
