from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import stu
from .models import fac
from .models import attendence

admin.site.register(stu)
admin.site.register(fac)
admin.site.register(attendence)

