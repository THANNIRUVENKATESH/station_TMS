from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from .forms import UserRegistrationForm, TaskForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

# UI Views
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'tasks/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Remove the login part
            messages.success(request, 'Registration successful! Please login to continue.')
            return redirect('login')  # Redirect to login instead of dashboard
    else:
        form = UserRegistrationForm()
    return render(request, 'tasks/register.html', {'form': form})

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    context = {
        'tasks': tasks,
        'pending_tasks': tasks.filter(status='pending').count(),
        'completed_tasks': tasks.filter(status='completed').count(),
    }
    return render(request, 'tasks/dashboard.html', context)

@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    return redirect('login')

@require_http_methods(['GET', 'POST'])
def custom_logout(request):
    try:
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
    except Exception as e:
        messages.error(request, 'An error occurred during logout.')
    return redirect('login')

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('dashboard')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Create Task'
    })

@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'task': task,
        'title': 'Edit Task'
    })

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    messages.success(request, 'Task deleted successfully!')
    return redirect('dashboard')

# API Views
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)