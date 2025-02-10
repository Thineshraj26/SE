"""
Definition of models.
"""

from django.db import models

from django.contrib.auth.models import User

#sharing entity

class Item(models.Model):
    item_id = models.CharField(primary_key=True, max_length=10)
    item_name = models.TextField()
    item_description = models.TextField(null=True,default=None, blank=True)
    def __str__(self):
        return str(self.item_id)

class Account(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=20)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.name