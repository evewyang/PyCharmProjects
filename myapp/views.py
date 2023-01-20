import folium
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from myapp import support_functions
from myapp.models import Currency, AccountHolder


# Create your views here.
def home(request):
    data = dict()
    import datetime
    xy = 1000
    data['time'] = datetime.datetime.now()
    data['xy'] = xy
    return render(request, "home.html", context=data)


def maintenance(request):
    data = dict()
    choice = "NONE"
    try:
        choice = request.GET['selection']
        if choice == "currencies":
            support_functions.add_currencies(support_functions.get_currency_list())
            c_list = Currency.objects.all()
            print("Got c_list", len(c_list))
            data['currencies'] = c_list
            return HttpResponseRedirect(reverse('currencies'))
    except:
        pass
    return render(request, "maintenance.html", context=data)


def view_currencies(request):
    data = dict()
    c_list = Currency.objects.all()
    data['currencies'] = c_list
    return render(request, 'currencies.html', context=data)


def currency_selection(request):
    data = dict()
    currencies =Currency.objects.all()
    data['currencies'] = currencies
    return render(request, "currency_selector.html", data)


def exch_rate(request):
    data = dict()
    try:
        currency1 = request.GET['currency_from']
        currency2 = request.GET['currency_to']
        c1 = Currency.objects.get(iso=currency1)
        c2 = Currency.objects.get(iso=currency2)
        support_functions.update_xrates(c1)
        data['currency1'] = c1
        data['currency2'] = c2
        try:
            user = request.user
            if user.is_authenticated:
                account_holder = AccountHolder.objects.get(user=user)
                account_holder.currencies_visited.add(c1)
                account_holder.currencies_visited.add(c2)
                data['currencies_visited'] = account_holder.currencies_visited.all()
        except:
            pass
        try:
            rate = c1.rates_set.get(x_currency=c2.iso).rate
            data['rate'] = rate
        except:
            data['rate'] = "Not Available"
    except:
        pass
    return render(request, "exchange_detail.html", data)


def register_new_user(request):
    context = dict()
    form = UserCreationForm(request.POST)
    if form.is_valid():
        new_user = form.save()
        dob = request.POST["dob"]
        acct_holder = AccountHolder(user=new_user, date_of_birth=dob)
        acct_holder.save()
        return render(request, "home.html", context=dict())
    else:
        form = UserCreationForm()
        context['form'] = form
    return render(request, "registration/register.html", context)


def map(request):
    m = folium.Map()
    m = m._repr_html_
    data = dict()
    data['m'] = m
    # convert the map object into a html string
    return render(request, "map.html", context=data)

