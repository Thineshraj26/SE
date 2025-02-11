"""
Definition of models.
"""

from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission

#sharing entity

class Item(models.Model):
    item_id = models.CharField(primary_key=True, max_length=10)
    item_name = models.TextField()
    item_description = models.TextField(null=True,default=None, blank=True)
    def __str__(self):
        return str(self.item_id)

# Built-in fields inherited from AbstractUser:
    # - username: CharField (max_length=150, unique=True) -> Required username field
    # - first_name: CharField (max_length=150, blank=True) -> User's first name (optional)
    # - last_name: CharField (max_length=150, blank=True) -> User's last name (optional)
    # - password: CharField (max_length=128) -> Hashed password storage
    # - is_staff: BooleanField (default=False) -> Determines if the user can access Django Admin
    # - is_active: BooleanField (default=True) -> Indicates if the account is active
    # - is_superuser: BooleanField (default=False) -> Grants all admin permissions
    # - date_joined: DateTimeField (auto_now_add=True) -> Stores account creation time
    # - last_login: DateTimeField (null=True, blank=True) -> Stores last login time
    # - groups: ManyToManyField (Group) -> User’s group memberships
    # - user_permissions: ManyToManyField (Permission) -> User-specific permissions
class Account(AbstractUser):

    RegistrationDate = models.DateField(auto_now_add=True)

    # These are to differentiate from the auth.User model
    groups = models.ManyToManyField(Group, related_name="account_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="account_users", blank=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def __str__(self):
        return self.get_full_name()
    
    def assign_group(self, role):
        dictRoleGroup = {
            'admin': 'Admin',
            'medical_staff': 'Medical Staff',
            'caretaker': 'Caretaker',
            'user': 'User',
        }

        groupName = dictRoleGroup.get(role)

        if groupName:
            # get_or_create() returns Group and Boolean
            # _ is to ignore the Boolean
            group, _ = Group.objects.get_or_create(name=groupName)
            # set() overwrites
            self.groups.set([group])
    
    class Meta:
        app_label = "app"

