from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    """Definine una relación uno a muchos desde User a otro modelo (posiblemente llamado Task), de modo que un usuario puede tener 
    muchas tareas, pero cada tarea está asociada a un único usuario. Si el usuario es eliminado, todas sus tareas también serán eliminadas."""

    def __str__(self):
        return f"{self.title}... - by {self.user.username}"  # Este trozo de codigo nos permite poder obervar el titulo del lado de DjangoAdmin,como vista previa
