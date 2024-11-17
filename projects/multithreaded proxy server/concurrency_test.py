import requests
from concurrent.futures import ThreadPoolExecutor

# Define the server URL
url = "http://127.0.0.1:65432"  # Replace with your server's URL

# Function to make HTTP requests
def make_request():
    try:
        response = requests.get(url)
        print(f"Response: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

# Number of concurrent requests
num_requests = 100  # Adjust as needed
concurrent_threads = 10  # Number of threads to run concurrently

# Using ThreadPoolExecutor to send requests concurrently
with ThreadPoolExecutor(max_workers=concurrent_threads) as executor:
    # Submit tasks to the thread pool
    futures = [executor.submit(make_request) for _ in range(num_requests)]
    # Wait for all futures to complete
    for future in futures:
        future.result()

