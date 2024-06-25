

from django import forms
from .models import Subscriber

class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'example@gmail.com', 'style': 'box-shadow: 3px 3px 10px black;border-radius: 50px; height: 50px;width: 700px;border-width: 0px;padding-left:20px;'}),
        }
        labels = {
            'email': '',  # Set the label to an empty string to remove it
        }
