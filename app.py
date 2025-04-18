from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

window_size = 10
numbers = []

def register():
    url = "http://20.244.56.144/evaluation-service/register"
    data = {
        "email": "your_email@domain.com",
        "name": "Your Name",
        "mobileNo": "9999999999",
        "githubUsername": "your_github_username",
        "rollNo": "your_roll_number",
        "collegeName": "Your College",
        "accessCode": "your_access_code"
    }
    response = requests.post(url, json=data)
    print(response.json())

def get_auth_token():
    url = "http://20.244.56.144/evaluation-service/auth"
    data = {
        "email": "your_email@domain.com",
        "name": "Your Name",
        "rollNo": "your_roll_number",
        "accessCode": "your_access_code",
        "clientID": "your_client_id",
        "clientSecret": "your_client_secret"
    }
    response = requests.post(url, json=data)
    print(response.json())
    return response.json().get('access_token')

def fetch_numbers(numberid):
    api_map = {
        'p': 'primes',
        'f': 'fibo',
        'e': 'even',
        'r': 'rand'
    }
    url = f"http://20.244.56.144/evaluation-service/{api_map[numberid]}"
    response = requests.get(url)
    return response.json().get('numbers', [])

@app.route('/numbers/<numberid>', methods=['GET'])
def get_numbers(numberid):
    global numbers
    new_numbers = fetch_numbers(numberid)

    numbers.extend(new_numbers)
    numbers = list(set(numbers)) 
    numbers = [n for n in numbers if n <= 500] 
    
    if len(numbers) > window_size:
        numbers = numbers[-window_size:]
    
    avg = sum(numbers) / len(numbers) if numbers else 0
    
    response = {
        "windowPrevState": numbers[:-len(new_numbers)],
        "windowCurrState": numbers,
        "numbers": new_numbers,
        "avg": avg
    }
    return jsonify(response)

if __name__ == '__main__':
    register() 
    app.run(port=9876)