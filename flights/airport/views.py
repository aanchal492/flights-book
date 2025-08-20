from django.shortcuts import render, get_object_or_404, redirect
from .models import Flight, FlightBooking
from datetime import date

def index(request):
    # search
    origin = request.GET.get('origin')
    destination = request.GET.get('destination')
    flight_date = request.GET.get('date')

    flights = Flight.objects.all()
    if origin:
        flights = flights.filter(origin__icontains=origin)
    if destination:
        flights = flights.filter(destination__icontains=destination)
    if flight_date:
        flights = flights.filter(date=flight_date)

    last_flight_id = request.session.get('last_flight_id')
    return render(request, 'index.html', {
        "flights": flights,
        "last_flight_id": last_flight_id
    })

def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    booked_seats = FlightBooking.objects.filter(flight=flight).values_list('seat_number', flat=True)
    available_seats = [s for s in range(1, flight.total_seats + 1) if s not in booked_seats]

    if request.method == 'POST':
        passenger_name = request.POST.get('passenger_name')
        seat_number = int(request.POST.get('seat_number'))

        FlightBooking.objects.create(
            flight=flight,
            passenger_name=passenger_name,
            seat_number=seat_number
        )
        request.session['last_flight_id'] = flight.id
        return redirect('booking_summary', flight_id=flight.id)

    return render(request, 'flight_book.html', {
        "flight": flight,
        "available_seats": available_seats
    })

def booking_summary(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    booking = FlightBooking.objects.filter(flight=flight).last()
    return render(request, 'booking_summary.html', {
        "booking": booking
    })

def your_flights(request):
    last_flight_id = request.session.get('last_flight_id')
    flights = FlightBooking.objects.all()
    return render(request, 'your_flight.html', {
        "flights": flights,
        "last_flight_id": last_flight_id
    })
def contact(request):
    return render(request, 'contact.html')
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

# Register view
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'register.html')

# Login view
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')
