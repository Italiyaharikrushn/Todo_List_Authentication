from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import User

# Registration View
def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = make_password(request.POST['password'])
        gender = request.POST['gender']
        age = request.POST['age']
        profession = request.POST['profession']

        if User.objects.filter(email=email).exists():
            return render(request, 'base/register.html', {'error': 'Email is already registered!'})

        User.objects.create(
            name=name, email=email, phone=phone, password=password,
            gender=gender, age=age, profession=profession
        )
        return redirect('login')

    return render(request, 'base/register.html')

# Login View
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('todo_list')
            else:
                return render(request, 'base/login.html', {'error': 'Invalid credentials!'})
        except User.DoesNotExist:
            return render(request, 'base/login.html', {'error': 'User does not exist!'})

    return render(request, 'base/login.html')

def logout(request):
    request.session.flush()
    return redirect('login')

def todo_list(request):
    todos = []
    return render(request, 'base/todo_list.html', {'todos': todos})
