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
    return render(request, 'pxp_app/home.html', {})


def login_view(request):
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

    logout(request)
    return redirect('home-view')


@login_required
def add_ticket_view(request):
    user_obj = User.objects.get(name=str(request.user))

    if request.method == 'POST':

        form = NewTicketForm(request.POST)
        if form.is_valid():
            
            department = form.cleaned_data['department']
            category = form.cleaned_data['category']
            subject = form.cleaned_data['subject']
            description = form.cleaned_data['description']
            priority = form.cleaned_data['priority']
            url = form.cleaned_data['url']

            ticket_obj = Ticket.objects.create(user=user_obj, department=department, category=category, url=url,
                                               subject=subject, description=description, priority=priority)
 

            # api_funcs.create_ticket(form.cleaned_data, user_obj)

            messages.add_message(request, messages.SUCCESS, 'Succesfully submitted ticket.')
            return redirect('add-ticket-view')
    else:
        form = NewTicketForm()

    return render(request, 'pxp_app/add_ticket.html', {'form': form, 'user_obj': user_obj})


@login_required
def manage_tickets_view(request):
    user_obj = User.objects.get(name=str(request.user))
    tickets = Ticket.objects.filter(user=user_obj)

    # content = api_funcs.get_all_tickets()
    # tickets = api_funcs.extract_content(content, user_obj)


    return render(request, 'pxp_app/manage_tickets.html', {'tickets': tickets})


def ticket_detail_view(request, pk):

    ticket = Ticket.objects.get(id=pk)

    # content = api_funcs.get_ticket_detail(pk)
    # content = [content]
    # ticket = api_funcs.extract_content(content)

    if request.method == 'POST':

        if ticket.status == 'Open':
            ticket.status = 'Close'
            # data = {'status': "Close"}
        else:
            ticket.status = 'Open'
            # data = {'status': "Open"}
    
        ticket.save()
        
        # api_funcs.update_ticket(data, pk)

        return redirect('manage-tickets-view')

    return render(request, 'pxp_app/ticket_detail.html', {'ticket': ticket})


def ticket_delete_view(request, pk):

    ticket = Ticket.objects.get(id=pk)
    ticket.delete()
    # api_funcs.delete_ticket(pk)
    return redirect('manage-tickets-view')