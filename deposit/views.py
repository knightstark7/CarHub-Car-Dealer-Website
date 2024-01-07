from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Deposit
from django.shortcuts import get_object_or_404, redirect
from contacts.models import Contact
# Create your views here.



def deposit_view(request):
    
    if request.method == 'POST':
        form = Deposit(request.POST)
        contact = get_object_or_404(Contact, pk=contact_id)
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user
            deposit.save()
            # Set is_deposited to True
            contact.is_deposited = True
            contact.save()
            return redirect('success_page')  
    else:
        form = Deposit()
    return render(request, 'deposit/deposit.html', {'form': form})
