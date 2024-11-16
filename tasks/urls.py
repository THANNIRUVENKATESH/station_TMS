from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='task')

urlpatterns = [
    path('register/', views.register_user, name='api_register'),
    path('login/', views.login_user, name='api_login'),
] + router.urls