from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from .models import Todo
from .forms import RegistrationForm, TodoForm
from .serializers import todoerializer


# -------- AUTH VIEWS --------

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('todo_list')
    else:
        form = RegistrationForm()
    return render(request, 'todo/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('todo_list')
        else:
            return render(request, 'todo/login.html', {'error': 'Invalid credentials'})
    return render(request, 'todo/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


# -------- TODO VIEWS (MVT) --------

@login_required
def todo_list(request):
    # Admin sees all, Student sees only theirs
    if request.user.role == 'admin':
        todo = Todo.objects.all()
    else:
        todo = Todo.objects.filter(user=request.user)
    return render(request, 'todo/todo_list.html', {'todo': todo})

@login_required
def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todo/todo_form.html', {'form': form})

@login_required
def todo_update(request, pk):
    if request.user.role == 'admin':
        todo = get_object_or_404(Todo, pk=pk)
    else:
        todo = get_object_or_404(Todo, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = TodoForm(instance=todo)
    return render(request, 'todo/todo_form.html', {'form': form})

@login_required
def todo_delete(request, pk):
    if request.user.role == 'admin':
        todo = get_object_or_404(Todo, pk=pk)
    else:
        todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.delete()
    return redirect('todo_list')


# -------- API VIEWS (DRF) --------

class TodoListCreateAPI(generics.ListCreateAPIView):
    serializer_class = todoerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Todo.objects.all()
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TodoDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = todoerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Todo.objects.all()
        return Todo.objects.filter(user=self.request.user)