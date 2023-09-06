import threading, requests

# Define a function that prints "uwu" repeatedly
def uwu_printer():
    while True:
        requests.get("http://127.0.0.1:8080/api/v1")

# Define the number of threads to create
num_threads = 300  # You can adjust this number

# Create and start the threads
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=uwu_printer)
    threads.append(thread)
    thread.start()

# Wait for all threads to finish (you can interrupt this manually)
for thread in threads:
    thread.join()
