from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def page_404(request):
    return render(request, '404.html')

def page_403(request):
    return render(request, '403.html')