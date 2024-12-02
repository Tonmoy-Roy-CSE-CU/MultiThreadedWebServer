import requests
from concurrent.futures import ThreadPoolExecutor

# Function to make a request
def make_request(url):
    response = requests.get(url)
    print(f"Response Code: {response.status_code} for {url}")

# List of URLs to test
urls = ["http://127.0.0.1:8080/about.html"] * 10  # Adjust number of requests

# Using ThreadPoolExecutor for concurrency
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(make_request, urls)
