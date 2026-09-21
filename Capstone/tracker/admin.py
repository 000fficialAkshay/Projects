from django.contrib import admin
from .models import Course, Part, Task, DailyTask, User

# Admin - GOD Password - GOD_1
# Register your models here.
admin.site.register(Course)
admin.site.register(Part)
admin.site.register(Task)
admin.site.register(DailyTask)
admin.site.register(User)