from django.shortcuts import render

def home(request):
    return render(request, "event_app/index.html")
