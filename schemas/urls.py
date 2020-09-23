"""fakecsv_generator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import (SchemaCreateView, SchemaDeleteView, SchemaUpdateView,
                    SchemaDetailView, SchemaListView, ColumnCreateView,
                    ColumnDeleteView, ColumnUpdateView, DataSetListView,
                    GenerateFileView)

app_name = "schemas"

urlpatterns = [
    path('', SchemaListView.as_view(), name="schema_list"),
    path('<slug:slug>/detail/', SchemaDetailView.as_view(), name="schema_detail"),
    path('<slug:slug>/delete/', SchemaDeleteView.as_view(), name="schema_delete"),
    path('new/', SchemaCreateView.as_view(), name="schema_create"),
    path('<slug:slug>/edit/', SchemaUpdateView.as_view(), name="schema_edit"),
    path('<schema>/columns/new/', ColumnCreateView.as_view(), name="column_create"),
    path('columns/<slug:slug>/edit', ColumnUpdateView.as_view(), name="column_edit"),
    path('columns/<slug:slug>/delete', ColumnDeleteView.as_view(), name="column_delete"),
    path('datasets/', DataSetListView.as_view(), name="dataset_list"),
    path('datasets/new/', GenerateFileView.as_view(), name="dataset_create"),
]