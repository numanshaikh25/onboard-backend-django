from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.signup,name='signup'),
    path('login/',views.signin,name='signin'),
    path('adddetails/',views.add_employee_details,name='add_employee_details'),
    path('getemployees/',views.getEmployees,name='getEmployees'),
    path('invite/',views.invite,name='invite'),
    path('getnotifications/',views.getNotifications,name='getNotifications'),
    path('readnotifications/<int:pk>/',views.readNotification,name='readNotification'),
    path('getemployee/<int:pk>/',views.getEmployee,name='getEmployee'),
    path('updateemployee/<int:pk>/',views.updateEmployee,name='updateEmployee'),
    path('updateemployeedocuments/<int:pk>/',views.updateDocuments,name='updateDocuments'),
    path('deleteemployee/<int:pk>/',views.deleteEmployee,name='deleteEmployee'),
    # path('addbankdetails/',views.add_bank_details,name='add_bank_details'),
]
