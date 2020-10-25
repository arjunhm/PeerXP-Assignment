from django.shortcuts import render, redirect

# User authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.contrib import messages

# Custom
from pxp_app.models import User, Ticket
from pxp_app.forms import NewTicketForm
from pxp_app import api_funcs


def home_view(request):
    """
    View for home page
    """
    return render(request, 'pxp_app/home.html', {})


def login_view(request):
    """
    View for logging in an user
    """
    if request.method == 'POST':

        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            raw_password = form.cleaned_data['password']

            user = authenticate(username=email, password=raw_password)
            login(request, user)

            return redirect('home-view')
    else:
        form = AuthenticationForm()

    return render(request, 'pxp_app/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    View for logging an user out
    """
    logout(request)
    return redirect('home-view')


@login_required
def add_ticket_view(request):
    """
    View for creating a ticket
    """
    
    user_obj = User.objects.get(name=str(request.user))

    if request.method == 'POST':

        form = NewTicketForm(request.POST)
        if form.is_valid():
            
            # Creates a ticket using the form data along with user details
            status_code = api_funcs.create_ticket(form.cleaned_data, user_obj)
            
            # If succesfully created a ticket
            if status_code:
                messages.add_message(request, messages.SUCCESS, 'Succesfully submitted ticket.')

            return redirect('add-ticket-view')
    else:
        form = NewTicketForm()

    return render(request, 'pxp_app/add_ticket.html', {'form': form, 'user_obj': user_obj})


@login_required
def manage_tickets_view(request):
    """
    View for listing out all tickets submitted by a user
    """

    user_obj = User.objects.get(name=str(request.user))

    # Fetch list of all tickets
    content = api_funcs.get_all_tickets()
    # Extract necessary details of tickets submitted by the user
    tickets = api_funcs.extract_content(content, user_obj)
    return render(request, 'pxp_app/manage_tickets.html', {'tickets': tickets})


def ticket_detail_view(request, pk):
    """
    View for viewing the details of a ticket
    """

    user_obj = User.objects.get(name=str(request.user))

    ticket = api_funcs.get_ticket_detail(pk)
    ticket['user'] = user_obj.name

    # If update request is received
    if request.method == 'POST':

        if ticket['status'] == 'Open':
            data = {'status': "Closed"}
        else:
            data = {'status': "Open"}
        
        # updates the status of a ticket        
        api_funcs.update_ticket(data, pk)

        return redirect('manage-tickets-view')

    return render(request, 'pxp_app/ticket_detail.html', {'ticket': ticket})


def ticket_delete_view(request, pk):
    """
    View for deleting a ticket
    """

    api_funcs.delete_ticket(pk)
    return redirect('manage-tickets-view')
