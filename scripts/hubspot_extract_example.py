"""Exemplo de extração real de contatos HubSpot para plugar no pipeline."""

import os
import requests


def fetch_contacts(token: str, limit: int = 100):
    url = "https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "limit": limit,
        "properties": "email,phone,firstname,lastname,city,cpf,lgpd_consent",
    }
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json().get("results", [])


if __name__ == "__main__":
    token = os.getenv("HUBSPOT_TOKEN")
    if not token:
        raise SystemExit("Defina HUBSPOT_TOKEN no ambiente.")
    items = fetch_contacts(token)
    print(f"contatos recebidos: {len(items)}")
