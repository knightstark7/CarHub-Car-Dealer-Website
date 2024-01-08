from django.db import models

class Deposit(models.Model):
    car_id = models.IntegerField(default=0)
    car_title = models.CharField(default='', max_length=100)
    user_id = models.IntegerField(blank=True, default=0)  # Adding default value for user_id
    payment_method = models.CharField(default='', max_length=100)
    email = models.EmailField(default='', max_length=100)
    phone = models.CharField(default='', max_length=100)
    deposit_amount = models.FloatField(default=0)
    message = models.TextField(blank=True)

    def __str__(self):
        return self.email
