from datetime import date
from BusDepoManagement import settings
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from Bus.models import Bus
from Bus.models import BookBus
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import razorpay
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

def homePage(request):
    
    return render(request,'templates/landingpage.html')

def contactPage(request):
    
    return render(request,'templates/contactus.html')

def aboutPage(request):
    
    return render(request,'templates/about.html')

def loginPage(request):

    if request.method == "POST":
        success = True
        if request.POST['username']=="":
            messages.error(request,"please fill empty field.")
            return render(request,"loginPage.html",{'error':True})
            
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username,password=pass1)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Bad Credentials")
            return redirect('loginPage')
            
    return render(request,'templates/loginPage.html')

def registrationPage(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            # messages.warning(request, "Username already exist! Please try some other username.")
            messages.error(request,"Username already exist! Please try some other username.")
            return redirect('registrationPage')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('registrationPage')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('registrationPage')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('registrationPage')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('registrationPage')

        newUser = User.objects.create_user(username,email,pass1)
        newUser.first_name = fname
        newUser.last_name = lname

        newUser.save()

        messages.success(request,"Your account has been successfully created")

        return redirect('loginPage')

    return render(request,'registrationPage.html')

def dashboard(request):
    return render(request,'dashboard.html')

def signOut(request):

    logout(request)
    return redirect('home')


# bus timetable 

def timeTablePage(request):
    busData = Bus.objects.all().order_by('arrival')
    # we can use order-by to order the data , - is used to arrange in reverse order
    # to limit the data we can simply use slice technique like [0:10]
    if request.method=="GET":
        source = request.GET.get('Source')
        destination = request.GET.get('Destination')
        if source!=None or destination!=None:
            busData = Bus.objects.filter(Q(source=source) | Q(destination=destination))
            print(busData)
    data={
        'busData':busData
    }
    return render(request,'timeTable.html',data)


# Booking 
@login_required(redirect_field_name='timeTablePage', login_url='/loginPage/')
def showBookPage(request,id):
    bus = Bus.objects.get(pk=id)

    if request.method == "POST":
        bus_source = request.POST['source']
        bus_destination = request.POST['destination']
        bus_arrival = request.POST['time']
        date = request.POST['date']
        seats = request.POST['seats']
        amount = bus.fare * float(seats)
        amount = amount*100

        # RazorPay
        client = razorpay.Client(auth=('rzp_test_DgmIs9k3dQ2Dfi','nAOhLmQG2UFgNhaWjSMatlhJ'))
        data = {
            'amount' : amount,
            'currency' : "INR",
            'receipt': "Book Ticket",
            'notes': {
                'name': request.user.username,
                'payment_for': "Seat Booking",
            },
        }

        Booking = client.order.create(data=data)
        booking_id = Booking['id']
        booking_status = Booking['status']

        if booking_status == "created":
            bookBus = BookBus(
                user = request.user.username,
                bus_source = bus_source,
                bus_destination = bus_destination,
                bus_arrival = bus_arrival,
                seats = seats,
                date = date,
                amount = amount/100,
                book_id = booking_id,
            )
            bookBus.save()
            return render(request,'bookingPage.html',{'bus':bus, 'payment':Booking})

    return render(request,'bookingPage.html',{'bus':bus})

def payment_status(request):
    response = request.POST
    params_dict={
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature'],
    }
    client = razorpay.Client(auth=('rzp_test_DgmIs9k3dQ2Dfi','nAOhLmQG2UFgNhaWjSMatlhJ'))
    try:
        print("inside try")
        status = client.utility.verify_payment_signature(params_dict)
        bookBus = BookBus.objects.get(book_id=response['razorpay_order_id'])
        bookBus.razorpay_payment_id = response['razorpay_payment_id']
        bookBus.paid = True
        bookBus.save()
        to_list = [request.user.email]
        print(to_list)
        html_content = render_to_string("paymentreceipt.html",{'book_details':bookBus,'user_details':request.user,'date':date.today()})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            "Your Booking Id is : ",
            text_content,
            settings.EMAIL_HOST_USER,
            to_list
        )
        email.attach_alternative(html_content,"text/html")
        email.send(fail_silently=True)
        return render(request,'payment_status.html',{'status' : True,'book_details':bookBus,'user_details':request.user,'date':date.today()})
    except:
        print("why faild")
        return render(request,'payment_status.html',{'status': False})

    print(response)
    return render(request,'payment_status.html')

def payment_receipt(request,bookBus):
    booking_details = BookBus.objects.get(book_id=bookBus)
    return render(request,'payment_receipt.html',{'booking_details':booking_details})

@login_required(redirect_field_name='timeTablePage', login_url='/loginPage/')
def user_profile(request):
    user_details = request.user
    booking_details = BookBus.objects.filter(Q(user=request.user.username))
    return render(request,'profile.html',{'user': user_details,'booking_details':booking_details})