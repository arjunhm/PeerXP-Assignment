from pxp_site import settings

import requests
import json

# To be added
AUTH_TOKEN = settings.AUTH_TOKEN

# Request HEADERS
HEADERS = {
    "Authorization": AUTH_TOKEN,
    "contentType": "application/json; charset=utf-8"
}


def get_all_tickets():
    """Retreives all the tickets

    Returns:
        response: The content of the response
    """
    response = requests.get('https://desk.zoho.com/api/v1/tickets/', headers=HEADERS)

    if response.status_code == 200:
        return response.content
    return None
    

def create_ticket(form_data, user):
    """Create ticket by using cleaned form data and user's data

    Args:
        form_data (Dict): Cleaned form data
        user (Model): User object from User queryset
    """

    data = {
        'departmentId': form_data['department'],
        'category': form_data['category'],
        'subject': form_data['subject'],
        'description': form_data['description'],
        'priority': form_data['priority'],
        'webUrl': form_data['url'],
        'email': form_data[user.email],
        "status" : "Open",
    }
    
    request = requests.post('https://desk.zoho.com/api/v1/tickets', headers=HEADERS, data=json.dumps(data))
    
    if request.status_code == 200:
        return True
    return False


def update_ticket(data, ticket_id):
    """Updates an existing ticket

    Args:
        data (dict): Data of the fields to be updated
        ticket_id (str): ID of the ticket to be updated

    Returns:
        Boolean: Indicates if the request was succesful or not
    """

    response = requests.patch(f"https://desk.zoho.com/api/v1/tickets/{ticket_id}",
                            headers=HEADERS,
                            data=json.dumps(data))
    
    if response.status_code == 200:
        return True
    return False


def delete_ticket(id):
    """Deletes an existing ticket

    Args:
        id (str): ID of the ticket to be deleted

    Returns:
        Boolean: Indicates if the request was succesful or not
    """
    data = {
        "ticketIds" : [ str(id) ]
    }
    response = requests.post('https://desk.zoho.com/api/v1/moveToTrash/',
                            headers=HEADERS,
                            data=json.dumps(data))

    if response.status_code == 200:
        return True
    return False


def extract_content(content, user_obj):
    """Extract required data from response

    Args:
        content (response): List of all tickets
        user_obj (Model): User object from User queryset

    Returns:
        list: List of dictionaries containing ticket details
    """
    data = []

    for i in content:

        if i['email'] == user_obj.email:
            temp = {
                    'department': content['departmentId'],
                    'category': content['category'],
                    'subject': content['subject'],
                    'description': content['description'],
                    'priority': content['priority'],
                    'url': content['webUrl'],
                    'email': content[user.email],
                    "status" : content['status']
                    }
            data.append(temp)
    
    return data


def get_ticket_detail(id):
    """Retrieves details of a ticket

    Args:
        id (str): ID of the ticket

    Returns:
        Response: The content of the response
    """
    response = requests.get(f'https://desk.zoho.com/api/v1/tickets/{id}', headers=HEADERS)

    if response.status_code == 200:
        return response.content
    return None
