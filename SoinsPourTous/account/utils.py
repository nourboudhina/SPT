import datetime
from email.message import EmailMessage
from random import randint
import uuid
from django.http import JsonResponse
from rest_framework.response import Response
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.template import Context
from .models import Otp, PasswordResetToken, Token, TokenForAgent, TokenForDoctor
from SoinsPourTous.settings import TEMPLATES_BASE_URL
from rest_framework.permissions import BasePermission
from django.utils import timezone
from twilio.rest import Client # type: ignore



def send_otp(phone):
   
    otp = randint(1000, 9999)
    validity = datetime.datetime.now() + datetime.timedelta(minutes=10)

    Otp.objects.update_or_create(phone=phone, defaults={"otp": otp, "verified": False, "validity": validity})

    try:
        # Remplacez 'TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE_NUMBER' par vos informations Twilio
        client = Client('AC464d7d24b2008670153c4bf483e8be10', 'dd2fb47121741b1d0d17fc267009c4a5')
        message = client.messages.create(
            body=f"Votre code OTP est : {otp}",
            from_='+12513129402',
            to=phone
        )
        print("OTP sent successfully:", message.sid)
        
        response_data = {
            'message': 'OTP sent successfully',
            'phone': phone,
            # Ajoutez d'autres données si nécessaire
        }
        return JsonResponse(response_data)
    except Exception as e:
        print("Failed to send OTP:", str(e))
        return JsonResponse({'message': 'Failed to send OTP'}, status=500)
    

def new_token() : 
    token = uuid.uuid1().hex
    return token
def token_response(user):
    token = new_token()
    Token.objects.create(token=token, user=user) 
    response_data = {
        'message': 'login successful',
        'token': token,
        'username' : user.username,
        
    }
    print(token)

    return JsonResponse(response_data)


def token_response_doctor(user):
    token = new_token()
    TokenForDoctor.objects.create(token=token, user=user) 
    response_data = {
        'message': 'login successful',
        'token': token,
        'username' : user.username,
        
    }
    print(token)

    return JsonResponse(response_data)

def token_response_Agent(user):
    token = new_token()
    TokenForAgent.objects.create(token=token, user=user) 
    response_data = {
        'message': 'login successful for Agent',
        'token': token,
        'username' : user.username,
        
    }
    print(token)

    return JsonResponse(response_data)
from django.core.mail import send_mail

def send_password_reset_email(user):
    print(type(user))  # Vérifiez le type de l'objet user

    token = new_token()
    exp_time = timezone.now() + timezone.timedelta(minutes=10)
    print("gouni")
    PasswordResetToken.objects.update_or_create(user=user, defaults={'user': user, 'token': token, 'validity': exp_time})
    print("gouni")
    email_data = {
        'token': token,
        'email': user.email,
        'base_url': TEMPLATES_BASE_URL
    }

    email_template = get_template('emails/reset-password.html')
    message = email_template.render(email_data)

    subject = 'Reset Password'
    recipients = [user.email]

    try:
        send_mail(subject, message, from_email=None, recipient_list=recipients, html_message=message)
        return JsonResponse({'message': 'reset_password_email_sent'})
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")
        return JsonResponse({'error': 'Failed to send reset password email'}, status=500)
    
class IsAuthenticatedUser(BasePermission) :
    message = 'unauthenticated_user'

    def has_permission(self,request,view) : 
        return bool(request.user)
