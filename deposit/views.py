from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from deposit.models import Deposit
from cars.models import Car
from django.contrib.auth.decorators import login_required
from django.core.signing import Signer


def deposit_view(request):
    user_deposits = Deposit.objects.filter(user_id=request.user.id)
    
    car_details = []

    for deposit in user_deposits:
        car_id = deposit.car_id
        car = Car.objects.get(id=car_id)
        car_details.append(car)
    
    data = {
        'deposits': user_deposits,
        'car_details': car_details,
    }
    return render(request, 'deposit/deposit.html', data)
