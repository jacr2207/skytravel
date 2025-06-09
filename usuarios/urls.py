from django.urls import path
from .views import RegisterView, LoginView, VerifyCodeView, register_page, login_page, verify_page
from .views import dashboard_page
from .views import contacto_page

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('verificar/', VerifyCodeView.as_view()),
    path('registro/', register_page),
    path('login_html/', login_page),
    path('verificar_html/', verify_page),
    path('dashboard/', dashboard_page, name='dashboard_page'),
    path('contacto/', contacto_page, name='contacto'),
]