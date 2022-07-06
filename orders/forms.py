# coding: utf-8
__author__ = 'swasher'


#from datetime import datetime
from django import forms
from orders.models import Order

# DEPRECATED old library bootstrap3_datetime.widgets
# NEED to be replaced
#from bootstrap3_datetime.widgets import DateTimePicker

# class FilterForm(forms.ModelForm):
#     from_date = forms.DateField(
#         widget=DateTimePicker(options={"format": "DD.MM.YYYY",
#                                        "pickTime": False,
#                                        "showToday": True,
#                                        }
#                               ),
#         required=False
#     )
#
#     to_date = forms.DateField(
#         widget=DateTimePicker(options={"format": "DD.MM.YYYY",
#                                        "pickTime": False,
#                                        "showToday": True
#                                        }
#                               ),
#         required=False
#     )
#
#
#     machine = forms.ModelChoiceField(
#         #label="Машина",
#         queryset=PrintingPress.objects.all(),
#         required=False,
#         empty_label='Машина',
#         widget=forms.Select(attrs={'class': 'selectpicker'})
#     )
#
#     filename = forms.CharField(
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         required=False
#     )
#
#     class Meta:
#         model = Grid
#         fields = ['from_date', 'to_date', 'contractor', 'machine']


class NewOrderForm(forms.ModelForm):
        order = forms.IntegerField(
            widget=forms.NumberInput(),
            required=True
        )

        # start_date = forms.DateField(
        #     widget=DateTimePicker(options={"format": "DD.MM.YYYY",
        #                                    "pickTime": False,
        #                                    "showToday": True,
        #                                    }
        #                           ),
        #     required=False)
        #
        # end_date = forms.DateField(
        #     widget=DateTimePicker(options={"format": "DD.MM.YYYY",
        #                                    "pickTime": False,
        #                                    "showToday": True,
        #                                    }
        #                           ),
        #     required=False)

        class Meta:
            model = Order
            # fields = ['order', 'start_date', 'end_date']
            fields = ['order']

