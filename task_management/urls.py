from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from tasks import views as task_views  # Change this line
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # UI Routes
    path('', task_views.home, name='home'),  # Use task_views instead of views
    path('dashboard/', task_views.dashboard, name='dashboard'),
    path('register/', task_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='tasks/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('task/create/', task_views.create_task, name='create_task'),
    path('task/edit/<int:pk>/', task_views.edit_task, name='edit_task'),
    path('task/delete/<int:pk>/', task_views.delete_task, name='delete_task'),
    
    # API Routes - Include the tasks.urls
    path('api/', include('tasks.urls')),
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)