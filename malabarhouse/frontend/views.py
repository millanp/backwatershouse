from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
# from django.http.response import HttpResponse

# Create your views here.
@login_required
def home(request):
    return render(request, "frontend/home.html", {})
    return HttpResponse("OOKLE")