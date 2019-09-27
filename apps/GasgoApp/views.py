
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt
import json
from django.conf import settings # new
import stripe 
from django.shortcuts import render # new

import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyAbS5UsBI2fVZE5BS9IfCnHYF5YqtsT-ws')

# # Geocoding an address
# geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
print(reverse_geocode_result)



# Request directions via public transit
# now = datetime.now()
# directions_result = gmaps.directions("Sydney Town Hall",
#                                      "Parramatta, NSW",
#                                      mode="transit",
#                                      departure_time=now)









# from django.views.generic.base import TemplateView



# Filler.objects.all().delete()
# Driver.objects.all().delete()
# Order.objects.all().delete()
# Address.objects.all().delete()

def index(request):
        return render(request,"GasgoApp/index.html")

def preregisterF(request):
    # uid = request.session.get("userid")
    # if not uid:
    #     return redirect("/")

    return render(request,"GasgoApp/FillerReg.html")

def preregisterD(request):
    # uid = request.session.get("userid")
    # if not uid:
    #     return redirect("/")
    return render(request,"GasgoApp/DriverReg.html")


def preLoginF(request):
    # uid = request.session.get("userid")
    # if not uid:
    #     return redirect("/")
    return render(request,"GasgoApp/FillerLogin.html")

def preLoginD(request):
    # uid = request.session.get("userid")
    # if not uid:
    #     return redirect("/")
    return render(request,"GasgoApp/DriverLogin.html")



def registerD(request):
    errors = Driver.objects.driver_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/driverReg')
    else:
        password = request.POST['password']
        print(password)
        password_confirm = request.POST['password_confirm']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) 
        pw_hash_confirm = bcrypt.hashpw(password_confirm.encode(), bcrypt.gensalt()) 
        print(pw_hash)
        Driver.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=pw_hash, password_confirm=pw_hash_confirm, 
        email=request.POST['email'], birth_date=request.POST['birth_date']) 
        print("its working")
        thedriver = Driver.objects.filter(email=request.POST['email']) 
        if thedriver: 
            logged_driver = thedriver[0] 
            request.session['userid'] = logged_driver.id
            return redirect('/successDriver')

        return redirect("/successDriver")


def loginD(request):
    if not Driver.objects.loginValidDriver(request):
        print("hello this is not working rn ")
        return redirect('/driverReg')
    else:
        thedriver = Driver.objects.filter(email=request.POST['email']) 
        if thedriver: 
            logged_driver = thedriver[0] 
            request.session['userid'] = logged_driver.id
            return redirect('/successDriver')
        return redirect('/driverReg')


def registerF(request):
    errors = Filler.objects.filler_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/fillerReg')
    else:
        password = request.POST['password']
        print(password)
        password_confirm = request.POST['password_confirm']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) 
        pw_hash_confirm = bcrypt.hashpw(password_confirm.encode(), bcrypt.gensalt()) 
        print(pw_hash)
        Filler.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=pw_hash, password_confirm=pw_hash_confirm, 
        email=request.POST['email'], 
        car_make=request.POST['carMake'],
        car_year=request.POST['carYear'],
        car_color = request.POST['carColor'],
        car_model=request.POST['carModel'],
        plate=request.POST['plate'],
        birth_date=request.POST['birth_date']) 
        print("its working")
        thefiller = Filler.objects.filter(email=request.POST['email']) 
        if thefiller: 
            logged_filler = thefiller[0] 
            request.session['userid'] = logged_filler.id
        return redirect("/successFiller")


def loginF(request):
    if not Filler.objects.loginValidFiller(request):
        return redirect('/fillerLog')
    else:
        thefiller = Filler.objects.filter(email=request.POST['email']) 
        if thefiller: 
            logged_filler = thefiller[0] 
            request.session['userid'] = logged_filler.id
            return redirect('/successFiller')
        return redirect('/fillerLog')

def successDriver(request):
        uid = request.session.get("userid")
        if not uid:
            return redirect("/")
        driver = Driver.objects.get(id=uid)
        this_driver_orders= driver.order.all()
        order = Order.objects.all()
        this_driver_accepted_orders = this_driver_orders.exclude(accepted=False)
        this_driver_exclude_completed = this_driver_accepted_orders.exclude(completed=True)
        all_other_orders = order.filter(accepted=False)
        this_driver_historic_orders = this_driver_orders.exclude(completed=False)


        context = {
            "Order": order,
            "Driver": this_driver_accepted_orders,
            "DriverPending": this_driver_exclude_completed,
            "AllDrivers": all_other_orders,
            "History": this_driver_historic_orders,
            }
        return render(request,"GasgoApp/successDriver.html",context)
        # return redirect("/driverLog")

def successFiller(request):
    if request.session.get("userid"):
        context = {
            "unleaded": 2.99,
            "plus": 3.09,
            "premium": 3.19,
        }
        return render(request,"GasgoApp/successFiller.html", context)
    return redirect("/fillerLog")




def logout(request):
    del request.session['userid'] 
    return redirect("/")

################^^^^^^^^^^^THE ABOVE CODE IS FOR REGISTRATION AND LOGIN^^^^^^^^^^^^######################

