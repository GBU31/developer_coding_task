import requests

def search():
    url = "https://api.mozio.com/v2/search/"
    headers = {
        "API-KEY": "6bd1e15ab9e94bb190074b4209e6b6f9"
    }
    payload = {
        "start_address": "44 Tehama Street, San Francisco, CA, USA",
        "end_address": "SFO",
        "mode": "one_way",
        "pickup_datetime": "2023-12-01 15:30",
        "num_passengers": 2,
        "currency": "USD",
        "campaign": "Daniel Tashman"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        search_id = response.json()["id"]
        return search_id
    else:
        print(response.status_code, response.text)
        return None


def poll_search(search_id):
    url = f"https://api.mozio.com/v2/search/{search_id}/poll/"
    headers = {
        "API-KEY": "6bd1e15ab9e94bb190074b4209e6b6f9"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(response.status_code, response.text)
        return None


def book(search_id):
    url = f"https://api.mozio.com/v2/search/{search_id}/reservations/"
    headers = {
        "API-KEY": "6bd1e15ab9e94bb190074b4209e6b6f9"
    }
    payload = {
        "search_id": search_id,
        "provider_name": "Dummy External Provider",
        "vehicle_type": "cheapest"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        confirmation_number = response.json()["confirmation_number"]
        return confirmation_number
    else:
        print("Error:", response.status_code, response.text)
        return None


def poll_booking(confirmation_number):
    url = f"https://api.mozio.com/v2/search/{confirmation_number}/poll/"
    headers = {
        "API-KEY": "6bd1e15ab9e94bb190074b4209e6b6f9"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code, response.text)
        return None


def cancel_booking(confirmation_number):
    url = f"https://api.mozio.com/v2/search/reservations/{confirmation_number}"
    headers = {
        "API-KEY": "6bd1e15ab9e94bb190074b4209e6b6f9"
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        print("Booking with confirmation number", confirmation_number, "has been cancelled.")
    else:
        print(response.status_code, response.text)


search_id = search()
if search_id:
    print("Search ID:", search_id)

    search_results = poll_search(search_id)
    if search_results:
        confirmation_number = book(search_id)
        if confirmation_number:
            print("Booking Confirmation Number:", confirmation_number)

            booking_status = poll_booking(confirmation_number)
            if booking_status:
                cancel_booking(confirmation_number)
        else:
            print("Booking failed.")
    else:
        print("Search results not found.")
else:
    print("Search failed.")
