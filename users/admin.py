from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
# from django.contrib.admin import 


class UserAdmin(BaseUserAdmin):
    ordering = ('id',)
    list_display = ('id','email','userEarnings',)
    list_display_links = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('userPics','userEarnings','last_login')}),
        ('Permissions', {'fields': ('is_staff','is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2'),
        }),
    )



admin.site.register(models.User,UserAdmin)





admin.site.register(models.PayHistory)
admin.site.register(models.Membership)
admin.site.register(models.UserMembership)
admin.site.register(models.Subscription)

admin.site.register(models.MoneyPost)
admin.site.register(models.SeenMoneyPost)
admin.site.register(models.UserRequestPayment)