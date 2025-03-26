import requests

session = requests.Session()

def login():
    url = "http://localhost:8000/api/token/"
    username = "root"
    password = "root"
    # username = "test1"
    # password = "test1"
    response = session.post(url, json={"username": username, "password": password})
    # set Authorization Bearer header with received token
    session.headers.update({"Authorization": f"Bearer {response.json()['access']}"})

def create_task():
    url = "http://localhost:8000/api/tasks/2/"
    response = session.get(url)
    print(response.json())

def create_team():
    url = "http://localhost:8000/api/teams/"
    data = {"name": "Alpha"}
    response = session.post(url, json=data)
    print(response.json())

def get_teams():
    url = "http://localhost:8000/api/teams/"
    response = session.get(url)
    print(response.json())

def assign_team():
    url = "http://localhost:8000/api/teams/members/"
    data = {
        "team": 10,
        "user": 5,
        "role": "member"
    }
    response = session.post(url, json=data)
    print(response.json())

if __name__ == "__main__":
    login()
    # get_teams()
    assign_team()