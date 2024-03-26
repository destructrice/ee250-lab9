import time
import numpy as np
import pandas as pd
import requests
import threading
import plotly.express as px

def generate_data() -> list:
    """Generate some random data."""
    return np.random.randint(100, 10000, size=1000).tolist()

def process1(data: list) -> list:
    """Find the next largest prime number for each number in data."""
    def foo(x):
        while True:
            x += 1
            if all(x % i for i in range(2, x)):
                return x
    return [foo(x) for x in data]

def process2(data: list) -> list:
    """Find the next perfect square for each number in data."""
    def foo(x):
        while True:
            x += 1
            if int(np.sqrt(x)) ** 2 == x:
                return x
    return [foo(x) for x in data]

def final_process(data1: list, data2: list) -> float:
    """Calculate the mean of the differences between data1 and data2."""
    return np.mean([x - y for x, y in zip(data1, data2)])

def offload_process(data: list, process_name: str, offload_url: str) -> list:
    """Offload processing to a server."""
    response = requests.post(f"{offload_url}/{process_name}", json={'data': data})
    return response.json()

def run(offload: str = None) -> float:
    data = generate_data()
    offload_url = 'http://172.20.10.4:5001'

    if offload == 'process1':
        thread = threading.Thread(target=lambda: offload_process(data, 'process1', offload_url))
        thread.start()
        data2 = process2(data)
        thread.join()
        data1 = offload_process(data, 'process1', offload_url)
    elif offload == 'process2':
        data1 = process1(data)
        thread = threading.Thread(target=lambda: offload_process(data, 'process2', offload_url))
        thread.start()
        thread.join()
        data2 = offload_process(data, 'process2', offload_url)
    elif offload == 'both':
        thread1 = threading.Thread(target=lambda: offload_process(data, 'process1', offload_url))
        thread2 = threading.Thread(target=lambda: offload_process(data, 'process2', offload_url))
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        data1 = offload_process(data, 'process1', offload_url)
        data2 = offload_process(data, 'process2', offload_url)
    else:  # No offloading
        data1 = process1(data)
        data2 = process2(data)

    return final_process(data1, data2)

def main():
    samples = 5
    modes = [None, 'process1', 'process2', 'both']
    rows = []

    for mode in modes:
        times = []
        for _ in range(samples):
            start = time.time()
            run(mode)
            end = time.time()
            times.append(end - start)
        
        rows.append([mode, np.mean(times), np.std(times)])
    
    df = pd.DataFrame(rows, columns=['Mode', 'Mean Time', 'Std Dev'])

    fig = px.bar(df, x='Mode', y='Mean Time', error_y='Std Dev', title='Execution Times by Offloading Mode')
    fig.show()

if __name__ == '__main__':
    main()
