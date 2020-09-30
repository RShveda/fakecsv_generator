from django.forms import ModelForm, NumberInput, Select
from .models import Column


class ColumnForm(ModelForm):

    class Meta:
        model = Column
        fields = ("name", "order", "data_type", "range_min", "range_max")
        widgets = {
            'data_type': Select(attrs={"id": "data-type-input", "onchange": "switchRanges()"}),
            'range_min': NumberInput(attrs={"id": "min-range-input", "disabled": "true"}),
            'range_max': NumberInput(attrs={"id": "max-range-input", "disabled": "true"}),
        }
