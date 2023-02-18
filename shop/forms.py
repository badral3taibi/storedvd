from django import forms
from django.core.exceptions import ValidationError

from shop.models import Order


class SearchForm(forms.Form):
    q = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Search'}
        )
    )


class OrderModelForm(forms.ModelForm):
    DELIVERY_CHOICES = (
        (0, 'Select, Please'),
        (1, 'Delivery'),
        (2, 'Pickup'),
    )
    delivery = forms.TypedChoiceField(label='Delivery', choices=DELIVERY_CHOICES, coerce=int)

    class Meta:
        model = Order
        exclude = ['discount', 'status', 'need_delivery']
        labels = {'address': 'Full address (Country, city, zip code, street, house, apartment)'}
        widgets = {
            'address': forms.Textarea(
                attrs={'rows': 6, 'cols': 80, 'placeholder': 'You can leave this field empty for self-delivery'}
            ),
            'notice': forms.Textarea(
                attrs={'rows': 6, 'cols': 80}
            )
        }

    def clean_delivery(self):
        data = self.cleaned_data['delivery']
        if data == 0:
            raise ValidationError('You must select a shipping method')
        return data

    def clean(self):
        try:
            delivery = self.cleaned_data['delivery']
            address = self.cleaned_data['address']
            if delivery == 1 and address == '':
                raise ValidationError('Enter a delivery address')
            return self.cleaned_data
        except KeyError:
            pass
