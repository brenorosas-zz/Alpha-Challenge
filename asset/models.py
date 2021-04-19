from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Asset(models.Model):
    name = models.CharField(max_length = 255)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    update_time = models.IntegerField(default = 60)
    inferior_limit = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    upper_limit = models.DecimalField(max_digits=11, decimal_places=2, null=True)
    def __str__(self):
        return self.name