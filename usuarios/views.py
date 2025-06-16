from django.shortcuts import render
from rest_framework import generics
from .serializers import RegisterSerializer
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from django.shortcuts import render
    
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.generate_verification_code()

        print(f"[DEBUG] Código enviado a {user.email}: {user.verification_code}")

        send_mail(
            'Verificación de cuenta',
            f'Código: {user.verification_code}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

@method_decorator(csrf_exempt, name='dispatch')  # <- ESTE ES CLAVE
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            return Response({"detail": "Login exitoso"}, status=200)
        else:
            return Response({"detail": "Credenciales inválidas"}, status=401)

class VerifyCodeView(APIView):
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        try:
            user = CustomUser.objects.get(email=email)
            if user.verification_code == code:
                user.is_verified = True
                user.verification_code = ''
                user.save()
                return Response({"message": "Cuenta verificada correctamente."})
            else:
                return Response({"error": "Código incorrecto."}, status=400)
        except CustomUser.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=404)

def register_page(request):
    return render(request, 'register.html')


def verify_page(request):
    return render(request, 'verify.html')


def login_page(request):
    return render(request, 'login.html')


def dashboard_page(request):
    return render(request, 'dashboard.html')

def contacto_page(request):
    return render(request, 'contacto.html')

@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    return redirect('login')
# Create your views here.
