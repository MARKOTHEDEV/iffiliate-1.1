from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model,login
from users import models


class UserSerializers(serializers.ModelSerializer):

    def create(self,validated_data):
        'since we using a custom User Model we will use our custom user create_user method'
        # so we sezed this oppputurnity to create a usermembership
        user = get_user_model().objects.create_user(**validated_data)
        Freesub = models.Membership.objects.get(membership_type='Free')
        user_membership = models.UserMembership.objects.create(user=user,membership=Freesub)

        return user
    class Meta:
        model = get_user_model()
        fields =['email','password']
        extra_kwargs = {'password':{'style':{'input_type':'password'},'write_only':True}}


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace =True)

    
    
  