import requests
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

def get_access_token():
    response = requests.post(
        "https://acleddata.com/oauth/token",
        data={
            "username": os.getenv("EMAIL"),
            "password": os.getenv("PASSWORD"),
            "grant_type": "password",
            "client_id": "acled",
            "scope": "authenticated"
        }
    )

    if response.status_code != 200:
        print("Authentication failed")
        exit()
    else:
        print("Authentication successful")

    token = response.json()["access_token"]

    return token
    

def fetch_nigeria_data(token):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "country": "Nigeria"
    }

    response = requests.get(
        "https://acleddata.com/api/acled/read",
        headers=headers,
        params=params
    )
    if response.status_code != 200:
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        return None

    data = response.json()

    if "data" not in data:
        raise ValueError("Malformed response: 'data' key not found.")

    if not data["data"]:
        print("No records found for the specified filter.")
    else:
        print(f"Fetched {len(data['data'])} records for Nigeria.")

    return data["data"]


if __name__ == "__main__":
    token = get_access_token()
    records = fetch_nigeria_data(token)
    
    if records is None:
        print("Data fetch failed. Exiting pipeline.")
        exit()
    df = pd.DataFrame(records)

    os.makedirs("data", exist_ok=True)

    df.to_csv("data/raw_nigeria_acled.csv", index=False)

    print(f"Saved {len(df)} records to data/raw_nigeria_acled.csv")