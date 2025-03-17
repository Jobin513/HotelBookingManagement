from django.shortcuts import render, redirect
from .forms import PaymentForm
from .models import Payment


def process_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payment_success')  # Redirect to a success page
    else:
        form = PaymentForm()

    return render(request, 'payments/payment_form.html', {'form': form})


def payment_success(request):
    return render(request, 'payments/payment_success.html')
