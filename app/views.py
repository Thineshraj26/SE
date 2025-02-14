from django.shortcuts import render, redirect, get_object_or_404
from .models import Account
# Create your views here.
from django.http import HttpRequest, FileResponse
from django.template import RequestContext
from datetime import datetime
from .forms import CatForm, AccountCreationForm, AppointmentForm, TreatmentForm

import os
from django.contrib.auth.decorators import login_required
from .models import Account
from CatDatabase.models import Cat, Treatment, Appointment
from django.conf import settings
import shutil

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        return(redirect('/menu'))
    else:
        return render(
            request,
            'app/index.html',
            {
                'title':'Home Page',
                'year': datetime.now().year,
            }
        )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Dr. Yeoh.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'ABC System',
            'message':'This application processes ...',
            'year':datetime.now().year,
        }
    )


def menu(request):
    if request.user.groups.filter(name="Medical Staff").exists():
        return redirect('medical_cat_list')  # Redirect Medical Staff

    if request.user.groups.filter(name="Caretaker").exists():
        return redirect('caretaker_duty_panel')  # Redirect Caretakers

    users = Account.objects.all()
    context = {
        'title': 'Main Menu',
        'year': datetime.now().year,
        'users': users,
        'user': request.user
    }
    return render(request, 'app/menu.html', context)


def cat_list(request):
    cats = Cat.objects.all()
    return render(request, 'app/cat_list.html', {'cats': cats})
def create_account(request):
    if request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Create user but don't save yet
            role = form.cleaned_data['role']  # Get the role from the form
            user.save()  # Save user
            user.assign_group(role)  # Assign role group
            return redirect('/')  # Redirect to homepage after successful registration
    else:
        form = AccountCreationForm()

    return render(request, "app/createAcc.html", {"form": form})
def configure_account(request):
    return render(request, 'app/configureAcc.html')
def change_password(request):
    return render(request, 'app/changePassword.html')
def system_settings(request):
    return render(request, 'app/system_settings.html')
def create_cat(request):
    if request.method == "POST":
        form = CatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to a success page (change as needed)
    else:
        form = CatForm()

    return render(request, 'app/createCat.html', {'form': form})



def cat_details(request, cat_id):
    cat = get_object_or_404(Cat, CatID=cat_id)
    # Fetch the latest appointment for this cat
    latest_appointment = Appointment.objects.filter(CatID=cat).order_by('-Date').first()

    return render(request, 'app/cat_details.html', {'cat': cat, 'appointment': latest_appointment})



def cat_scheduler_checkup(request, cat_id):
    cat = get_object_or_404(Cat, CatID=cat_id)  # Fetch the correct cat
    form = AppointmentForm(request.POST or None)  # Load form with POST data if available

    if request.method == 'POST' and form.is_valid():
        checkup = form.save(commit=False)
        checkup.CatID = cat  # Assign the correct cat
        checkup.save()
        return redirect('cat_details', cat_id=cat.CatID)  # Redirect after saving

    return render(request, 'app/cat_scheduler_checkup.html', {'form': form, 'cat': cat})


def medical_cat_detail(request, cat_id):
    cat = get_object_or_404(Cat, CatID=cat_id)  # Ensure the cat exists
    treatments = Treatment.objects.filter(CatID=cat_id)


    return render(request, 'app/medical_cat_detail.html', {
        'treatments': treatments,
        'CatID': cat_id,  # Ensure this key is passed
    })


def create_treatment(request, cat_id):
    cat = get_object_or_404(Cat, pk=cat_id)  # Ensure the cat exists

    if request.method == "POST":
        form = TreatmentForm(request.POST)
        if form.is_valid():
            treatment = form.save(commit=False)
            treatment.CatID = cat  # Assign the foreign key
            treatment.save()
            return redirect("medical_cat_detail", cat_id=cat_id)
    else:
        form = TreatmentForm()

    return render(request, "app/create_treatment.html", {"form": form, "cat_id": cat_id})


@login_required
def medical_cat_list(request):
    cats = Cat.objects.all()
    return render(request, 'app/medical_cat_list.html', {'cats': cats})

@login_required
def caretaker_duty_panel(request):
    cats = Cat.objects.all()  # Fetch all cats from the database
    today_date = datetime.now().strftime('%d/%m/%Y')  # Format: DD/MM/YYYY
    current_time = datetime.now().strftime('%H:%M')  # Format: HH:MM

    return render(request, 'app/caretaker_duty_panel.html', {'cats': cats, 'today_date': today_date,
        'current_time': current_time})

def backup_database(request):
    db_path = os.path.join(settings.BASE_DIR, "db.sqlite3")
    response = FileResponse(open(db_path, "rb"), as_attachment=True, filename="backup.sqlite3")
    return response


def import_database(request):
    if request.method == "POST" and request.FILES.get("db_file"):
        new_db = request.FILES["db_file"]
        db_path = os.path.join(settings.BASE_DIR, "db.sqlite3")

        # Save the uploaded file as the new database
        with open(db_path, "wb") as f:
            for chunk in new_db.chunks():
                f.write(chunk)

        return redirect("system_settings")  # Redirect after successful import

    return redirect("system_settings")  # Redirect if no file was uploaded
