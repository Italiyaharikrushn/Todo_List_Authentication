from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Todo

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = make_password(request.POST['password'])
        gender = request.POST['gender']
        age = request.POST['age']
        profession = request.POST['profession']

        User.objects.create(
            name=name, email=email, phone=phone, password=password,
            gender=gender, age=age, profession=profession
        )
        return redirect('login')

    return render(request, 'base/register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.get(email=email)
        if check_password(password, user.password):
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            return redirect('todo_list')

    return render(request, 'base/login.html')

def logout(request):
    request.session.flush()
    return redirect('login')

def todo_list(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session['user_id']
    todos = Todo.objects.filter(user_id=user_id)

    return render(request, 'base/todo_list.html', {'todos': todos})

def addTask(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session['user_id']

    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        status = request.POST.get('status')
        completion_date = request.POST.get('completion_date') if status == 'Complete' else None
        dropdown_submit = request.POST.get('dropdown_submit', False)
        if dropdown_submit:
            return render(request, 'base/add_todo.html', {
                'task': {'title': title, 'desc': desc, 'status': status, 'completion_date': completion_date}
            })
        if Todo.objects.filter(title=title, user_id=user_id).exists():
            return redirect('addtask')

        Todo.objects.create(
            title=title, desc=desc, status=status,
            completion_date=completion_date, user_id=user_id
        )
        return redirect('todo_list')

    return render(request, 'base/add_todo.html')

def delete_task(request, id):
    item = Todo.objects.get(id=id)             

    if request.method == "POST":
        if request.POST.get("confirm") == "Yes":
            item.delete()  
            return redirect('todo_list')
        return redirect('todo_list') 

    return render(request, 'base/delete_todo.html', {'item': item})

def editTask(request, id):
    task = Todo.objects.get(id=id)

    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        status = request.POST.get('status')
        completion_date = request.POST.get('completion_date')

        dropdown_submit = request.POST.get('dropdown_submit', False)

        task.title = title
        task.desc = desc
        task.status = status

        if status == 'Complete':
            task.completion_date = completion_date or task.completion_date
        else:
            task.completion_date = None

        if not dropdown_submit:
            task.save()

        return render(request, 'base/edit_todo.html', {'task': task})

    return render(request, 'base/edit_todo.html', {'task': task})