def submitFillerFrom(request):
    # errors = Filler.objects.submittingFillerForm(request)
    # if len(errors) > 0:
    #     for key, value in errors.items():
    #         messages.error(request, value)
    #     return redirect('/successFiller')
    # else:
        if request.session.get("userid"):
            this_user_session_id= request.session.get("userid")
            # print(this_user_session_id)
            # print(Filler.objects.all().values())

            this_user_obj= Filler.objects.get(id= this_user_session_id)

            print(this_user_obj)
            # print(request.POST["Type"])

            newAddress = Address.objects.create(
            address1 = request.POST["address1"],
            address2 = request.POST["address2"],
            zip_code = request.POST["zip"],
            state = request.POST["state"],
            city = request.POST["city"],
            country = request.POST["country"],
            latitude = request.POST["lat"],
            longitude = request.POST["lng"],
            )
            print(newAddress)

            new_order = Order.objects.create(
            gallons = request.POST["Gallons"],
            type = request.POST["Type"],
            address = newAddress,
            price = request.POST["Type"],
            filler = this_user_obj,
            )
            print(new_order)
            return redirect ("/confirmation")
        return render(request,"GasgoApp/index.html")

def confirmation(request):
    if request.session.get("userid"):
        this_user_session_id= request.session.get("userid")
        this_user_obj= Filler.objects.get(id= this_user_session_id)
        this_order = Order.objects.filter(filler__id = this_user_obj.id)
        this_order1 = this_order.last()
        print(this_order1)
        Total = this_order1.price * this_order1.gallons
        context ={
            "Order": this_order1,
            "total":Total
        }
        return render(request,"GasgoApp/confirmation.html",context)
    return redirect("/fillerLog")

def get_context_data(self, **kwargs): # new
    context = super().get_context_data(**kwargs)
    context['key'] = settings.STRIPE_PUBLISHABLE_KEY
    return context

stripe.api_key = settings.STRIPE_SECRET_KEY 


def charge(request): # new
    if request.method == 'POST':
        print("this is going to the achagesf")
        charge = stripe.Charge.create(
            amount=500,
            currency='usd',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        print("KJHFKJNKJNINCNEOJ")
        return render(request, 'charge.html')

def checkout2(request): # new

        return render(request,"GasgoApp/charge.html")


def accepted(request,id):
    uid = request.session.get("userid")
    if not uid:
        return redirect("/")
    else:
        this_user_session_id= request.session.get("userid")
        driver = Driver.objects.get(id=this_user_session_id)
        print(this_user_session_id)
        update_item_obj= Order.objects.get(id= id)
        print(update_item_obj.id)
        update_item_obj.accepted = True
        update_item_obj.driver = driver
        update_item_obj.save()
        return redirect ("/successDriver")

    return render(request,"successDriver.html")



def completed(request,id):
    uid = request.session.get("userid")
    if not uid:
        return redirect("/")
    else:
        this_user_session_id= request.session.get("userid")
        driver = Driver.objects.get(id=this_user_session_id)
        print(this_user_session_id)
        update_item_obj= Order.objects.get(id= id)
        print(update_item_obj.id)
        update_item_obj.completed = True
        update_item_obj.driver = driver
        update_item_obj.save()
        return redirect ("/successDriver")
    return render(request,"successDriver.html")


def cancel(request,id):
    uid = request.session.get("userid")
    if not uid:
        return redirect("/")
    else:
        this_user_session_id= request.session.get("userid")
        print("HELLO")
        update_item_obj= Order.objects.get(id= id)
        print(update_item_obj.id)
        update_item_obj.accepted = False
        update_item_obj.save()
        return redirect ("/successDriver")

    return render(request,"successDriver.html")


            # this_user = User.objects.get(id=this_user_session_id)
            # print(this_user)
            # new_book_adding.users_who_fav.add(this_user)
            # return redirect ("/confirmation")


def viewPage(request,id):
    uid = request.session.get("userid")
    if not uid:
        return redirect("/")
    else:
        view = Order.objects.get(id= id)
        price = view.price
        gallons = view.gallons
        total =  price * gallons
        context = {
            "Order":view,
            "Total":total
        }
        return render(request,"GasgoApp/viewPage.html",context)

    return render(request,"successDriver.html")




def yourOrders(request):
        uid = request.session.get("userid")
        if not uid:
            return redirect("/")
        driver = Driver.objects.get(id=uid)
        this_driver_orders= driver.order.all()
        order = Order.objects.all()
        this_driver_accepted_orders = this_driver_orders.exclude(accepted=False)
        this_driver_exclude_completed = this_driver_accepted_orders.exclude(completed=True)
        all_other_orders = order.filter(accepted=False)
        this_driver_historic_orders = this_driver_orders.exclude(completed=False)
        context = {
            "Order": order,
            "Driver": this_driver_accepted_orders,
            "DriverPending": this_driver_exclude_completed,
            "AllDrivers": all_other_orders,
            "History": this_driver_historic_orders,
            }
        return render(request,"GasgoApp/yourOrders.html",context)
        # return redirect("/driverLog")



def History(request):
        uid = request.session.get("userid")
        if not uid:
            return redirect("/")
        driver = Driver.objects.get(id=uid)
        this_driver_orders= driver.order.all()
        order = Order.objects.all()
        this_driver_accepted_orders = this_driver_orders.exclude(accepted=False)
        this_driver_exclude_completed = this_driver_accepted_orders.exclude(completed=True)
        all_other_orders = order.filter(accepted=False)
        this_driver_historic_orders = this_driver_orders.exclude(completed=False)
        context = {
            "Order": order,
            "Driver": this_driver_accepted_orders,
            "DriverPending": this_driver_exclude_completed,
            "AllDrivers": all_other_orders,
            "History": this_driver_historic_orders,
            }
        return render(request,"GasgoApp/History.html",context)
        # return redirect("/driverLog")

