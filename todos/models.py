from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=14)
    password = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        default="Select",
    )
    age = models.PositiveIntegerField()
    profession = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.phone.startswith("+91-"):
            self.phone = f"+91-{self.phone}"
        super().save(*args, **kwargs)


class Todo(models.Model):
    title = models.CharField(max_length=250)
    desc = models.CharField(max_length=500)
    status = models.CharField(max_length=20)
    completion_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos', default=1)

    def __str__(self):
        return self.title
