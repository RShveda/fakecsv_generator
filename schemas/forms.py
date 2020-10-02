from django.forms import ModelForm, NumberInput, Select
from django.forms import inlineformset_factory
from .models import Column, Schema


class ColumnForm(ModelForm):

    class Meta:
        model = Column
        fields = ("name", "data_type", "range_min", "range_max", "order",)
        widgets = {
            # 'data_type': Select(attrs={"id": "data-type-input", "onchange": "switchRanges()"}), #this line prevent formset validation on extra form
            'range_min': NumberInput(attrs={"id": "min-range-input", "disabled": "true"}),
            'range_max': NumberInput(attrs={"id": "max-range-input", "disabled": "true"}),
        }

ColumnSetForm = inlineformset_factory(Schema, Column, form=ColumnForm, extra=1, can_delete=True, can_order=True)


