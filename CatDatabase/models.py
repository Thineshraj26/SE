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

class Treatment(models.Model):
    TreatmentID = models.AutoField(primary_key=True)
    CatID = models.ForeignKey(Cat, on_delete=models.CASCADE, null=True, blank=True)
    TreatmentName = models.CharField(max_length=200)
    StartDate = models.DateField(blank=True)
    EndDate = models.DateField(blank=True)
    Description = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.TreatmentName)
    
class Appointment(models.Model):
    AppointmentID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(djangoUser, on_delete=models.CASCADE, null=True, blank=True)
    CatID = models.ForeignKey(Cat, on_delete=models.CASCADE, null=True, blank=True)
    Date = models.DateField(blank=True)
    Time = models.TimeField(blank=True)
    Reason = models.CharField(max_length=500)

    def __str__(self):
        return str(self.AppointmentID)

class Medication(models.Model):
    MedicationID = models.AutoField(primary_key=True)
    TreatmentID = models.ForeignKey(Treatment, on_delete=models.CASCADE, null=True, blank=True)
    MedicationName = models.CharField(max_length=200)
    Dosage = models.IntegerField()
    Frequency = models.IntegerField()
    Description = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.MedicationName)
    
class Report(models.Model):
    ReportID = models.AutoField(primary_key=True)
    CatID = models.ForeignKey(Cat, on_delete=models.CASCADE, null=True, blank=True)
    Date = models.DateField(blank=True)
    Details = models.CharField(max_length=1000)
    ReportType = models.CharField(max_length=100)