from django.db import models

# Create your models here.
# Trong file models.py
from django.contrib.auth.models import User

class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    # Thêm các trường khác nếu cần
