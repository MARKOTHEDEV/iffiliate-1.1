from rest_framework.permissions import BasePermission
from users import models


class AvoidFreeUsers(BasePermission):


    def has_permission(self, request, view):
        "dont allow users with free memebership"
        currentUserMembership =  models.UserMembership.objects.get(user=request.user)
        membership = models.Membership.objects.get(slug ='Free')
        if membership.membership_type == currentUserMembership.membership.membership_type:
            'if the currentUserMembership is equak to free then we have to retun false'
            return False
        return True