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
from django.contrib.auth.hashers import make_password


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


def configure_account(request, user_id):
    user = get_object_or_404(Account, id=user_id)  # Fetch user

    if request.method == "POST":
        if "delete" in request.POST:  # Handle Delete
            user.delete()
            return redirect("menu")  # Redirect to menu after deletion

        elif "update" in request.POST:  # Handle Update
            full_name = request.POST.get("full_name", "").strip()
            name_parts = full_name.split(" ", 1)  # Split into first and last name

            user.first_name = name_parts[0]  # First part as first name
            user.last_name = name_parts[1] if len(name_parts) > 1 else ""  # Second part (if available) as last name
            user.username = request.POST.get("username")
            user.role = request.POST.get("role")

            user.save()
            return redirect("menu")  # Redirect after updating

    return render(request, "app/configureAcc.html", {"user": user})
def change_password(request, user_id):
    user = get_object_or_404(Account, id=user_id)

    if request.method == "POST":
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password != confirm_password:
            return render(request, "app/changePassword.html", {
                "error_message": "Passwords do not match."
            })

        # Hash and save the new password
        user.password = make_password(new_password)
        user.save()
        return redirect("menu")  # Redirect after successful password change

    return render(request, "app/changePassword.html")
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
    cat = get_object_or_404(Cat, CatID=cat_id)  # Get the cat from the Cat database
    treatments = Treatment.objects.filter(CatID=cat)  # Use the cat instance, not just cat_id

    return render(request, 'app/medical_cat_detail.html', {
        'cat': cat,  # Pass the cat object
        'treatments': treatments,  # Pass treatments related to this cat
    })



def create_treatment(request, cat_id):
    cat = get_object_or_404(Cat, CatID=cat_id)
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

@login_required
def report(request):
    cats = Cat.objects.all()  # Fetch all cats from the database
    cat_treatments = {cat.CatID: Treatment.objects.filter(CatID=cat.CatID) for cat in cats}
    return render(request, 'app/report.html', {'cats': cats, 'cat_treatments': cat_treatments})

def configure_cat(request, cat_id):
    cat = get_object_or_404(Cat, CatID=cat_id)  # Correct field name

    if request.method == "POST":
        if 'update' in request.POST:
            cat.Name = request.POST.get('name')
            cat.Breed = request.POST.get('breed')
            cat.Age = request.POST.get('age')
            cat.Description = request.POST.get('description')
            cat.save()
        elif 'delete' in request.POST:
            cat.delete()
            return redirect('cat_list')  # Redirect to cat list after deletion

    return render(request, 'app/configureCat.html', {'cat': cat})
