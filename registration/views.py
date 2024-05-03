from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from shop.permissions import IsOwnerOrReadOnly
from .models import *
from .serializers import *
from .utils import SMSGateway


class CustomUserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    # parser_classes = (MultiPartParser, FormParser)


@permission_classes((AllowAny,))
class CustomUserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    # parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    # parser_classes = (MultiPartParser, FormParser)

    def delete(self, request, *args, **kwargs):
        user = self.queryset.get(id=kwargs['pk'])
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data=f"{user} has been deleted")

    def put(self, request, *args, **kwargs):
        if request.user.is_staff or request.user.id == self.get_object().id:
            return self.update(request, args, kwargs)


class CustomUserGet(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(key=request.headers['Authorization'].split("Token ")[1])
            serializer = CustomUserSerializer(token.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(data={"Not Found"}, status=status.HTTP_404_NOT_FOUND)


class CustomUserOTP(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = []

    def get(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(phone=kwargs['phone'])
            user.otp = user.generate_otp()
            user.verified_otp = False
            user.save()
            # sms_status = SMSGateway().send_sms(user.phone, user.otp)
            verification_sms_status = SMSGateway().send_verification_code(user.phone, user.otp)
            # print(sms_status, verification_sms_status)
            return Response(data=f"OTP STATUS: {verification_sms_status}", status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(data="Phone does not exist", status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response(data="Provide phone number", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(data="Something went wrong", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        try:
            otp = request.data['otp']
            user = CustomUser.objects.get(otp=otp, phone=request.data['phone'])
            user.verified_otp = True
            user.otp = user.generate_otp()
            serialized_user = CustomUserSerializer(user, context={'request': request})
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={
                'token': token.key,
                'user': serialized_user.data
            }, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
                return Response({"error": "Wrong OTP"}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
                return Response({"error": "Request body is incomplete. Phone & OTP required"},
                                status=status.HTTP_400_BAD_REQUEST)


# Address
class UserAddressDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class UserAddressList(generics.ListAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        try:
            if request.user:
                addresses = UserAddress.objects.filter(user=request.user)
                serializer = UserAddressSerializer(addresses, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(data={"error": "Could not find user"}, status=status.HTTP_404_NOT_FOUND)
        except UserAddress.DoesNotExist:
            return Response(data={"error": "Address not found for user"}, status=status.HTTP_404_NOT_FOUND)

class UserAddressCreate(generics.CreateAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = UserAddressSerializer
    permission_classes = [IsAuthenticated]


# Contact Us
class ContactUsCreate(generics.CreateAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = []


class ContactUsList(generics.ListAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [IsAdminUser]


class ContactUsDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer
    permission_classes = [IsAdminUser]


# City
class CityList(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = []


class CityCreate(generics.CreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdminUser]


class CityDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdminUser]


# Province
class ProvinceList(generics.ListAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes = []


class ProvinceCreate(generics.CreateAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes = [IsAdminUser]


class ProvinceDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes = []


# Registration Form
class RegistrationList(generics.ListAPIView):
    queryset = RegistrationForm.objects.all()
    serializer_class = RegistrationFormSerializer
    permission_classes = [IsAdminUser]


class RegistrationCreate(generics.CreateAPIView):
    queryset = RegistrationForm.objects.all()
    serializer_class = RegistrationFormSerializer
    permission_classes = [IsAuthenticated]


class RegistrationDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = RegistrationForm.objects.all()
    serializer_class = RegistrationFormSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


# Password Reset
class PasswordResetCreate(generics.CreateAPIView):
    queryset = PasswordReset.objects.all()
    serializer_class = PasswordResetSerializer
    permission_classes = [IsAuthenticated]


class PasswordResetDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = PasswordReset.objects.all()
    serializer_class = PasswordResetSerializer
    permission_classes = [IsAuthenticated]


class SponsorCreate(generics.CreateAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)


class SponsorDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)


class SponsorList(generics.ListAPIView):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = []


class LicenseDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = License.objects.all()
    serializer_class = LicenseSerializer
    permission_classes = []

    def get(self, request, *args, **kwargs):
        if 'license_id' in request.data:
            license = License.objects.get(license_id=request.data['license_id'])
            return Response(LicenseSerializer(license).data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        if 'license_id' in request.data:
            license = License.objects.get(license_id=request.data['license_id'])
            license.hwid = request.data['hwid']
            license.save()
            return Response(license.license_id, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
