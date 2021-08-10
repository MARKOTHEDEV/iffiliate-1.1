from django import forms
from django.forms import fields
from iffliateLanding_page import models as landing_page_Models



class BlogForm(forms.ModelForm):

    
 

    class Meta:
        model = landing_page_Models.Blog
        fields = ['title','content','contentImage']

