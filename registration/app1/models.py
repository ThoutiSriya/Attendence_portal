from django.db import models

# Create your models here.
class stu(models.Model):
    name = models.TextField(max_length=50, null=True)
    email = models.EmailField()
    pass1 = models.TextField(max_length=50, null=True)
    ids = models.TextField(max_length=50, null=True)
    type1 = models.TextField(max_length=50, null=True)
    def __str__(self):
        return self.name

class fac(models.Model):
    name = models.TextField(max_length=50, null=True)
    email = models.EmailField()
    pass1 = models.TextField(max_length=50, null=True)
    type1 = models.TextField(max_length=50, null=True)
    def __str__(self):
        return self.name
    
class attendence(models.Model):
    ids = models.TextField(max_length=50, null=True)
    date = models.DateField(null = True)
    ftime = models.TimeField(null = True)
    stime = models.TimeField(null = True)
    cnt = models.TextField(default=0,max_length=50, null=True)
    status = models.TextField(default="no",max_length=50, null=True)
    def __str__(self):
        return self.ids

