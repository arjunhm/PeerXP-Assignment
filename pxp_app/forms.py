from django import forms
from pxp_app.models import User, Ticket


class NewTicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['department', 'category', 'url', 'subject', 'description', 'priority']
