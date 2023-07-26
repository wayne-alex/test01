from django.db import models

# Create your models here.


class Account(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField()
    phone_number = models.IntegerField()
    verified = models.BooleanField(default=False)
