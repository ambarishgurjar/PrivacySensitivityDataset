from django import forms
from app.models import Customer

class customerForm(forms.ModelForm):
    userName = forms.CharField()
    name = forms.CharField()
    dateOfBirth = forms.DateField(widget=forms.SelectDateWidget)
    accountNumber = forms.CharField(max_length=50)
    phoneNumber = forms.CharField(max_length=50)
    address = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Customer
        fields = '__all__'