from django.db import models
from django.contrib.auth import get_user_model

djangoUser = get_user_model();  

# Create your models here.
class Cat(models.Model):
    CatID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(djangoUser, on_delete=models.CASCADE, null=True, blank=True)
    Name = models.CharField(max_length=50)
    Breed = models.CharField(max_length=50)
    Age = models.IntegerField()
    Gender = models.CharField(max_length=1)
    Description = models.CharField(max_length=500)

    def __str__(self):
        return str(self.Name)