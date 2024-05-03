from collections import UserList

from django.urls import path, include
from registration.views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('oauth/', obtain_auth_token, name='obtain_auth_token'),

    path('user/', CustomUserCreate.as_view(), name='user-create'),
    path('user/<int:pk>/', CustomUserDetails.as_view(), name='user-details'),
    path('users/', CustomUserList.as_view(), name='user-list'),
    path('user/otp/<str:phone>', CustomUserOTP.as_view(), name='user-otp'),
    path('user/otp/auth/', CustomAuthToken.as_view(), name='custom-auth-token'),
    path('user/gft/', CustomUserGet.as_view(), name='get-user-by-token'),

    path('cities/', CityList.as_view(), name='city-list'),
    path('city/<int:pk>/', CityDetails.as_view(), name='city-details'),
    path('city/', CityCreate.as_view(), name='city-create'),

    path('provinces/', ProvinceList.as_view(), name='province-list'),
    path('province/<int:pk>/', ProvinceDetails.as_view(), name='province-details'),
    path('province/', ProvinceCreate.as_view(), name='province-create'),

    path('useraddresses/', UserAddressList.as_view(), name='user-address-list'),
    path('useraddresses/<int:pk>/', UserAddressDetails.as_view(), name='user-details'),
    path('useraddress/', UserAddressCreate.as_view(), name='user-address-create'),

    path('contact-us/', ContactUsCreate.as_view(), name='contact-us-create'),
    path('contact-us/<int:pk>/', ContactUsDetails.as_view(), name='contact-us-details'),
    path('contact-uss/', ContactUsList.as_view(), name='contact-us-list'),


    path('form/', RegistrationCreate.as_view(), name='register'),
    path('form/', RegistrationList.as_view(), name='register-list'),
    path('form/<int:pk>/', RegistrationDetails.as_view(), name='register-details'),
    

    path('passres/', PasswordResetCreate.as_view(), name='password-reset-create'),
    path('passres/<int:pk>/', PasswordResetDetails.as_view(), name='password-reset-details'),

    path('sponsors/', SponsorList.as_view(), name='sponsor-list'),
    path('sponsor/', SponsorCreate.as_view(), name='sponsor-create'),
    path('sponsors/<int:pk>/', SponsorDetails.as_view(), name='sponsor-details'),

    path('license/', LicenseDetails.as_view(), name='license-details')
]
