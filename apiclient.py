import requests


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_contacts(self):
        url = f"{self.base_url}/contact"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            return None


if __name__ == "__main__":

    api_client = APIClient("http://localhost:5000")

    contacts = api_client.get_contacts()

    if contacts is not None:
        all_contacts = []
        for contact in contacts:
            all_contacts.append(contact)
        print(all_contacts)
