import requests
import os
import json

BASIC_URL = "http://localhost:8000/api/public/v1/"
GCLOUD_SERVICE_MAIL = os.getenv("GCLOUD_SERVICE_MAIL")
CLIENT_ID = os.getenv("AIRBYTE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AIRBYTE_CLIENT_SECRET")
SERVICE_ACCOUNT_FILE = "service_account_info.json"


def get_token(client_id, client_secret):
    url = f"{BASIC_URL}applications/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    return f'{data["token_type"]} {data["access_token"]}'


def get_first_workspace_data(token):
    url = f"{BASIC_URL}workspaces"
    headers = {
        "Accept": "application/json",
        "Authorization": token
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    if not data.get("data"):
        raise ValueError("No workspaces found")
    workspace = data["data"][0]
    return workspace["workspaceId"], workspace["name"]


def get_sources_list(workspace_id, workspace_name, token):
    url = f"{BASIC_URL}sources"
    headers = {
        "Accept": "application/json",
        "Authorization": token
    }
    payload = {
        "name": workspace_name,
        "workspaceId": workspace_id
    }
    response = requests.get(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json().get("data", [])


def read_service_account_info():
    with open(SERVICE_ACCOUNT_FILE, "r") as f:
        return f.read()


def connect_google_search(workspace_id, workspace_name, token, service_account_info):
    url = f"{BASIC_URL}sources"
    payload = { 
        "configuration": {
            "sourceType": "google-search-console",
            "authorization": {
                "service_account_info": service_account_info,
                "auth_type": "Service",
                "email": GCLOUD_SERVICE_MAIL
            },
            "site_urls": ["google.com"],
            "data_state": "final"
        },
        "name": workspace_name,
        "workspaceId": workspace_id 
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": token
    }
    response = requests.post(url, json=payload, headers=headers)
    print("Google Search response:", response.text)


def connect_google_analytics(workspace_id, workspace_name, token, service_account_info):
    url = f"{BASIC_URL}sources"
    payload = {
        "configuration": {
            "sourceType": "google-analytics-data-api",
            "credentials": {
                "auth_type": "Service",
                "credentials_json": service_account_info
            },
            "property_ids": ["473794894"]
        },
        "name": workspace_name,
        "workspaceId": workspace_id
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": token
    }
    response = requests.post(url, json=payload, headers=headers)
    print("Google Analytics response:", response.text)


def connect_posthog(workspace_id, workspace_name, token):
    url = f"{BASIC_URL}sources"
    payload = {
        "configuration": {
            "sourceType": "posthog",
            "api_key": "phx_IyecEa8A9yj0cVi1Hswoy9wV0MUykOwkk4p7UmajRs7oLxO",
            "start_date": "2021-01-01T00:00:00Z"
        },
        "name": workspace_name,
        "workspaceId": workspace_id
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": token
    }
    response = requests.post(url, json=payload, headers=headers)
    print("Posthog response:", response.text)


def main():
    token = get_token(CLIENT_ID, CLIENT_SECRET)
    workspace_id, workspace_name = get_first_workspace_data(token)
    sources = get_sources_list(workspace_id, workspace_name, token)
    
    if not sources:
        service_account_info = read_service_account_info()
        connect_google_analytics(workspace_id, workspace_name, token, service_account_info)
        connect_google_search(workspace_id, workspace_name, token, service_account_info)
        connect_posthog(workspace_id, workspace_name, token)

if __name__ == "__main__":
    main()
