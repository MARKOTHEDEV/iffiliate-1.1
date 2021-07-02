from django import forms




class raffleRegisterForm(forms.Form):
    amount = forms.IntegerField()

    