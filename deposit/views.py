from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Deposit
# Create your views here.



def deposit_view(request):
    if request.method == 'POST':
        form = Deposit(request.POST)
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user
            deposit.save()
            # Xử lý logic nạp tiền (cập nhật số dư, gửi thông báo, ...)
            return redirect('success_page')  # Chuyển hướng sau khi nạp tiền thành công
    else:
        form = Deposit()
    return render(request, 'deposit/deposit.html', {'form': form})
