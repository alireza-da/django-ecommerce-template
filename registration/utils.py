import os
import ghasedakpack

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from dotenv import load_dotenv

load_dotenv()


class MyFileStorage(FileSystemStorage):

    # This method is actually defined in Storage
    def get_available_name(self, name):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


def content_file_name(instance, filename):
    return '/'.join(['content/users', instance.email, filename])


def message_file_name(instance, filename):
    return '/'.join(['messages/users', instance.type, filename])


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class SMSGateway:
    """
    A class that handles sending sms messages
    """
    sms = ghasedakpack.Ghasedak(os.environ.get('SMS_API_KEY'))
    _instance = None
    template = "BazyshOauth"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SMSGateway, cls).__new__(cls)
        return cls._instance

    def send_sms(self, phone: str, message: str):
        """
        Send an SMS via Ghasedak API
        """
        return self.sms.send({'message': message,
                              'receptor': phone, 'linenumber': '10008566'})

    def send_verification_code(self, phone: str, code: str):
        return self.sms.verification({'receptor': phone,
                                      'type': '1', 'template': self.template, 'param1': code})
