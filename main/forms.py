from django import forms
from .models import Order  # make sure your model is named Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
