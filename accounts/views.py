from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from cars.models import Car
from deposit.models import Deposit
from django.contrib.auth.decorators import login_required
from django.core.signing import Signer

# Create your views here.   

def login(request):
    remember = False
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        remember = request.POST.get('remember', False)
        
        print("Remember:", remember)
        
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            
            if remember:
                # Set cookies for username and password
                response = redirect('home')
                response.set_cookie("remember", remember, max_age=60 * 60 * 500, httponly=False)
                response.set_cookie("username", username, max_age=60 * 60 * 500, httponly=False)
                response.set_cookie("password", password, max_age=60 * 60 * 500, httponly=True)

                return response
            
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    
    remember_cookie = request.COOKIES.get('remember', False)
    if remember_cookie:
        username_cookie = request.COOKIES.get('username', "")
        password_cookie = request.COOKIES.get('password', "")
        return render(request, 'accounts/login.html', {'username': username_cookie, 'password': password_cookie})

    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password)
                    #auth.login(request, user)
                    #messages.success(request, 'You are now logged in.')
                    #return redirect('dashboard')
                    user.save()
                    messages.success(request, 'You are registered successfully.')
                    return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


@login_required(login_url = 'login')
def dashboard(request):
    user_inquiry = Contact.objects.order_by('-create_date').filter(user_id=request.user.id)
    
    car_details = []
    deposit_amounts = []

    for inquiry in user_inquiry:
        car_id = inquiry.car_id
        car = Car.objects.get(id=car_id)
        car_details.append(car)

        deposit_amount = car.price * 0.2
        deposit_amounts.append({
            'car_id': car_id,
            'amount': deposit_amount
        })
    
    data = {
        'inquiries': user_inquiry,
        'car_details': car_details,
        'deposit_amounts': deposit_amounts,
    }
    return render(request, 'accounts/dashboard.html', data)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return redirect('home')


def deposit_submit(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        car_id = request.POST['car_id']
        car_title = request.POST['car_title']
        email = request.POST['email']
        phone = request.POST['phone']
        payment_method = request.POST['payment_method']
        deposit_amount = request.POST['deposit_amount']

        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Deposit.objects.filter(car_id=car_id, user_id=user_id).exists()
            if has_contacted:
                messages.error(request, 'You have already made an deposit about this car. Please wait until we get back to you.')
                return redirect('dashboard')

        # Get the first superuser or handle the case where there is no superuser
        try:
            admin_info = User.objects.filter(is_superuser=True).first()
            if admin_info is None:
                raise User.DoesNotExist("No superuser found.")
        except User.DoesNotExist:
            messages.error(request, 'Error: No superuser found to receive the deposit.')
            return redirect('dashboard')
        
        contact = Contact.objects.get(user_id=user_id, car_id=car_id)
        contact.is_deposited = True
        contact.save()
        
        deposit = Deposit(car_id = car_id, car_title = car_title, user_id = user_id, email = email, phone = phone, payment_method = payment_method, deposit_amount = deposit_amount)
        deposit.save()
        messages.success(request, 'Your request has been submitted; we will get back to you shortly.')
        return redirect('dashboard')

    