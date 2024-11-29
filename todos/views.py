from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import User, Todo

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

        # Create a new user
        User.objects.create(
            name=name, email=email, phone=phone, password=password,
            gender=gender, age=age, profession=profession
        )
        messages.success(request, "Registration successful! You can now log in.")
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
                messages.success(request, f"Welcome, {user.name}!")
                return redirect('todo_list')
            else:
                messages.error(request, 'Invalid password.')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')

    return render(request, 'base/login.html')

# Logout View
def logout(request):
    request.session.flush()
    messages.info(request, "You have been logged out.")
    return redirect('login')

# To-Do List View
def todo_list(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session['user_id']
    todos = Todo.objects.filter(user_id=user_id)

    # Display a message if there are no tasks
    no_items_message = "No tasks to show" if not todos else None

    return render(request, 'base/todo_list.html', {'todos': todos, 'no_items_message': no_items_message})


# Add Task View
def addTask(request):
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session['user_id']

    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        status = request.POST.get('status')
        completion_date = request.POST.get('completion_date') if status == 'Complete' else None

        # Check for duplicate tasks
        if Todo.objects.filter(title=title, user_id=user_id).exists():
            messages.warning(request, "This task is already in your list.")
            return redirect('addtask')

        # Create the task
        Todo.objects.create(
            title=title, desc=desc, status=status,
            completion_date=completion_date, user_id=user_id
        )
        messages.success(request, "Task added successfully!")
        return redirect('todo_list')

    return render(request, 'base/add_todo.html')


# Delete Task View
def delete_task(request, id):
    item = Todo.objects.get(id=id)             

    if request.method == "POST":
        if request.POST.get("confirm") == "Yes":
            item.delete()  
            return redirect('todo_list')
        return redirect('todo_list') 
    
    return render(request, 'base/delete_todo.html', {'item': item})

# Edit Task View
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