from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Todo
from django.contrib import messages


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
    todos = Todo.objects.all()
    return render(request, 'base/todo_list.html', {'todos': todos})

# add todo
def addTask(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        status = request.POST.get('status')
        
        completion_date = request.POST.get('completion_date') if status == 'Complete' else None

        dropdown_submit = request.POST.get('dropdown_submit', False)

        if dropdown_submit:
            return render(request, 'add.html', {
                'task': {'title': title, 'desc': desc, 'status': status, 'completion_date': completion_date}
            })

        if not Todo.objects.filter(title=title).exists():
            todo = Todo(title=title, desc=desc, status=status, completion_date=completion_date)
            todo.save() 
            return redirect('todo_list')
        else:
            messages.warning(request, "This item is already in your list")
            return redirect('add')

    return render(request, 'base/add_todo.html')

# delete todo
def delete_task(request, id):
    item = Todo.objects.get(id=id)        

    if request.method == "POST":
        if request.POST.get("confirm") == "Yes":
            item.delete()  
            return redirect('todo_list')
        return redirect('todo_list') 
    
    return render(request, 'base/delete_todo.html', {'item': item})

# edit todo
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
            messages.success(request, 'Task updated successfully.')

        return render(request, 'base/edit_todo.html', {'task': task})

    return render(request, 'base/edit_todo.html', {'task': task})
