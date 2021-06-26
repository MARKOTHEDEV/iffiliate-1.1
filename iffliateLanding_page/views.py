from django.shortcuts import render,get_object_or_404,redirect,resolve_url,redirect,HttpResponseRedirect
from django.views.generic import ListView,DetailView, detail
from django.contrib.auth.views import LoginView
# Create your views here.
from iffliateLanding_page import models
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from users import serializers
from users import models as userModels
from django.contrib.auth import authenticate, get_user_model, login
from django.conf import settings
import datetime,requests,json
from rest_framework.response import Response
from datetime import datetime as dt
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model
"password rest import"
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator 
from django.core.mail import BadHeaderError, send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import views as djangopassword_restviews
from django.core.exceptions import ValidationError
from django.utils.http import ( urlsafe_base64_decode,)


"End of password rest import"



TODAY = datetime.date.today()


def index(request):
    'shows us the landing page if u new to the qebsite'
    return render(request,'iffliateLanding_page/index.html')


def product(request):
    
    return render(request,'iffliateLanding_page/product.html')


def pricing(request):
    'this just renders the pricing page it also has some funtionality to imporve security'
    subObject = False
    if request.user != 'AnonymousUser ':
        # get_object_or_404()
        get_membershipType = userModels.Membership.objects.get(membership_type='Free')
        "if the current logged in user is on a free mode UserMembership then return true"
        try:
            currentUserMembership =  userModels.UserMembership.objects.get(user=request.user,membership=get_membershipType)
            subObject = userModels.Subscription.objects.filter(user_membership=currentUserMembership).exists()
            # print(currentUserMembership)
            # if subObject == False
        except:
            pass
    



    context={'isNotUserOn_aPaidSub':subObject}
    return render(request,'iffliateLanding_page/pricing.html',context)

def ourTeam(request):
    return render(request,'iffliateLanding_page/team.html')

def support(request):
    return render(request,'iffliateLanding_page/support.html')

def contactUs(request):
    return render(request,'iffliateLanding_page/contact.html')
    

def signup(request):
    return render(request,'iffliateLanding_page/signup.html')

def errorpage(request):
    return render(request,'iffliateLanding_page/errorPage.html')

class CreateUserApi(CreateAPIView):
    'this view assit the signup funtion but it has just one job create a user'
    queryset = get_user_model().objects.all()
    # this serializer class is located at the user App
    serializer_class = serializers.UserSerializers


def password_reset_request(request):
    if request.method == "POST":
        # print(request.POST)
        domain = request.headers['Host']
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = get_user_model().objects.filter(email=data)
            # You can use more than one way like this for resetting the password.
            # ...filter(Q(email=data) | Q(username=data))
            # but with this you may need to change the password_reset form as well.
            # print('associated_users',associated_users)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_subject.txt"
                    c = {
                        "email": user.email,
                        'domain': domain,
                        'site_name': 'Interface',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email])
                        # print("email sent")
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()

    return render(request=request, template_name="registration/password_reset_form.html",
                  context={"password_reset_form": password_reset_form})


class CustomPasswordResetConfirmView(djangopassword_restviews.PasswordResetConfirmView):
    
    template_name ='registration/password_reset_confirm.html'

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
          
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist, ValidationError):
            user = None
        return user

# def signin(request):
#     return render(request,'iffliateLanding_page/signin.html')

class SignInView(LoginView):
    template_name = 'iffliateLanding_page/signin.html'    
    # def dispatch(self, request, *args, **kwargs):
    #     return super(CLASS_NAME, self).dispatch(request, *args, **kwargs)



    # def get_success_url(self):
        # url = self.get_redirect_url()
        # return url or resolve_url(settings.LOGIN_REDIRECT_URL)

class SignInAPIView(APIView):
    serializer_class = serializers.SignInSerializer


    def post(self, request, format=None):
        email = self.request.data.get('email')
        password = self.request.data.get('password')
        


        user = authenticate(username=email,password=password)
        if user is not None:
            # well at this point the user is oviously a member! now i can login him in
            login(self.request,user)
            return Response(data={'success':'validated Successfully'})
        
        return Response(data={'error':'Wrong username or password Try again'})

    
"""
THIS JUST A CODE TO CHECK THE EXIPIRE DATE OF THE USER
# if(instance.expires_in < today):
user = self.request.user
# get a free membeship instance
Freememebership = userModels.Membership.objects.get(membership_type='Free')
# check if usermembership is on free mode
is_user_membership_free = userModels.UserMembership.objects.filter(user=user,membership=Freememebership).exists()
user_Membership = userModels.UserMembership.objects.get(user=user)
#  if usermembership is on free mode the it false
if is_user_membership_free == False:
    # the we get the user sub
    usersub = userModels.Subscription.objects.get(user_membership=user_Membership)
    # and check for it expire date
    if(usersub.expires_in == TODAY):
        # then set it current sub to false
        'check if the person subcription has expired'
        usersub.active = False
        usersub.save()
        print('hello world')
        # and revert it usermembership to free
        user_Membership.membership = Freememebership
        user_Membership.save()
        # user_Membership


# hassub =  
"""



class BlogListView(ListView):
    model = models.Blog
    template_name = "iffliateLanding_page/blog.html"
    context_object_name = 'Allnews'
    paginate_by = 6

    
    def get_context_data(self, **kwargs):
        'here we just added the 3 rcent blog post'
        context = super(BlogListView, self).get_context_data(**kwargs)
        context['recentNews'] = models.Blog.objects.all().order_by('-date_created')[:3]
        return context



class BlogDetailView(DetailView):
    model = models.Blog
    template_name = "iffliateLanding_page/blog-post.html"
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        'get any news content'
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        context['recentNews'] = models.Blog.objects.all().order_by('-date_created')[:3]
        return context













