from django.forms import ModelForm
from .models import Column

class ColumnForm(ModelForm):

    class Meta:
        model = Column
        fields = ["name", "order", "data_type", "range_min", "range_max"]
