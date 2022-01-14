from django.contrib import admin

from employee.models import Invite, Notifications, User,Employee

# Register your models here.
admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Invite)
admin.site.register(Notifications)
