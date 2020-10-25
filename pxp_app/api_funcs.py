import requests
import json

from pxp_site import settings

AUTH_TOKEN = settings.AUTH_TOKEN
ORG_ID = settings.ORG_ID

# Request HEADERS
HEADERS = {
    "Authorization": AUTH_TOKEN,
    "orgId": ORG_ID,
    "contentType": "application/json; charset=utf-8"
}

DEPARTMENT_IDS = {
    '7189000001062045': 'PWSLab DevOps Support',
    '7189000000051431': 'iSupport'
}


def get_all_tickets():
    """Retreives all the tickets

    Returns:
        response: The content of the response
    """
    response = requests.get('https://desk.zoho.in/api/v1/tickets', headers=HEADERS)
    if response.status_code == 200:
        return json.loads(response.content)
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
        'email': user.email,
        "status" : "Open",
        "contactId": "7189000001130003"
    }
    data = json.dumps(data)
    response = requests.post('https://desk.zoho.in/api/v1/tickets', headers=HEADERS, data=data)
    if response.status_code == 200:
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

    response = requests.patch(f"https://desk.zoho.in/api/v1/tickets/{ticket_id}",
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

    response = requests.post('https://desk.zoho.in/api/v1/tickets/moveToTrash',
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
    if content:
        for i in content['data']:
            if i['email'] == str(user_obj.email):
                temp = {
                        'id': i['id'],
                        'ticketNumber': i['ticketNumber'],
                        'department': DEPARTMENT_IDS[i['departmentId']],
                        'category': i['category'],
                        'subject': i['subject'],
                        'priority': i['priority'],
                        'url': i['webUrl'],
                        'email': i['email'],
                        "status" : i['status'],
                        'contactId': i['contactId']
                        }
                data.append(temp)
    return data


def get_ticket_detail(ticket_id):
    """Retrieves details of a ticket

    Args:
        id (str): ID of the ticket

    Returns:
        Response: The content of the response
    """
    response = requests.get(f'https://desk.zoho.in/api/v1/tickets/{ticket_id}', headers=HEADERS)

    if response.status_code == 200:
        return json.loads(response.content)
    return None
