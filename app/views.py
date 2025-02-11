from django.shortcuts import render, redirect
from .models import Account
# Create your views here.
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime


from django.contrib.auth.decorators import login_required
from .models import Account
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


@login_required
def menu(request):
    check_employee = request.user.groups.filter(name__in=['Admin', 'Medical Staff', 'Caretaker']).exists()

    # Fetch all users from the database
    users = Account.objects.all()

    context = {
        'title': 'Main Menu',
        'is_employee': check_employee,
        'year': datetime.now().year,
        'users': users,  # Pass users to template
        'user': request.user
    }

    return render(request, 'app/menu.html', context)

def create_account(request):
    return render(request, 'app/createAcc.html')
def configure_account(request):
    return render(request, 'app/configureAcc.html')
def change_password(request):
    return render(request, 'app/changePassword.html')
