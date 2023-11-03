from django.contrib import admin
from .models import Task
# Register your models here.

class TaskAdmin(admin.ModelAdmin):#Permite ver la fecha y hora de la creación desde el DjngAdm, no es editable...
    readonly_fields = ('created',)

admin.site.register(Task, TaskAdmin)