'HEY THIS CODE HAS TO DO WITH PAYMENT'


# @api_view(['GET'])
@csrf_exempt
def accept_paymentfor_anyplan(request):
    'depending on the plan the person clicks'
    # print(request)
    frontEnddata = json.loads(request.body)
    plan = frontEnddata['plan']
    # print(plan)
    # return JsonResponse({'data':plan})
    # print(request.GET)

    'first after getting a plan then we fetch an membership instance from the database'
    fetch_membership =  userModels.Membership.objects.filter(membership_type=plan).exists()

    # print(fetch_membership)
    'if the plan exist then we can proceed else redrect user back to the subscribe page where there is plan buttons'
    if fetch_membership == False:
        return redirect('subcribe')
    'so we get an instace of the membership model e.g free,medium,gold '
    membership =userModels.Membership.objects.get(membership_type=plan)
    # print('plan price:',membership.price)
    'this just turning or price to kobo'
    price = float(membership.price)*100 # We need to multiply the price by 100 because Paystack receives in kobo and not naira.
    price = int(price)
    
    'now we are intialzing the payment -- Note it a function which is no called yet'
    def init_payment(request):
        'so we got the paystack url for tranzaction'
        url = 'https://api.paystack.co/transaction/initialize'
        'so now we just arangig requests parameter '
        'the request must have a valid email and price'
        headers = {
			'Authorization': 'Bearer '+settings.PAYSTACK_SECRET_KEY,
			'Content-Type' : 'application/json',
			'Accept': 'application/json',
            
        
			}
        print(request)
        body = {
			"email": request.user.email,
			"amount": price
			}
        'so we just push the data to the request url headers and data'
        x = requests.post(url, data=json.dumps(body), headers=headers)
        'so if it not a 200 response return the status code so we know'
        if x.status_code != 200:
            # return str(x.status_code)
            return False
		# else return  a json format 
        results = x.json()
        return results
    # now we called init_payment(request) which we expecting a status code or json format
    initialized = init_payment(request)
    # print(initialized)
    if initialized == False:
        'if the payment wasnt succesfuul redirect the to a unsucceful page'
        pass        
    amount = price/100

    # all we need is the refernce code and acceces_code from the json response
    instance = userModels.PayHistory.objects.create(amount=amount, payment_for=membership, user=request.user,
    # we need to save the reference code so we can check it in our callback funtion if it exists
    paystack_charge_id=initialized['data']['reference'],
    paystack_access_code=initialized['data']['access_code'])
    userModels.UserMembership.objects.filter(user =instance.user).update(reference_code=initialized['data']['reference'])

    # the give me a link to send to javascript which would take me to paystack payment gate way
    link = initialized['data']['authorization_url']
    # print(link)
    # return HttpResponseRedirect(link)   
    return JsonResponse({'link':link})


# this  function get triggered when the payment has finish
def mycallback(request):
    'this funtion is triggered by paystack when the payment went true'
    # in the basic term it the payment gete way call back funtion
    reference = request.GET.get('reference')
    print(reference)
    # if u remeber when we were handling paymnet we stored the refernce in the payment history
    checkpay = userModels.PayHistory.objects.filter(paystack_charge_id=reference).exists()
    if checkpay == False:
        # if it false then payment had error  and did not get to stage of saving the refernce
        'this means payment was not made'
        raise ValueError('payment was not made')
    else:
        # this means the payment went true so we have to get the payhistory instance
        payment = userModels.PayHistory.objects.get(paystack_charge_id=reference)
        # we need to check if the payment was successfull
        def verify_payment(request):
            'so we got the paystack url for tranzaction'
            # so we make a get request to the verify url that includes our refece  
            url = 'https://api.paystack.co/transaction/verify/'+reference
            'so now we just arangig requests parameter '
            'the request must have a valid email and price'
            headers = {
			    'Authorization': 'Bearer '+settings.PAYSTACK_SECRET_KEY,
			    'Content-Type' : 'application/json',
			    'Accept': 'application/json',
			    }
            body = {
			    "reference": payment.paystack_charge_id   
			    }
            'so we just push the data to the request url headers and data'
            x = requests.get(url, data=json.dumps(body), headers=headers)
            'so if it not a 200 response return the status code so we know'
            if x.status_code != 200:
                print('surely not 200')
                return str(x.status_code)
		    # else return  a json format 
            results = x.json()
            return results
    # now we called init_payment(request) which we expecting a status code or json format
    initialized = verify_payment(request)
    print(initialized)
    print(initialized['data']['status'])
    # if the request return success 
    if initialized['data']['status'] == 'success':
        # then run some of the stuff
        userModels.PayHistory.objects.filter(paystack_charge_id=initialized['data']['reference']).update(paid=True,who_is_getting_payed='Iffilate')
        new_payment =userModels.PayHistory.objects.get(paystack_charge_id=initialized['data']['reference'])
        instance =userModels.Membership.objects.get(id=new_payment.payment_for.id)
        sub = userModels.UserMembership.objects.filter(reference_code=initialized['data']['reference']).update(membership=instance)
        user_membership = userModels.UserMembership.objects.get(reference_code=initialized['data']['reference'])
        subscription,created = userModels.Subscription.objects.get_or_create(user_membership=user_membership)   
        subscription.expires_in =  expires_in=dt.now().date() + timedelta(days=user_membership.membership.duration)
        subscription.save()
        # userModels.Subscription.objects.get(user_membership=user_membership, expires_in=dt.now().date() + timedelta(days=user_membership.membership.duration))
        print(instance)
        return redirect('home')
    # after we the person has subscribe and all models are set well redirect them to a
    # sucseesful page telling them they have subscribed
    return redirect('pricing')
