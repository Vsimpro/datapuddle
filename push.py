import json
import requests

URL = ""

# Temporary push for testing
def push( payload ):
    response = requests.post(url, json=payload)

    print(response.status_code)
    print(response.json())


if __name__ == "__main__":
    url = "http://localhost:5000/api/puddle/add"
    URL = url

    with open("populate.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    
    for d in data:
        push(d)