from email import message
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from employee.models import Employee, Invite, Notifications,User
from .serializers import NotificationSerializer, UserSerializer, EmployeeSerializer,UserSerializerWithToken
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from rest_framework import serializers, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import json,re
from django.core.mail import EmailMessage
from django.core.mail import send_mail
# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request,format=None):
    try:
        data = request.data
        if not data['name']:
            content = {'error': 'PLease provide a name'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        name = data['name']
        if not data['email']:
            content = {'error': 'PLease provide an email'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        email = data['email']
        if not data['password']:
            content = {'error': 'PLease provide a password'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        password=data['password']
        # if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email):
        #     content = {'error': 'Enter a valid email'}
        #     return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if len(password) < 5:
            content = {'error': 'Password needs to be at least of 5 char'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        password=make_password(password)
        employee = User.objects.create(name=name,email=email,password=password)
        serializer = UserSerializerWithToken(employee, many=False)
        return Response(serializer.data)
    except Exception as e:
        print(e)
        content = {'error': 'Employee with this email already exists'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt 
@api_view(['POST']) 
@permission_classes([AllowAny])
def signin(request):
    try:
        if not request.method == 'POST':
            content = {'error': ['Send a post request with valid paramenter only']}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        #used to accept json data
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        
        email = body['email']
        password = body['password']


    # validation part
        # if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email):
        #     content = {'error': 'Enter a valid email'}
        #     return Response(content, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 5:
            content = {'error': 'Password needs to be at least of 5 char'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        #getting user model from db
        UserModel = get_user_model()

        try:
            #getting the user data of the user trying to login
            user = UserModel.objects.get(email=email)
            #validating correct password and email
            if user.check_password(password):
                usr_dict = UserModel.objects.filter(
                    email=email).values().first()
                usr_dict.pop('password')
                #generating refresh token and access token

                login(request, user)
                serializer = UserSerializerWithToken(user, many=False)
                return Response(serializer.data)
            else:
                content = {'error':'Invalid password'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        except UserModel.DoesNotExist:
            content = {'error': 'Invalid Email'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        content = {'error': 'Email or password missing'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt 
@api_view(['POST']) 
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def add_employee_details(request):
    try:
        user = request.user
        first_name = request.POST.get('first_name',None)
        last_name = request.POST.get('last_name',None)
        email = request.POST.get('email',None)
        gender = request.POST.get('gender',None)
        age = request.POST.get('age',None)
        mobile_number = request.POST.get('mobile_number',None)
        address = request.POST.get('address',None)
        role = request.POST.get('role',None)
        bank_name = request.POST.get('bank_name',None)
        account_no = request.POST.get('account_no',None)
        ifsc_code = request.POST.get('ifsc_code',None)
        bank_branch_location = request.POST.get('bank_branch_location',None)
        aadhar_card = request.FILES.get('aadhar_card',None)
        pan_card = request.FILES.get('pan_card',None)
        passport = request.FILES.get('passport',None)
        driving_license = request.FILES.get('driving_license',None)
        if first_name is None:
            content = {'error': 'Please provide a first name'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if last_name is None:
            content = {'error': 'Please provide a last name'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if email is None:
            content = {'error': 'Please provide an email'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if gender is None:
            content = {'error': 'Please provide gender'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if age is None:
            content = {'error': 'Please provide age'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        age = eval(age)
        if age < 20:
            content = {'error': 'Age should be greater than 20'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if mobile_number is None:
            content = {'error': 'Please provide mobile number'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if address is None:
            content = {'error': 'Please provide address'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if role is None:
            content = {'error': 'Please provide a role'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if bank_name is None:
            content = {'error': 'Please provide bank name'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if account_no is None:
            content = {'error': 'Please provide account no'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if ifsc_code is None:
            content = {'error': 'Please provide ifsc code'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if bank_branch_location is None:
            content = {'error': 'Please provide bank branch location'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if aadhar_card is None:
            content = {'error': 'Please provide aadhar card'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            extension = aadhar_card.name.split(".")
            if not extension[-1] == 'pdf':
                content = {'error': 'Unsupported file type'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if pan_card is None:
            content = {'error': 'Please provide pan card'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            extension = pan_card.name.split(".")
            if not extension[-1] == 'pdf':
                content = {'error': 'Unsupported file type'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if passport is None:
            content = {'error': 'Please provide passport'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        else:
            extension = passport.name.split(".")
            if not extension[-1] == 'pdf':
                content = {'error': 'Unsupported file type'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        user_employee = Employee.objects.filter(email=user.email).first()
        if not user_employee:
            if not email == user.email:
                content = {'error': 'Please provide your details only'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        employee_details = Employee.objects.filter(email=email).first()
        if employee_details:
            content = {'error': 'Employee with this email already exists'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if not driving_license:
            employee_personal_details = Employee.objects.create(
                first_name=first_name,last_name=last_name,email=email,
                gender=gender,age=age,mobile_number=mobile_number,address=address,role=role,
                bank_name=bank_name,account_no=account_no,ifsc_code=ifsc_code,
                bank_branch_location=bank_branch_location,aadhar_card=aadhar_card,pan_card=pan_card,passport=passport)
        else:
            extension = driving_license.name.split(".")
            if not extension[-1] == 'pdf':
                content = {'error': 'Unsupported file type'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            employee_personal_details = Employee.objects.create(
                first_name=first_name,last_name=last_name,email=email,
                gender=gender,age=age,mobile_number=mobile_number,address=address,role=role,
                bank_name=bank_name,account_no=account_no,ifsc_code=ifsc_code,
                bank_branch_location=bank_branch_location,aadhar_card=aadhar_card,pan_card=pan_card,passport=passport,driving_license=driving_license)
        invited_employee = Invite.objects.filter(email=email).first()
        print(invited_employee)
        if invited_employee:
            if invited_employee.email == email:
                message = 'The employee with email '+str(email)+' you invited has registered'
                notification = Notifications.objects.create(message = message)
        return JsonResponse({'success':'Details added'})
    except Exception as e:
        print(e)
        content = {'error': 'Only pdf files allowed'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt 
@api_view(['GET']) 
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def getEmployees(request):
    employees = Employee.objects.all().order_by('id')
    serializer = EmployeeSerializer(employees,many=True)
    return Response({'employees':serializer.data})

@csrf_exempt 
@api_view(['GET']) 
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def getEmployee(request,pk):
    employee = Employee.objects.get(id=pk)
    serializer = EmployeeSerializer(employee,many=False)
    return Response({'employee':serializer.data})

@csrf_exempt 
@api_view(['PUT']) 
@permission_classes([IsAdminUser])
@authentication_classes([JWTAuthentication])
def updateEmployee(request,pk):
    first_name = request.POST.get('first_name',None)
    last_name = request.POST.get('last_name',None)
    email = request.POST.get('email',None)
    gender = request.POST.get('gender',None)
    age = request.POST.get('age',None)
    mobile_number = request.POST.get('mobile_number',None)
    address = request.POST.get('address',None)
    role = request.POST.get('role',None)
    bank_name = request.POST.get('bank_name',None)
    account_no = request.POST.get('account_no',None)
    ifsc_code = request.POST.get('ifsc_code',None)
    bank_branch_location = request.POST.get('bank_branch_location',None)
    if first_name is None:
        content = {'error': 'Please provide a first name'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if last_name is None:
        content = {'error': 'Please provide a last name'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if email is None:
        content = {'error': 'Please provide an email'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if gender is None:
        content = {'error': 'Please provide gender'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if age is None:
        content = {'error': 'Please provide age'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    age = eval(age)
    if age < 20:
        content = {'error': 'Age should be greater than 20'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if mobile_number is None:
        content = {'error': 'Please provide mobile number'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if address is None:
        content = {'error': 'Please provide address'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if role is None:
        content = {'error': 'Please provide a role'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if bank_name is None:
        content = {'error': 'Please provide bank name'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if account_no is None:
        content = {'error': 'Please provide account no'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if ifsc_code is None:
        content = {'error': 'Please provide ifsc code'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    if bank_branch_location is None:
        content = {'error': 'Please provide bank branch location'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)   
    employee_details = Employee.objects.filter(email=email).first()
    if employee_details:
        if email != employee_details.email:
            content = {'error': 'Employee with this email already exists'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    employee = Employee.objects.get(id=pk)
    employee.first_name = first_name
    employee.last_name = last_name
    employee.email = email
    employee.gender = gender
    employee.age = age
    employee.mobile_number = mobile_number
    employee.address = address
    employee.role = role
    employee.bank_name = bank_name
    employee.account_no = account_no
    employee.ifsc_code = ifsc_code
    employee.bank_branch_location = bank_branch_location
    employee.save()
    serializer = EmployeeSerializer(employee,many=False)
    return Response({'success':'Employee details were updated'})


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def updateDocuments(request, pk):
    aadhar_card = request.FILES.get('aadhar_card',None)
    pan_card = request.FILES.get('pan_card',None)
    passport = request.FILES.get('passport',None)
    driving_license = request.FILES.get('driving_license',None)
    employee = Employee.objects.get(id=pk)
    if aadhar_card is not None:
        extension = aadhar_card.name.split(".")
        if not extension[-1] == 'pdf':
            content = {'error': 'Unsupported file type'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        employee.aadhar_card = aadhar_card
    if pan_card is not None:
        extension = pan_card.name.split(".")
        if not extension[-1] == 'pdf':
            content = {'error': 'Unsupported file type'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        employee.pan_card = pan_card
    if passport is not None:
        extension = passport.name.split(".")
        if not extension[-1] == 'pdf':
            content = {'error': 'Unsupported file type'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        employee.passport = passport
    if driving_license is not None:
        extension = driving_license.name.split(".")
        if not extension[-1] == 'pdf':
            content = {'error': 'Unsupported file type'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        employee.driving_license = driving_license
    employee.save()
    return Response({'success':'Employee documents were updated'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def deleteEmployee(request, pk):
    employeeForDeletion = Employee.objects.get(id=pk)
    employeeForDeletion.delete()
    return Response({'success':'Employee was deleted'})


@api_view(['POST'])
@permission_classes([IsAdminUser])
@authentication_classes([JWTAuthentication])
def invite(request):
    email = request.POST.get('email',None)
    if email is None:
        content = {'error': 'Please provide an email'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    invited_email = email
    user = request.user
    subject = 'You are invite to regsiter yourself'
    email = [email]
    print(email)
    body = 'From '+ str(user.email) +"\n" + 'We have invited you to signup on our platform and register your details on' +'\n' +'http://127.0.0.1:3000/signup/'
    
    try:
        send_mail(subject,
        body,
        'testcrinitis@gmail.com',
        email,
        fail_silently=False)
    except:
        content = {'error': 'Email not valid'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    invite = Invite(email=invited_email)
    invite.save()
    return Response({'success':'Email was sent'})


@api_view(['GET'])
@permission_classes([IsAdminUser])
@authentication_classes([JWTAuthentication])
def getNotifications(request):
    notifications = Notifications.objects.filter(is_read=False)
    serializer = NotificationSerializer(notifications, many=True)
    return Response({'notifications':serializer.data})

@api_view(['GET'])
@permission_classes([IsAdminUser])
@authentication_classes([JWTAuthentication])
def readNotification(request,pk):
    notification = Notifications.objects.get(id=pk)
    notification.is_read = True
    notification.save()
    notifications = Notifications.objects.filter(is_read=False)
    serializer = NotificationSerializer(notifications, many=True)
    return Response({'notifications':serializer.data})



# @csrf_exempt 
# @api_view(['POST']) 
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
# def add_bank_details(request):
#     body_unicode = request.body.decode('utf-8')
#     body = json.loads(body_unicode)
#     try:
#         employee = request.user
#         bank_name = body['bank_name']
#         account_no = body['account_no']
#         ifsc_code = body['ifsc_code']
#         branch_location = body['branch_location']
#         search_employee = Employee.objects.filter(email=employee.email).first()
#         employee_details = Employee_Personal_Details.objects.filter(email=employee.email).first()
#         if employee_details:
#             content = {'error': 'Employee personal details of this employee already exists'}
#             return Response(content, status=status.HTTP_400_BAD_REQUEST)
#         if search_employee is not None:
#             employee = search_employee
#             employee_bank_details = Employee_Personal_Details.objects.create(bank_name=bank_name,account_no=account_no,ifsc_code=ifsc_code,branch_location=branch_location,employee=employee)
#         else:
#             employee_bank_details = Employee_Personal_Details.objects.create(bank_name=bank_name,account_no=account_no,ifsc_code=ifsc_code,branch_location=branch_location)
#         return JsonResponse({'success':'Details added'})
#     except Exception as e:
#         content = {'error': e}
#         return Response(content, status=status.HTTP_400_BAD_REQUEST)
