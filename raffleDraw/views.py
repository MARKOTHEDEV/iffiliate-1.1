from django.shortcuts import render

# Create your views here.



def registerFor_RaffleDraw(request):
    'this renders a form that takes user amount and account mostly usefull deails'
    return render(request,'raffleDraw/registerForGame.html')