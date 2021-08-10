from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=1000,null=True)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name or self.email



class Blog(models.Model):
    author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    contentImage = models.ImageField(upload_to='iffliateLanding_page/Blog/%m/%d/',null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)


    @property
    def introContent(self):
        'this method takes word from content content-- this is what the user sees before he clicks'
        return f'{self.content[:100]}.......'


    def __str__(self):
        return f'{self.title} by {self.author}'

        