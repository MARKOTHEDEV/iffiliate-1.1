from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model

import datetime
from datetime import timedelta
from datetime import datetime as dt
from .limitpay import LimitUserPay


today = datetime.date.today()

### Custom User Model Used Here

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of username.
    """
    def create_user(self, email, password):
        """
        Create and save a User with the given email and password.
        """
        if email is None:
            raise ValueError('The Email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(email=email,password=password)
        user.is_staff=True
        user.is_superuser = True
        user.save(using=self._db)

        return user


#### This is User Profile
class User(AbstractBaseUser,PermissionsMixin):
    'custom built usermodel' 
    # name = models.CharField( max_length=100, unique=True)
    email = models.EmailField(unique=True)
    userEarnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    userPics = models.ImageField(upload_to='user/profilepics/%d/%m/',default='user.jpg',null=True)
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def imageUrl(self):
        return self.userPics.url

    def __str__(self):
        return self.email


# #### This is user settings
# class UserSetting(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
#     account_verified = models.BooleanField(default=False)
#     verified_code = models.CharField(max_length=100, default='', blank=True)
#     verification_expires = models.DateField(default=dt.now().date() + timedelta(days=settings.VERIFY_EXPIRE_DAYS))
#     code_expired = models.BooleanField(default=False)
#     recieve_email_notice = models.BooleanField(default=True)



#### User Payment History
class PayHistory(models.Model):
    'keeps track of the users payment and helps me verfy paystack'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    'paystack_access_code we store paystack reference there so we can verfiy payment'
    paystack_charge_id = models.CharField(max_length=100, default='', blank=True)
    paystack_access_code = models.CharField(max_length=100, default='', blank=True)
    payment_for = models.ForeignKey('Membership', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    # is it user that is getting payed or iffiliate
    benefactor_of_payment = (
        ('Iffilate','Iffilate'),
        ('User','User'),
    )
    who_is_getting_payed = models.CharField(choices=benefactor_of_payment,null=True,blank=True,max_length=10)
    
    def __str__(self):
        return self.user.__str__()

    
    @property
    def get_user_end_date(self):
        currentUserMembership = UserMembership.objects.get(user=self.user)
        subObject = Subscription.objects.get(user_membership=currentUserMembership)

        return subObject.expires_in


#### Membership
class Membership(models.Model):
    'this is a object for instances of plans a person can have e.g gold and duration and price'
    MEMBERSHIP_CHOICES = (
    	# ('Extended', 'Extended'), # Note that they are all capitalize//
    	('Gold', 'Gold'),
    	('Silver', 'Silver'),
        ('Bronze', 'Bronze'),
        ('Free', 'Free')
    )
    PERIOD_DURATION = (
        ('Days', 'Days'),
        ('Week', 'Week'),
        ('Months', 'Months'),
    )
    slug = models.SlugField(null=True, blank=True)
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES, default='Free', max_length=30)
    duration = models.PositiveIntegerField(default=7)
    duration_period = models.CharField(max_length=100, default='Day', choices=PERIOD_DURATION)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    earningLimit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,null=True,blank=True)


    

    def __str__(self):
       return self.membership_type

#### User Membership
class UserMembership(models.Model):
    'this is just a user that has a memebership it helps me know if a user is payed or not'
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, related_name='user_membership', on_delete=models.SET_NULL, null=True)
    reference_code = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
       'we use the .__str__() because we are connceted to a ONE TO ONE FIELD'
       return self.user.__str__()


#### User Subscription
class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, related_name='subscription', on_delete=models.CASCADE, default=None)
    expires_in = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.__str__()


class UserRequestPayment(models.Model):
    'this actually save the user OR file the user for payment'
    # user that requested for payment
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    # amount this is the amout the user have currently in his account
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00 ,blank =True)
    # check if we have paid this bitch
    isPaid = models.BooleanField(default=False)
    # account_number e.g 3590450454
    account_number = models.CharField(max_length=160)
    # e.g Mr MARKOTHEDEV
    account_name = models.CharField(max_length=150,blank=True)
    # this will be gotten from a json file in the user app so dont worry
    bank_code = models.CharField(max_length=10,blank=True)
    bank_name = models.CharField(max_length=50,blank=True)
    # this is the most important one we will refrece it back when we wanna pay this person
    recipient_code = models.CharField(max_length=20,blank=True)
    # this is more like a time stamp -> the docs says u cant override it
    date_requested = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f'{self.user} requested for Payment -> {self.amount}'




class MoneyPost(models.Model):
    'This model store all the scrapped post and  feed it to users to read for money'
    title=  models.CharField(max_length=300)
    content = models.TextField()

    @property
    def get_someText(self):
        'get some text from self.content'
        return f'{self.content[0:300]}.....'

    def __str__(self):
        return self.title


class SeenMoneyPost(models.Model):
    'this model is for users that has read a post so we use this model to determine who is getting paid'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    postSeen = models.ForeignKey(MoneyPost,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} has read {self.postSeen}'

class SponsoredPost(models.Model):
    "this is a Table that holds all the SponsoredPost"
    sponsored_post_link = models.CharField(max_length=300)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sponsor_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.sponsor_name} Post'







def paythisUser(request):
    "# this handles updating user Earnings when he reads a particular post" 
    user_membership =  UserMembership.objects.get(user=request.user)
    user = get_user_model().objects.get(email=request.user.email)
    if str(user_membership.membership) == 'Gold':
        # print('pay Gold')
        user.userEarnings += 400

        user.save()
        LimitUserPay(request.user)

    elif str(user_membership.membership) == 'Silver':
        # print('pay Silver')
        user.userEarnings += 300
        LimitUserPay(request.user)

        user.save()
        LimitUserPay(request.user)


    elif str(user_membership.membership) == 'Bronze':
        # print('pay Bronze')
        user.userEarnings += 200
        user.save()

        LimitUserPay(request.user)



def object_viewed_reciver(sender,instance,request,*args,**kwargs):
    # print('wowo it WORKED MARKOTHEDEV',instance)

    # this line will check if the user has read the post if not
    # it will record that the user has read the post 
    'instance in this case actually contains the post that was opened data'
    userHasReadThePost,create = SeenMoneyPost.objects.get_or_create(user=request.user,postSeen=instance)

    if create == True:
        'check if created is false then we can pay users'
        paythisUser(request)
        

    # include a model that saves the user object and the post object
    # so we user get_or_create for validation

from .signals import object_viewed_signal 


object_viewed_signal.connect(object_viewed_reciver)