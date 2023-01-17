from django.shortcuts import render

# Create your views here.
def home(request):
    data = dict()
    import datetime
    xy = 1000
    data['time'] = datetime.datetime.now()
    data['xy'] = xy
    return render(request, "home.html", context=data)
