from django import forms




class raffleRegisterForm(forms.Form):
    amount = forms.IntegerField()


class CloseRaffleBatchForm(forms.Form):
    is_close = forms.BooleanField()

    