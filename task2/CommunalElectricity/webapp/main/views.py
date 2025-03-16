from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, AddForm, SendForm
from .models import User, Meter, Bill, Reading
from django.utils import timezone

DAY_TARIFF = 4.32
NIGHT_TARIFF = 2.16

def index(request):
    return render(request, 'index.html')

def registration(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if User.objects.filter(email=email).exists():
                return render(request, 'registration.html',
                              {'form': form,
                               'error': 'Користувач з такою поштою уже існує'})
            user = User(name=name, email=email, password=password)
            user.save()
            return redirect('/')

    return render(request, 'registration.html',{ 'form': form, })

def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if User.objects.filter(email=email, password=password).exists():
                request.session['email'] = email
                return redirect('home',)
            else:
                return render(request, 'login.html',
                              {'form': form,
                               'error': 'Такого користувача не існує, перевірте введені дані'})

    return render(request, 'login.html',{ 'form': form, })

def home(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')
    return render(request, 'home.html',{'email': email})

def logout(request):
    request.session.flush()
    return redirect('/')

def add(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')
    form = AddForm()
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']
            if Meter.objects.filter(meter_number=number).exists():
                return render(request, 'adding.html',
                              {'email': email,
                               'form': form,
                               'error': 'Лічильник з таким номером вже зареєстрований у системі'})
            user = User.objects.filter(email=email).first()
            meter = Meter(meter_number=number, user=user)
            meter.save()
            return redirect('home')

    return render(request, 'adding.html',
                  {'email': email,
                            'form': form})

def calculate_total(prev_day, prev_night, curr_day, curr_night):
    day_fee = (curr_day - prev_day) * DAY_TARIFF
    night_fee = (curr_night - prev_night) * NIGHT_TARIFF
    return day_fee, night_fee, day_fee + night_fee

def send(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')
    form = SendForm(email)
    if request.method == 'POST':
        form = SendForm(email, request.POST)
        if form.is_valid():
            meter = form.cleaned_data['choiceMeter']
            day_value = form.cleaned_data['dayValue']
            night_value = form.cleaned_data['nightValue']
            user = User.objects.filter(email=email).first()

            reading = Reading(meter=meter, day_kwh=day_value, night_kwh=night_value)

            prev_reading = Reading.objects.filter(meter=meter).order_by("-date").first()

            try:
                prev_day_value = prev_reading.day_kwh
                prev_night_value = prev_reading.night_kwh
            except AttributeError:
                request.session['is_first_reading'] = True
                reading.save()
                return redirect('home')

            if request.session.get('is_first_reading') is True:
                request.session['is_first_reading'] = False

            if prev_day_value > day_value:
                local_date = timezone.localtime(prev_reading.date)
                return render(request, 'sending.html',
                              {'email': email, 'form': form,
            'error': f"Помилка: Попередні денні показники {local_date.strftime('%d-%m-%Y %H:%M:%S')} - {prev_day_value} кВт⋅год більші за поточні {day_value} кВт⋅год !"})

            if prev_night_value > night_value:
                local_date = timezone.localtime(prev_reading.date)
                return render(request, 'sending.html',
                              {'email': email, 'form': form,
            'error': f"Помилка: Попередні нічні показники {local_date.strftime('%d-%m-%Y %H:%M:%S')} - {prev_night_value} кВт⋅год більші за поточні {night_value} кВт⋅год !"})

            reading.save()

            day_fee, night_fee, total_fee = calculate_total(prev_day_value, prev_night_value, day_value, night_value)

            bill = Bill(user=user, meter=meter, day_usage=day_fee, night_usage=night_fee, total_price=total_fee)
            bill.save()

            request.session['is_success_send'] = True
            return redirect('home')

    return render(request, 'sending.html',
                  {'email': email, 'form': form, })

def history(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')

    user = User.objects.filter(email=email).first()
    meters = Meter.objects.filter(user=user)

    history_data = []
    for meter in meters:
        readings = Reading.objects.filter(meter=meter).order_by('-date')
        bils = Bill.objects.filter(meter=meter).order_by('-date')
        prev_dates = []
        for reading in readings:
            prev_dates.append(reading.date)
        prev_dates.pop(0)
        bills = []
        counter = 0
        for bil in bils:
            bills.append({
                'prev_date': prev_dates[counter],
                'date': bil.date,
                'total_price': bil.total_price
            })
            counter += 1
        meter_data = {
            'meter_number': meter.meter_number,
            'readings': readings,
            'bills': bills,
        }
        history_data.append(meter_data)

    return render(request, 'history.html',
                  {'email': email,
                        'history_data': history_data})




