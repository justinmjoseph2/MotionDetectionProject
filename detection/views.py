from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import SubscriberForm

def home(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = SubscriberForm()
    return render(request, 'detection/home.html', {'form': form})
