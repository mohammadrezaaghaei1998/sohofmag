from django.shortcuts import render,redirect
from .forms import ContactUsForm
from django.contrib import messages
from django.http import JsonResponse
from .models import Map


# Create your views here.





def contact_us(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST) 
        if form.is_valid():
            form.save()  
            return JsonResponse({
                'status': 'success',
                'message': 'Your message has been sent successfully!'
            })
        else:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list
            return JsonResponse({
                'status': 'error',
                'errors': errors
            })
    else:
        form = ContactUsForm()  
        map_instance = Map.objects.first()
    return render(request, 'first/contactus.html', {'form': form , 'map_iframe': map_instance.iframe if map_instance else None})
